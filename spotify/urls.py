from django.contrib import admin
from django.urls import path, include
from .views import AuthURL, spotify_call_back, IsAuthenticated, CurrentSong, PauseSong, PlaySong, SkipSong

app_name = "spotify"

urlpatterns = [
    path('get-auth-url', AuthURL.as_view()),
    path('redirect', spotify_call_back),
    path('is-authenticated', IsAuthenticated.as_view()),
    path('get-current-song', CurrentSong.as_view()),
    path('play-song', PlaySong.as_view()),
    path('pause-song', PauseSong.as_view()),
    path('skip-song', SkipSong.as_view()),
]
