from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('ws/chat/<uuid:dialog_id>/', consumers.ChatConsumer.as_asgi()),
]
