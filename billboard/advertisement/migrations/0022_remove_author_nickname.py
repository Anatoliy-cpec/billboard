# Generated by Django 5.0.6 on 2024-07-03 07:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0021_alter_advertisement_file_1_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='nickname',
        ),
    ]
