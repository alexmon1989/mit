# Generated by Django 2.0.3 on 2018-03-07 17:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mit_calendar', '0006_spectator'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='spectator',
            options={'ordering': ('username',), 'verbose_name': 'Зритель', 'verbose_name_plural': 'Зрители'},
        ),
    ]