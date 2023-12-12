from django.contrib import admin
from django.urls import path, include
from .views import AuthURL, spotify_call_back, IsAuthenticated

app_name = "spotify"

urlpatterns = [
    path('get-auth-url', AuthURL.as_view()),
    path('redirect', spotify_call_back),
    path('is-authenticated', IsAuthenticated.as_view()),
]
