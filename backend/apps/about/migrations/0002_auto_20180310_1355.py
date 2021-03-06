# Generated by Django 2.0.3 on 2018-03-10 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='partner',
            options={'verbose_name': 'Партнёр проекта', 'verbose_name_plural': 'Партнёры проекта'},
        ),
        migrations.AlterField(
            model_name='about',
            name='partners',
            field=models.ManyToManyField(to='about.Partner', verbose_name='Партнёры проекта'),
        ),
        migrations.AlterField(
            model_name='about',
            name='persons',
            field=models.ManyToManyField(to='theater.Person', verbose_name='Команда проекта'),
        ),
    ]
