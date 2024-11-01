from rest_framework import generics
from .models import Dialog, Message
from .serializers import DialogSerializer, MessageSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from account.models import User
from rest_framework import status
from rest_framework.response import Response

class DialogListCreateView(generics.ListCreateAPIView):
    """Представление для получения списка и создания диалогов."""
    permission_classes = [IsAuthenticated]
    serializer_class = DialogSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['created_at']
    search_fields = ['user1__username', 'user2__username', 'created_at']
    ordering_fields = ['created_at']
    
    def get_queryset(self):
        """Возвращает диалоги текущего пользователя."""
        user = self.request.user
        return Dialog.objects.filter(Q(user1=user) | Q(user2=user))
    
    def perform_create(self, serializer):

        """Создание нового диалога."""
        user1 = self.request.user
        user2_id = self.request.data.get('user2')

        # Проверьте, существует ли второй пользователь
        user2 = User.objects.filter(id=user2_id).first()
        if not user2:
            return Response({"error": "Пользователь не существует."}, status=status.HTTP_400_BAD_REQUEST)

        # Проверьте, существует ли уже диалог между этими пользователями
        if Dialog.objects.filter(Q(user1=user1, user2=user2) | Q(user1=user2, user2=user1)).exists():
            return Response({"error": "Диалог уже существует."}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(user1=user1, user2=user2)
    
    

class DialogDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Представление для получения, обновления и удаления конкретного диалога."""
    permission_classes = [IsAuthenticated]
    queryset = Dialog.objects.all()

    def delete(self, request, *args, **kwargs):
        dialog = self.get_object()

        # Проверка, является ли пользователь одним из участников диалога

        if dialog.user1 != request.user and dialog.user2 != request.user:
            return Response({"error": "У вас нет прав для удаления этого диалога."}, status=status.HTTP_403_FORBIDDEN)

        dialog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MessageListCreateView(generics.ListCreateAPIView):
    """Представление для получения списка и создания сообщений в диалоге."""
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        dialog_id = self.kwargs['dialog_id']
        return Message.objects.filter(dialog__id=dialog_id)

class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Представление для получения, обновления и удаления конкретного сообщения."""
    queryset = Message.objects.all()
    serializer_class = MessageSerializer