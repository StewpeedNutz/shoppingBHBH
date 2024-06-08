# Generated by Django 5.0.6 on 2024-06-01 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_remove_cart_phone_cart_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='username',
        ),
        migrations.AddField(
            model_name='cart',
            name='phone',
            field=models.CharField(default='', max_length=15),
        ),
    ]