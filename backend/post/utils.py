# from django.core.mail import send_mail
# from django.conf import settings
# from .models import Order

# def send_order_email(order_id):
#     order = Order.objects.get(id=order_id)
#     subject = f'Подтверждение заказа #{order.id}'
#     # Форматируем дату
#     formatted_date = order.created_at.strftime('%d-%m-%Y %H:%M:%S')
#     message = f'Ваш заказ #{order.id} был успешно создан!\nДата создания: {formatted_date}\nВ ближайшее время с вами свяжется специалист.'
#     recipient_list = [order.user.email]
#     # Отправляем электронное письмо
#     send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)



# def delete_order(order_id):
#     try:
#         order = Order.objects.get(id=order_id)
#         subject = f'Удаление  заказа #{order.id}'
#         message = f'Ваш заказ #{order.id} удален!'
#         order.delete()
#         recipient_list = [order.user.email]
#         return send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
#     except Order.DoesNotExist:
#         return f'Order {order_id} does not exist.'

