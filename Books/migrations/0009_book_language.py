# Generated by Django 4.1.7 on 2023-07-29 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Books', '0008_alter_bookreview_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='language',
            field=models.CharField(default='English', max_length=50),
        ),
    ]
