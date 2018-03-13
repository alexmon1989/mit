# Generated by Django 2.0.3 on 2018-03-13 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mit_calendar', '0011_auto_20180312_1629'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='spectator',
            options={'ordering': ('last_name',), 'verbose_name': 'Зритель', 'verbose_name_plural': 'Зрители'},
        ),
        migrations.RenameField(
            model_name='spectator',
            old_name='username',
            new_name='first_name',
        ),
        migrations.AddField(
            model_name='spectator',
            name='last_name',
            field=models.CharField(default='', max_length=255, verbose_name='Фамилия'),
        ),
        migrations.AddField(
            model_name='spectator',
            name='patronymic_name',
            field=models.CharField(default='', max_length=255, verbose_name='Отчество'),
        ),
    ]