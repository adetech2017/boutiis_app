import json
from channels.generic.websocket import AsyncWebsocketConsumer




class ForumConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.forum_id = self.scope['url_route']['kwargs']['forum_id']
        self.forum_group_name = f'forum_{self.forum_id}'

        # Join forum group
        await self.channel_layer.group_add(
            self.forum_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave forum group
        await self.channel_layer.group_discard(
            self.forum_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        # Broadcast message to forum group
        await self.channel_layer.group_send(
            self.forum_group_name,
            {
                'type': 'forum_message',
                'message': text_data,
            }
        )

    # Receive message from forum group
    async def forum_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))
