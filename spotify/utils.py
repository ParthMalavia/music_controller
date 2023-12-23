from .models import SpotifyToken
from .credentials import CLIENT_ID, CLIENT_SECRET
from django.utils import timezone
from datetime import timedelta
import requests


def get_user_token(session_id) -> SpotifyToken | None:
    user_token = SpotifyToken.objects.filter(user=session_id).first()
    if user_token:
        return user_token
    return None

def update_or_create_token(session_id, access_token, token_type, expires_in, refresh_token, scope):
    token = get_user_token(session_id)
    expires_at = timezone.now() + timedelta(expires_in)

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
    print("is_spotify_authenticated >> token ::", token) 
    if token:
        expires_at = token.expires_at
        if expires_at <= timezone.now():
            refresh_spotify_token(session_id, token)
        return True

    return False

def refresh_spotify_token(session_id, token = None):

    refersh_token = token.refresh_token if token else get_user_token(session_id)

    response = requests.post("https://accounts.spotify.com/api/token", data={
        "grant_type": "refresh_token",
        "refresh_token": refersh_token,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }).json()
    print("refresh_spotify_token >> response ::", response)
 
    access_token = response.get("access_token")
    token_type = response.get("token_type")
    expires_in = response.get("expires_in")
    refresh_token = response.get("refresh_token")
    scope = response.get("scope")

    update_or_create_token(
        session_id,
        access_token, token_type, expires_in, refresh_token, scope
    )
