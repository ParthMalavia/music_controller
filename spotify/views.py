from django.shortcuts import render, redirect
from .credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URL
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import requests
from requests.auth import HTTPBasicAuth
from .utils import update_or_create_token, is_spotify_authenticated, execute_spotify_api, play_song, pause_song, skip_song
from api.models import Room
from .models import Vote


class AuthURL(APIView):
    def get(self, request, format=None):
        try:
            scopes = "user-read-playback-state user-modify-playback-state user-read-currently-playing"

            url = requests.Request("GET", "https://accounts.spotify.com/authorize", params={
                "response_type": 'code',
                "client_id": CLIENT_ID,
                "scope": scopes,
                "redirect_uri": REDIRECT_URL,
            }).prepare().url

            return Response({"url": url}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"url": "-----url-----"}, status=status.HTTP_200_OK)


def spotify_call_back(request):
    code = request.GET.get('code', None)

    response = requests.post(
        "https://accounts.spotify.com/api/token", 
        data = {
            "grant_type": "authorization_code",
            "redirect_uri": REDIRECT_URL,
            "code": code
        },
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        auth=(CLIENT_ID, CLIENT_SECRET)).json()

    access_token = response.get("access_token")
    token_type = response.get("token_type")
    expires_in = response.get("expires_in")
    refresh_token = response.get("refresh_token")
    scope = response.get("scope")
    error = response.get("error")

    if not request.session.exists(request.session.session_key):
        request.session.create()

    update_or_create_token(
        request.session.session_key,
        access_token, token_type, expires_in, refresh_token, scope
    )

    return redirect("http://127.0.0.1:3000/")

class IsAuthenticated(APIView):
    def get(self, request, format=None):
        is_authenticated = is_spotify_authenticated(self.request.session.session_key)
        return Response({"status": is_authenticated}, status=status.HTTP_200_OK)
 

class CurrentSong(APIView):
    def get(self, request, format=None):
        room_code = self.request.session.get("room_code")
        room = Room.objects.filter(code=room_code).first()
        if not room:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        
        host = room.host
        endpoint = "/me/player/currently-playing"
        response = execute_spotify_api(endpoint, host)
        if "error" in response:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        is_playing = response.get("is_playing")
        item = response.get("item", {})
        duration = item.get("duration_ms")
        progress = response.get("progress_ms")
        album_img = item.get("album", {}).get("images", [{"url": ""}])[0].get("url")
        song_id = item.get("id")

        artist_string = ", ".join(map(lambda x: x.get("name"), item.get("artists")))

        votes = len(Vote.objects.filter(room=room, song_id=song_id))
        song = {
            "title": item.get("name"),
            "artist": artist_string,
            "duration": duration,
            "progress": progress,
            "image_url": album_img,
            "id": song_id,
            "is_playing": is_playing,
            "votes": votes,
            "votes_required": room.vote_to_skip,
        }

        self.update_room(room, song_id)

        return Response(song, status=status.HTTP_200_OK)
    
    def update_room(self, room: Room, song_id):
        current_song = room.current_song

        if current_song != song_id:
            room.current_song = song_id
            room.save(update_fields=['current_song'])
            votes = Vote.objects.filter(room=room).delete()

class PauseSong(APIView):
    def put(self, request, format=None):
        room_code = self.request.session.get("room_code")
        room = Room.objects.filter(code=room_code).first()
        
        if room.guest_can_pause or self.request.session.session_key == room.host:
            res = pause_song(room.host)
            return Response(res, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_403_FORBIDDEN)

class PlaySong(APIView):
    def put(self, request, format=None):
        room_code = self.request.session.get("room_code")
        room = Room.objects.filter(code=room_code).first()
        
        if room.guest_can_pause or self.request.session.session_key == room.host:
            res = play_song(room.host)
            return Response(res, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_403_FORBIDDEN)

class SkipSong(APIView):
    def post(self, request, format=None):
        room_code = self.request.session.get("room_code")
        room = Room.objects.filter(code=room_code).first()
        votes = Vote.objects.filter(room=room, song_id=room.current_song)
        votes_to_skip = room.vote_to_skip

        if self.request.session.session_key == room.host or len(votes) + 1 >= votes_to_skip :
            res = skip_song(room.host)
            votes.delete()
            return Response(res, status=status.HTTP_200_OK)
        else:
            vote = Vote(user=self.request.session.session_key, song_id=room.current_song, room = room)
            vote.save()
        
        return Response({}, status=status.HTTP_204_NO_CONTENT)

