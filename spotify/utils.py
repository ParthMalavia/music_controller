from .models import SpotifyToken
from .credentials import CLIENT_ID, CLIENT_SECRET
from django.utils import timezone
from datetime import timedelta
import requests
import requests

BASE_URL = "https://api.spotify.com/v1"


def get_user_token(session_id) -> SpotifyToken | None:
    user_token = SpotifyToken.objects.filter(user=session_id).first()
    if user_token:
        return user_token
    return None

def update_or_create_token(session_id, access_token, token_type, expires_in, refresh_token, scope):
    token = get_user_token(session_id)
    expires_at = timezone.now() + timedelta(seconds=expires_in)

    if token:
        token.expires_at = expires_at
        token.refresh_token = refresh_token
        token.access_token = access_token
        token.token_type = token_type
        token.save()
    else:
        token = SpotifyToken(
            user = session_id,
            access_token = access_token,
            token_type = token_type,
            expires_at = expires_at,
            refresh_token = refresh_token,
        )
        token.save()

def is_spotify_authenticated(session_id):
    token = get_user_token(session_id)   
    print("is_spotify_authenticated >> token ::") 
    # print(token.expires_at) 
    if token:
        expires_at = token.expires_at
        print(expires_at, timezone.now())
        if expires_at <= timezone.now():
            refresh_spotify_token(session_id, token)
        return True

    return False

def refresh_spotify_token(session_id, token = None):

    refresh_token = token.refresh_token if token else get_user_token(session_id).refresh_token

    response = requests.post("https://accounts.spotify.com/api/token", data={
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }).json()
    print("refresh_spotify_token >> response ::", response)
 
    access_token = response.get("access_token")
    print("access_token >> ", access_token)
    token_type = response.get("token_type")
    expires_in = response.get("expires_in")
    scope = response.get("scope")

    update_or_create_token(
        session_id,
        access_token, token_type, expires_in, refresh_token, scope
    )

def execute_spotify_api(endpoint, session_id, post_=False, put_=False):
    token = get_user_token(session_id).access_token
    print("execute_spotify_api >> token :: ", token)
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(token)
    }
    method = "GET"
    if post_:
        method = "POST"
    if put_:
        method = "PUT"
    try:
        response = requests.request(method, BASE_URL+endpoint, headers=headers)
        if response.status_code == 204:
            return {"error": "No Content"}
        return response.json()
    except:
        return {"error": "error with request"}

def pause_song(session_id):
    return execute_spotify_api("/me/player/pause", session_id, put_=True)

def play_song(session_id):
    return execute_spotify_api("/me/player/play", session_id, put_=True)

def skip_song(session_id):
    return execute_spotify_api("/me/player/next", session_id, post_=True)
