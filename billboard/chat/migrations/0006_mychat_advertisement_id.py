# Generated by Django 5.0.6 on 2024-07-12 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_mychat_chat_name_alter_chatmessage_message_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mychat',
            name='advertisement_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
