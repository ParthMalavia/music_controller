from django.contrib import admin
from django.urls import path, include
from .views import CreateRoomView, GetRoomView, JoinRoomView, UserInRoom, LeaveRoom, TestView, csrf_token_view, UpdateRoom

app_name = "api"

urlpatterns = [
    # path('room', RoomView.as_view()),
    path('create-room', CreateRoomView.as_view()),
    path('get-room', GetRoomView.as_view()),
    path('join-room', JoinRoomView.as_view()),
    path('user-in-room', UserInRoom.as_view()),
    path('leave-room', LeaveRoom.as_view()),
    path('update-room', UpdateRoom.as_view()),
    path('test', TestView.as_view(), name="test"),
    path('csrf-token', csrf_token_view, name="csrf-token"),
]
