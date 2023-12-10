from django.contrib import admin
from django.urls import path, include

app_name = "api"

urlpatterns = [
    path('get-room', GetRoomView.as_view()),
]
