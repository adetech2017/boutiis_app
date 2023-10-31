from rest_framework import generics
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer
from django.contrib.auth import get_user_model
from django.shortcuts import render


class ChatRoomListCreateView(generics.ListCreateAPIView):
    serializer_class = ChatRoomSerializer

    def get_queryset(self):
        user = self.request.user  # Get the authenticated user
        return user.chat_rooms.all()  # Filter chat rooms by the user

    def perform_create(self, serializer):
        user = self.request.user  # Get the authenticated user
        serializer.save(users=[user])

class ChatRoomDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChatRoomSerializer

    def get_queryset(self):
        user = self.request.user  # Get the authenticated user
        return user.chat_rooms.all()  # Filter chat rooms by the user

class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        user = self.request.user  # Get the authenticated user
        return Message.objects.filter(chat_room__users=user)

class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        user = self.request.user  # Get the authenticated user
        return Message.objects.filter(chat_room__users=user)


def index(request):
    return render(request, "chat/index.html")


def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})