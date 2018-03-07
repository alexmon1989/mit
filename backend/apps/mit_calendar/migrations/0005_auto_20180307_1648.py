# Generated by Django 2.0.3 on 2018-03-07 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mit_calendar', '0004_event_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='meta_description',
            field=models.TextField(blank=True, null=True, verbose_name='Description (мета-тег)'),
        ),
        migrations.AddField(
            model_name='event',
            name='meta_h1',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Тег h1 (мета-тег)'),
        ),
        migrations.AddField(
            model_name='event',
            name='meta_keywords',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Keywords (мета-тег)'),
        ),
        migrations.AddField(
            model_name='event',
            name='meta_title',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Title (мета-тег)'),
        ),
    ]