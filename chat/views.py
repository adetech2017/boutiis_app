from rest_framework import generics, status
from rest_framework.response import Response
from .models import Message, PrivateRoom
from .serializers import MessageSerializer, PrivateRoomSerializer






class MessageView(generics.CreateAPIView):
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Assuming user is authenticated and attaching user to message
        user = self.request.user
        serializer.save(user=user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)



class PrivateRoomView(generics.CreateAPIView):
    serializer_class = PrivateRoomSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Assuming user is authenticated and attaching user1 to room
        user1 = self.request.user
        user2 = serializer.validated_data.get('user2')

        # Check if a room already exists between user1 and user2
        existing_room = PrivateRoom.objects.filter(user1=user1, user2=user2).first() \
                        or PrivateRoom.objects.filter(user1=user2, user2=user1).first()

        if existing_room:
            return Response(PrivateRoomSerializer(existing_room).data, status=status.HTTP_200_OK)

        # If no existing room, create a new one
        room = serializer.save(user1=user1)
        
        return Response(PrivateRoomSerializer(room).data, status=status.HTTP_201_CREATED)