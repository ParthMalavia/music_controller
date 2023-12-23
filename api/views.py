from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import random
from .serializer import RoomSerializer, CreateRoomSerializer, UpdateRoomSerializer
from .models import Room
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator

from django.http import HttpResponse, JsonResponse
from django.views import View

def csrf_token_view(request):
    # Get the CSRF token from the request
    X_CSRFToken = request.headers.get("X-CSRFToken")
    csrf_token = request.COOKIES.get('csrftoken')
    print("request.headers.get('X-CSRFToken'):::", X_CSRFToken)
    print("request.headers:::", request.headers)
    print("request.COOKIES.get('csrftoken'):::", request.COOKIES.get('csrftoken'))
    print("request.COOKIES:::", request.COOKIES)
    
    if csrf_token:
        return JsonResponse({'csrfToken': csrf_token})
    else:
        return JsonResponse({'error': 'CSRF token not found'}, status=400)

class TestView(View):
    def get(self, request):
        print(request.session.get('test_keys'))
        print(request.session.session_key)
        test_keys = request.session.get('test_keys', [])
        test_keys.append(random.randint(1, 100))
        request.session['test_keys'] = test_keys
        return HttpResponse(str(request.session.get('test_keys', [])))


class JoinRoomView(APIView):
    lookup_url_kwargs = "code"
    
    def post(self, request, code=None):
        print("JOIN ROOM")
        print(self.request.session.session_key)
        print(self.request.session.items())
        if not request.session.exists(request.session.session_key):
            request.session.create()
        
        code = request.data.get(self.lookup_url_kwargs)
        if code is not None:
            room = Room.objects.filter(code=code).first()
            if room:
                request.session["room_code"] = code
                return Response({'message': "Joined Room!!"}, status=status.HTTP_200_OK)
            return Response({'error': "Invalid room code."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': "Code Parameter not found in request."}, status=status.HTTP_400_BAD_REQUEST)

class GetRoomView(APIView):
    serializer_class = RoomSerializer
    lookup_url_kwargs = "code"
    def get(self, request, code=None):
        print("GET ROOM")
        print(request.session.items())
        print(self.request.session.items())
        print(request.session.session_key)
        print(self.request.session.session_key)
        code = request.GET.get(self.lookup_url_kwargs)
        if code:
            room = Room.objects.filter(code=code).first()
            if room:
                data = RoomSerializer(room).data
                # request.session["room_code"] = code
                data['is_host'] = request.session.session_key == room.host
                return Response(data, status=status.HTTP_200_OK)
            return Response({'error': "Invalid room code."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': "Code Parameter not found in request."}, status=status.HTTP_400_BAD_REQUEST)

class CreateRoomView(APIView):
    def post(self, request):
        print("CREATE ROOM")
        print(request.session.items())
        print(self.request.session.items())
        print(request.session.session_key)
        print(self.request.session.session_key)
        if not request.session.exists(request.session.session_key):
            request.session.create()
        serializer = CreateRoomSerializer(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get('guest_can_pause')
            vote_to_skip = serializer.data.get('vote_to_skip')
            host = request.session.session_key
            queryset = Room.objects.filter(host=host)

            if queryset.exists():
                room = queryset[0]
                room.guest_can_pause = guest_can_pause
                room.vote_to_skip = vote_to_skip
                request.session["room_code"] = room.code
                room.save(update_fields=['guest_can_pause', 'vote_to_skip'])
            else:
                room = Room(host=host,
                            guest_can_pause=guest_can_pause,
                            vote_to_skip=vote_to_skip)
                request.session["room_code"] = room.code
                room.save()

            return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserInRoom(APIView):
    def get(self, request):
        print("USER IN ROOM")
        if not request.session.exists(request.session.session_key):
            request.session.create()
        data = {
            "code": request.session.get("room_code")
        }
        print("Room Code >>", request.session.get("room_code"))
        return Response(data, status=status.HTTP_200_OK)

class LeaveRoom(APIView):
    def post(self, request):
        print("LEAVE ROOM")
        print("request.session >>", request.session.items())
        print("self.request.session >>", self.request.session.items())
        if "room_code" in request.session:
            request.session.pop("room_code")
            room = Room.objects.filter(host=request.session.session_key)
            if room:
                room.delete()
        print(" ------ AFTER DELETION -----")
        print("request.session >>", request.session.items())
        print("self.request.session >>", self.request.session.items())
        return Response({"message": "success"}, status=status.HTTP_200_OK)

class UpdateRoom(APIView):
    def patch(self, request):
        print("UPDATE ROOM")
        print(request.session.session_key)
        print(self.request.session.session_key)
        if not request.session.exists(request.session.session_key):
            request.session.create()

        serializer = UpdateRoomSerializer(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get('guest_can_pause')
            vote_to_skip = serializer.data.get('vote_to_skip')
            code = serializer.data.get('code')

            room = Room.objects.filter(code=code).first()
            if not room:
                return Response({'error': "Room not found"}, status=status.HTTP_404_NOT_FOUND)

            user_id = request.session.session_key
            if room.host != user_id:
                return Response({'error': "You are not the host"}, status=status.HTTP_403_FORBIDDEN)

            room.guest_can_pause = guest_can_pause
            room.vote_to_skip = vote_to_skip
            room.save(update_fields=['guest_can_pause', 'vote_to_skip'])
            return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
