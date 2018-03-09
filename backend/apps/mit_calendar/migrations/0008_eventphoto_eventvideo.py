# Generated by Django 2.0.3 on 2018-03-09 08:27

import apps.mit_calendar.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mit_calendar', '0007_auto_20180307_1916'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
                ('image', models.ImageField(help_text='Оптимальный размер: 800px*500px.', upload_to=apps.mit_calendar.models.EventPhoto.upload_to, verbose_name='Изображение')),
                ('is_visible', models.BooleanField(default=True, verbose_name='Включено')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mit_calendar.Event', verbose_name='Мероприятие')),
            ],
            options={
                'verbose_name': 'Изображение',
                'verbose_name_plural': 'Изображения',
            },
        ),
        migrations.CreateModel(
            name='EventVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
                ('youtube_id', models.CharField(help_text='Например, для видео https://www.youtube.com/watch?v=JMJXvsCLu6, его идентификатором будет JMJXvsCLu6.', max_length=32, verbose_name='Идентификатор на Youtube')),
                ('is_visible', models.BooleanField(default=True, verbose_name='Включено')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mit_calendar.Event', verbose_name='Мероприятие')),
            ],
            options={
                'verbose_name': 'Видео',
                'verbose_name_plural': 'Видео',
            },
        ),
    ]
