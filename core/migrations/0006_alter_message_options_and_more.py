# Generated by Django 5.1.3 on 2025-04-25 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_message_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['sent_at']},
        ),
        migrations.RenameField(
            model_name='message',
            old_name='receiver',
            new_name='recipient',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='timestamp',
            new_name='sent_at',
        ),
        migrations.AddField(
            model_name='message',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]
