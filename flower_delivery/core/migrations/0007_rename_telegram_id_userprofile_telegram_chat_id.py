# Generated by Django 5.1.2 on 2025-01-06 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_remove_userprofile_telegram_chat_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='telegram_id',
            new_name='telegram_chat_id',
        ),
    ]
