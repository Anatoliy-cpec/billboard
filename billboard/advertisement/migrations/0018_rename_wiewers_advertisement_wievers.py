# Generated by Django 5.0.6 on 2024-07-03 02:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0017_remove_advertisement_views_advertisement_wiewers_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='advertisement',
            old_name='wiewers',
            new_name='wievers',
        ),
    ]
