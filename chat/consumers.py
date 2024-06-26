import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Message, PrivateRoom
from .serializers import MessageSerializer, PrivateRoomSerializer
from rest_framework.exceptions import ValidationError
from core.models import User





class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'
        self.room = await self.get_room(self.room_id)
        
        if self.room and self.scope['user'] in [self.room.user1, self.room.user2]:
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
            # Send the last 50 messages to the user
            await self.send_last_messages()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.room and self.scope['user'] in [self.room.user1, self.room.user2]:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive_json(self, content):
        message = content['message']
        user = self.scope['user']

        if user.is_authenticated and self.room and user in [self.room.user1, self.room.user2]:
            await self.save_message(user, message)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'user': user.username,
                    'message': message
                }
            )

    async def chat_message(self, event):
        await self.send_json({
            'user': event['user'],
            'message': event['message']
        })


    @sync_to_async
    def save_message(self, user, message):
        Message.objects.create(room=self.room, user=user, content=message)

    async def send_last_messages(self):
        last_messages = await sync_to_async(list)(
            Message.objects.filter(room=self.room).order_by('-timestamp')[:50]
        )
        last_messages.reverse()  # Display the last messages in the correct order
        serializer = MessageSerializer(last_messages, many=True)
        await self.send_json({
            'type': 'last_messages',
            'messages': serializer.data
        })

    async def send_room_details(self):
        serializer = PrivateRoomSerializer(self.room)
        await self.send_json({
            'type': 'room_details',
            'room': serializer.data
        })

    @sync_to_async
    def get_room(self, room_id):
        try:
            return PrivateRoom.objects.get(id=room_id)
        except PrivateRoom.DoesNotExist:
            return None

