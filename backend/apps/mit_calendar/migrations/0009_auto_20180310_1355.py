# Generated by Django 2.0.3 on 2018-03-10 11:55

import apps.mit_calendar.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mit_calendar', '0008_eventphoto_eventvideo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventphoto',
            name='image',
            field=models.ImageField(help_text='Оптимальный размер: 900px*600px.', upload_to=apps.mit_calendar.models.EventPhoto.upload_to, verbose_name='Изображение'),
        ),
    ]
