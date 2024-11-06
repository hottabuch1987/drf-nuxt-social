from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/user-status/', consumers.StatusConsumer.as_asgi()),
]
