# Generated by Django 5.0.6 on 2024-06-22 07:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0003_alter_advertisement_file_1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='author',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='advertisement.author'),
        ),
    ]