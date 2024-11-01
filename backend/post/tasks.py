# from celery import shared_task
# from django.core.mail import send_mail
# from django.utils import timezone
# from .models import Order

# @shared_task
# def send_order_email(order_id):
#     try:
#         order = Order.objects.get(id=order_id)
#         subject = f'Подтверждение заказа #{order.id}'
#         formatted_date = order.created_at.strftime('%d-%m-%Y %H:%M:%S')
#         message = f'Ваш заказ {order.product.name} #{order.id} был успешно создан!\nДата создания: {formatted_date}\nВ ближайшее время с вами свяжется специалист.'
#         recipient_list = [order.user.email]

#         if recipient_list:
#             send_mail(subject, message, 'varvar1987a@mail.ru', recipient_list)
#         else:
#             print('Нет почтового адреса для пользователя.')
#     except Order.DoesNotExist:
#         print(f'Заказ с id {order_id} не найден.')
#     except Exception as e:
#         print(f'Ошибка при отправке письма: {str(e)}')


# @shared_task
# def delete_order(order_id):
#     try:
#         order = Order.objects.get(id=order_id)
#         subject = f'Удаление  заказа #{order.id}'
#         message = f'Ваш заказ #{order.id} удален!'
#         order.delete()
#         recipient_list = [order.user.email]
#         return send_mail(subject, message, 'varvar1987a@mail.ru', recipient_list)
#     except Order.DoesNotExist:
#         return f'Order {order_id} does not exist.'

