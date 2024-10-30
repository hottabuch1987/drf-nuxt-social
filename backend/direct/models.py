from django.db import models
from account.models import User
import uuid

class Dialog(models.Model):
    """Модель для хранения личных переписок между пользователями."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user1 = models.ForeignKey(User, related_name='dialog_user1', on_delete=models.CASCADE, verbose_name="Пользователь 1")
    user2 = models.ForeignKey(User, related_name='dialog_user2', on_delete=models.CASCADE, verbose_name="Пользователь 2")
    created_at = models.DateTimeField("Дата", auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')  # Обеспечиваем уникальность пары пользователей
        verbose_name = 'Личный диалог'
        verbose_name_plural = 'Личные диалоги'
        ordering = ('-created_at',)

    def __str__(self):
        return f'Диалог между {self.user1.username} и {self.user2.username}'

class Message(models.Model):
    """Сообщения в личном диалоге."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    dialog = models.ForeignKey(Dialog, related_name='messages', on_delete=models.CASCADE, verbose_name='Диалог')
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE, verbose_name='Отправитель')
    content = models.TextField('Текст сообщения')
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('Прочитано', 'Прочитано'),
        ('Не прочитано', 'Не прочитано')
    ], default='Не прочитано')

    class Meta:
        ordering = ('-timestamp',)
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        indexes = [
            models.Index(fields=['sender']),
            models.Index(fields=['timestamp']),
        ]

    def mark_as_read(self):
        """Изменяет статус сообщения на 'прочитано'."""
        self.status = 'Прочитано'
        self.save()

    def mark_as_unread(self):
        """Изменяет статус сообщения на 'не прочитано'."""
        self.status = 'Не прочитано'
        self.save()

    def __str__(self):
        return f'Сообщение от {self.sender.username} в диалоге {self.dialog}'