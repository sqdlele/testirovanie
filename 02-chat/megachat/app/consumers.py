import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, Message


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_slug = None
        self.room_group_name = None
        self.user_name = None

    async def connect(self):
        self.room_slug = self.scope['url_route']['kwargs']['slug']
        self.room_group_name = f'chat_{self.room_slug}'
        self.user_name = 'Аноним'

        room_exists = await database_sync_to_async(
            Room.objects.filter(slug=self.room_slug).exists
        )()
        if not room_exists:
            await self.close()
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if self.room_group_name:
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            if data.get('type') == 'set_username':
                self.user_name = (data.get('user_name') or '').strip() or 'Аноним'
                return
            content = (data.get('content') or '').strip()
            if not content:
                return
            message = await self.save_message(content)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                },
            )
        except (json.JSONDecodeError, KeyError):
            pass

    @database_sync_to_async
    def save_message(self, content):
        room = Room.objects.get(slug=self.room_slug)
        msg = Message.objects.create(
            room=room,
            user_name=self.user_name,
            content=content,
        )
        return {
            'id': msg.id,
            'user_name': msg.user_name,
            'content': msg.content,
            'timestamp': msg.timestamp.strftime('%H:%M'),
        }

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event['message']))
