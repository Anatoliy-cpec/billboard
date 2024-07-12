# Generated by Django 5.0.6 on 2024-07-06 08:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0025_advertisement_state_alter_advertisement_body_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='disliked_authors',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='disliked', to='advertisement.author', verbose_name='Дизлайки'),
        ),
        migrations.AddField(
            model_name='advertisement',
            name='liked_authors',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='liked', to='advertisement.author', verbose_name='Лайки'),
        ),
    ]