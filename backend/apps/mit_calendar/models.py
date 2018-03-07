from django.db import models
from django.utils import timezone
from colorful.fields import RGBColorField
from backend.abstract_models import TimeStampedModel
from apps.theater.models import Play


class EventManager(models.Manager):
    def enabled(self):
        """Возвращает категории с is_enabled=True."""
        return super(EventManager, self).get_queryset().filter(is_enabled=True)


class Event(TimeStampedModel):
    """Модель события."""
    play = models.ForeignKey(Play, verbose_name='Спектакль', on_delete=models.CASCADE)
    date = models.DateField('Дата')
    time = models.TimeField('Время')
    place = models.CharField('Место проведения', max_length=255)
    address = models.CharField('Адрес', max_length=255)
    latitude = models.FloatField('Широта')
    longitude = models.FloatField('Долгота')
    color = RGBColorField('Цвет маркера на карте', default='#FF0000')
    visitors_count = models.PositiveSmallIntegerField('Зрителей допускается', default=25)
    is_enabled = models.BooleanField('Включено', default=True)

    objects = EventManager()

    def __str__(self):
        return self.place

    @property
    def is_past_due(self):
        """Прошедшее ли это мероприятие."""
        return timezone.now().date() > self.date

    @staticmethod
    def get_future_events_count():
        """Возвращает количество будущих мероприятий"""
        return len(Event.objects.enabled().filter(date__gte=timezone.now().date()))

    @staticmethod
    def get_past_events_count():
        """Возвращает количество прошедших мероприятий"""
        return len(Event.objects.enabled().filter(date__lt=timezone.now().date()))

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'
        ordering = ('date',)
