# Generated by Django 4.1.7 on 2023-07-29 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Books', '0010_alter_editions_pages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='editions',
            name='pages',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
