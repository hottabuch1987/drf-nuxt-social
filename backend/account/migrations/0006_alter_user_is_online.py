# Generated by Django 4.2.16 on 2024-11-06 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_user_is_online'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_online',
            field=models.BooleanField(default=False, verbose_name='Онлайн статус'),
        ),
    ]