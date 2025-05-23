# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message, Dialog
from .tasks import send_new_message_notification

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.dialog_id = self.scope['url_route']['kwargs']['dialog_id']
        self.dialog_group_name = f'chat_{self.dialog_id}'

        # Присоединяемся к группе диалога
        await self.channel_layer.group_add(
            self.dialog_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Отключаемся от группы диалога
        await self.channel_layer.group_discard(
            self.dialog_group_name,
            self.channel_name
        )

   

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_content = text_data_json['message']
        user_id = text_data_json['user_id']  # ID отправителя

        # Получаем диалог и создаем сообщение в базе данных
        dialog = await self.get_dialog(self.dialog_id)
        message = await self.create_message(dialog, user_id, message_content)

        # Отправляем сообщение в группу
        await self.channel_layer.group_send(
            self.dialog_group_name,
            {
                'type': 'chat_message',
                'content': message_content,
                'sender_id': str(user_id),  # Преобразуем в строку
                'timestamp': message.timestamp.isoformat(),
            }
        )

        # Отправляем уведомление о новом сообщении
        await self.channel_layer.group_send(
            self.dialog_group_name,
            {
                'type': 'new_message_notification',
                'sender_id': str(user_id),  # Преобразуем в строку
                'message_id': str(message.id),  # Преобразуем в строку, если нужно
            }
        )





    @database_sync_to_async
    def get_dialog(self, dialog_id):
        return Dialog.objects.get(id=dialog_id)

    @database_sync_to_async
    def create_message(self, dialog, user_id, content):
        message = Message.objects.create(
            dialog=dialog,
            sender_id=user_id,
            content=content
        )
        send_new_message_notification.delay(message.id)
        return message

    async def chat_message(self, event):
        content = event['content']
        sender_id = event['sender_id']
        timestamp = event['timestamp']

        # Отправляем сообщение через веб-сокет
        await self.send(text_data=json.dumps({
            'message': content,
            'sender_id': sender_id,
            'timestamp': timestamp,
        }))


    async def new_message_notification(self, event):
    # Логика для отправки уведомления
        notification_message = f"Новое сообщение от {event['sender_id']}!"
        print(notification_message)  # Выводим уведомление в консоль для отладки
        await self.send(text_data=json.dumps({
            'notification': notification_message,
            'message_id': event['message_id'],
        }))







    # async def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message_content = text_data_json['message']
    #     user_id = text_data_json['user_id']  # ID отправителя

    #     # Получаем диалог и создаем сообщение в базе данных
    #     dialog = await self.get_dialog(self.dialog_id)
    #     message = await self.create_message(dialog, user_id, message_content)

    #     # Отправляем сообщение в группу
    #     await self.channel_layer.group_send(
    #         self.dialog_group_name,
    #         {
    #             'type': 'chat_message',
    #             'content': message_content,
    #             'sender_id': user_id,
    #             'timestamp': message.timestamp.isoformat(),
    #         }
    #     )



