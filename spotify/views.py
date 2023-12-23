from django.shortcuts import render, redirect
from .credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URL
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import requests
from requests.auth import HTTPBasicAuth
from .utils import update_or_create_token, is_spotify_authenticated


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
            print("EROOOORR:::", e)
            return Response({"url": "-----url-----"}, status=status.HTTP_200_OK)


def spotify_call_back(request):
    code = request.GET.get('code', None)
    state = request.GET.get('state', None)
    print("spotify_call_back >> code ::", code)
    print("spotify_call_back >> state ::", state)

    response = requests.post(
        "https://accounts.spotify.com/api/token", 
        data= {
            "grant_type": "authorization_code",
            "redirect_uri": REDIRECT_URL,
            "code": code
        },
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
        }, auth=(CLIENT_ID, CLIENT_SECRET)).json()
    print("spotify_call_back >> response ::", response)

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
    print("request.headers >>> ", request.headers)

    return redirect("http://127.0.0.1:3000/")

class IsAuthenticated(APIView):
    def get(self, request, format=None):
        is_authenticated = is_spotify_authenticated(self.request.session.session_key)
        return Response({"status": is_authenticated}, status=status.HTTP_200_OK)
 



