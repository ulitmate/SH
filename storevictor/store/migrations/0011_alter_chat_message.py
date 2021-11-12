# Generated by Django 3.2.8 on 2021-10-23 20:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_alter_chat_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='message',
            field=models.TextField(blank=True, max_length=300, null=True, validators=[django.core.validators.RegexValidator(code='invalid_username', message='Please ensure that you use right characters in your message', regex='[*aA-zZ1234567890{}$%_-\\/~@#$%^&*()!?]*$')], verbose_name='Chat Payload'),
        ),
    ]