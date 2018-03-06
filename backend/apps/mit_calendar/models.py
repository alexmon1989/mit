from django.db import models
from backend.abstract_models import TimeStampedModel
from apps.theater.models import Play


class Event(TimeStampedModel):
    """Модель события."""
    play = models.ForeignKey(Play, verbose_name='Спектакль', on_delete=models.CASCADE)
    date = models.DateField('Дата')
    time = models.TimeField('Время')
    place = models.CharField('Место проведения', max_length=255)
    address = models.CharField('Адрес', max_length=255)
    latitude = models.FloatField('Широта')
    longitude = models.FloatField('Долгота')
    visitors_count = models.PositiveSmallIntegerField('Зрителей допускается', default=25)
    is_enabled = models.BooleanField('Включено', default=True)

    def __str__(self):
        return self.place

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'
