from rest_framework import serializers
from .models import Dialog, Message
from account.serializers import UserSerializer


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'dialog', 'sender', 'content', 'timestamp', 'status']

class DialogSerializer(serializers.ModelSerializer):
    user1 = UserSerializer(read_only=True)
    user2 = UserSerializer(read_only=True)
    # messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Dialog
        fields = ['id', 'user1', 'user2', 'created_at']
