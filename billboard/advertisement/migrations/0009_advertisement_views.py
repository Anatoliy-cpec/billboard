# Generated by Django 5.0.6 on 2024-06-22 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0008_alter_advertisement_header_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='views',
            field=models.PositiveIntegerField(default=1, verbose_name='Просмотры'),
        ),
    ]
