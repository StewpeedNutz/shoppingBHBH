# Generated by Django 5.0.6 on 2024-05-27 11:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_customer_email_customer_passw'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='passw',
            new_name='password',
        ),
    ]
