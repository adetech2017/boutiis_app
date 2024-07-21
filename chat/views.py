from rest_framework import generics, status
from rest_framework.response import Response
from .models import Message, PrivateRoom
from .serializers import MessageSerializer, PrivateRoomSerializer, PrivateRoomDetailSerializer
from django.db.models import Q
from core.models import User





class MessageView(generics.CreateAPIView):
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Assuming user is authenticated and attaching user to message
        user = self.request.user
        serializer.save(user=user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)



class PrivateRoomView(generics.GenericAPIView):
    serializer_class = PrivateRoomSerializer

    def get(self, request, *args, **kwargs):
        user1 = request.user
        user2_id = self.kwargs['user_id']

        # Prevent creating a room with the same user but return existing room details if they exist
        if user1.id == user2_id:
            existing_room = PrivateRoom.objects.filter(
                Q(user1=user1, user2=user1)
            ).first()
            if existing_room:
                serializer = PrivateRoomSerializer(existing_room)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"message": "Cannot create a room with the same user"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user2 = User.objects.get(id=user2_id)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check for an existing room
        existing_room = PrivateRoom.objects.filter(
            Q(user1=user1, user2=user2) | Q(user1=user2, user2=user1)
        ).first()

        if existing_room:
            serializer = PrivateRoomSerializer(existing_room)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Create new room
        context = self.get_serializer_context()
        context['user_id'] = user2_id
        serializer = self.get_serializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        room = serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserChatsView(generics.GenericAPIView):
    serializer_class = PrivateRoomDetailSerializer

    def get(self, request, *args, **kwargs):
        user = request.user

        # Fetch all rooms where the user is either user1 or user2 profilePicture: json['profile_picture'],
        rooms = PrivateRoom.objects.filter(user1=user).union(PrivateRoom.objects.filter(user2=user))
        
        chats_data = []
        for room in rooms:
            last_message = Message.objects.filter(room=room).order_by('-timestamp').first()
            room_data = PrivateRoomDetailSerializer(room).data
            room_data['last_message'] = MessageSerializer(last_message).data if last_message else None
            chats_data.append(room_data)
        
        return Response(chats_data, status=status.HTTP_200_OK)


class PrivateRoomMessagesView(generics.GenericAPIView):
    serializer_class = MessageSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        room_id = self.kwargs['room_id']

        try:
            room = PrivateRoom.objects.get(id=room_id)
        except PrivateRoom.DoesNotExist:
            return Response({"message": "Room not found"}, status=status.HTTP_404_NOT_FOUND)

        if user not in [room.user1, room.user2]:
            return Response({"message": "You do not have access to this room"}, status=status.HTTP_403_FORBIDDEN)

        messages = Message.objects.filter(room=room).order_by('timestamp')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user
        room_id = self.kwargs['room_id']

        try:
            room = PrivateRoom.objects.get(id=room_id)
        except PrivateRoom.DoesNotExist:
            return Response({"message": "Room not found"}, status=status.HTTP_404_NOT_FOUND)

        if user not in [room.user1, room.user2]:
            return Response({"message": "You do not have access to this room"}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        data['user'] = user.id
        data['room'] = room.id

        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)