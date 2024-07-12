# Generated by Django 5.0.6 on 2024-06-27 07:03

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0014_remove_advertisement_response_advertisement_response'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата создания'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='advertisement',
            name='response',
            field=models.ManyToManyField(blank=True, related_name='responses', to='advertisement.message', verbose_name='Отклики'),
        ),
    ]
