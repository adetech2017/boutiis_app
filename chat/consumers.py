import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from core.models import User
from .models import PrivateRoom, Message





class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        # Get the user from the scope (assuming user is authenticated)
        self.user = self.scope['user']
        print(f"Received user: {self.user}")

        if self.user.is_anonymous:
            await self.close()
        else:
            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type')
        message = text_data_json.get('message')

        if self.scope.get('user') and not self.scope['user'].is_anonymous:
            user = self.scope['user'].username

            if message_type == 'typing':
                # Broadcast typing status to room group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'user_typing',
                        'user': self.scope['user'].username,
                    }
                )
            else:
                # Save message to the database
                await self.save_message_to_db(message)

                # Broadcast message to room group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message,
                        'user': self.scope['user'].username,
                    }
                )
                print(f"Received message: {message}, from user: {user}")
        else:
            print("Received message from anonymous or unauthenticated user.")

    async def chat_message(self, event):
        message = event['message']
        user = event['user']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user
        }))

    async def user_typing(self, event):
        user = event['user']

        # Send typing status to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'user': user
        }))

    @database_sync_to_async
    def save_message_to_db(self, message):
        room = PrivateRoom.objects.get(id=self.room_id)
        try:
            user = User.objects.get(id=self.scope['user'].id)
        except User.DoesNotExist:
            print(f"User with ID {self.scope['user'].id} does not exist")
            return

        return Message.objects.create(room=room, user=user, content=message)
