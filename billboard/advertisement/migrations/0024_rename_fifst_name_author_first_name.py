# Generated by Django 5.0.6 on 2024-07-04 06:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0023_alter_author_bio_alter_author_fifst_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='fifst_name',
            new_name='first_name',
        ),
    ]
