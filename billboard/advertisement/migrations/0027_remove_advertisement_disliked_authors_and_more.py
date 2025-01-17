# Generated by Django 5.0.6 on 2024-07-06 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0026_advertisement_disliked_authors_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advertisement',
            name='disliked_authors',
        ),
        migrations.RemoveField(
            model_name='advertisement',
            name='liked_authors',
        ),
        migrations.AddField(
            model_name='advertisement',
            name='disliked_authors',
            field=models.ManyToManyField(blank=True, related_name='disliked_authors', to='advertisement.author', verbose_name='Дизлайки'),
        ),
        migrations.AddField(
            model_name='advertisement',
            name='liked_authors',
            field=models.ManyToManyField(blank=True, related_name='liked_authors', to='advertisement.author', verbose_name='Лайки'),
        ),
    ]
