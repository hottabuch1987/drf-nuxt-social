from django.apps import AppConfig


class DirectConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'direct'
    verbose_name = 'Личные диалоги'
