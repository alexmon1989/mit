# Generated by Django 2.0.2 on 2018-03-06 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('theater', '0003_personplayrole_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
                ('date', models.DateField(verbose_name='Дата')),
                ('time', models.TimeField(verbose_name='Время')),
                ('place', models.CharField(max_length=255, verbose_name='Место проведения')),
                ('address', models.CharField(max_length=255, verbose_name='Адрес')),
                ('latitude', models.FloatField(verbose_name='Широта')),
                ('longitude', models.FloatField(verbose_name='Долгота')),
                ('visitors_count', models.PositiveSmallIntegerField(default=25, verbose_name='Зрителей допускается')),
                ('play', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='theater.Play', verbose_name='Спектакль')),
            ],
            options={
                'verbose_name': 'Событие',
                'verbose_name_plural': 'События',
            },
        ),
    ]
