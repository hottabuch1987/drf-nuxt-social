import json
from channels.generic.websocket import AsyncWebsocketConsumer


class StatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        print(self.user.username)
        await self.channel_layer.group_add(
            "status",
            self.channel_name
        )
        await self.accept()

        # Отправляем сообщение о новом пользователе
        await self.channel_layer.group_send(
            "status",
            {
                'type': 'send_status_update',
                'username': self.user.username,
                'status': 'online'
            }
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "status",
            self.channel_name
        )

        # Отправляем сообщение о том, что пользователь вышел
        await self.channel_layer.group_send(
            "status",
            {
                'type': 'send_status_update',
                'username': self.user.username,
                'status': 'offline'
            }
        )

    async def send_status_update(self, event):
        await self.send(text_data=json.dumps({
            'username': event['username'],
            'status': event['status'],
        }))
