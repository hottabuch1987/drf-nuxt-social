# tasks.py
from celery import shared_task
from django.core.mail import send_mail
import time
from django.conf import settings


@shared_task
def send_verification_email(email, code):
    subject = 'Подтверждение электронной почты'
    message = f'Добро пожаловать на наш сайт! Ваш код подтверждения: {code}'
    from_email = settings.EMAIL_HOST_USER  # Изменено здесь
    recipient_list = [email]

    print('send_verification_email', email, code, recipient_list, from_email)
    try:
        send_mail(subject, message, from_email, recipient_list)
        return True
    except Exception as e:
        # Log the error or handle it as appropriate
        print(f"Ошибка при отправке письма: {e}")
        return False
    


@shared_task
def debug_task():
    time.sleep(5)
    print('hello from debug task')