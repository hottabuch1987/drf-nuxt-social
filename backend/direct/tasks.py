from celery import shared_task
from .models import Message
from django.core.mail import send_mail  
from django.conf import settings

@shared_task
def send_new_message_notification(message_id):
    message = Message.objects.get(id=message_id)

    # Отправляем уведомление получателю
    send_mail(
        subject='Новое сообщение',
        message=f'Вы получили новое сообщение от {message.sender.username}: {message.content}',
        from_email = settings.EMAIL_HOST_USER,

        recipient_list=[message.dialog.user2.email],  # Уведомление для получателя
    )


