# Generated by Django 4.1.6 on 2023-02-23 03:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_contact'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='body',
            new_name='message',
        ),
    ]
