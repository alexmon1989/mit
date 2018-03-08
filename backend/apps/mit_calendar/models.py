from django.db import models
from django.utils import timezone
from colorful.fields import RGBColorField
from ckeditor_uploader.fields import RichTextUploadingField
from backend.abstract_models import TimeStampedModel, SeoModel
from apps.theater.models import Play


class EventManager(models.Manager):
    def enabled(self):
        """Возвращает категории с is_enabled=True."""
        return super(EventManager, self).get_queryset().filter(is_enabled=True)


class Event(SeoModel, TimeStampedModel):
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
    text = RichTextUploadingField('Текст', null=True, blank=True)
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

    def get_spectators(self):
        """Возвращает зрителей мероприятия."""
        return self.spectator_set.all()

    def get_free_places_count(self):
        """Возвращает количество свободных мест для регистрации."""
        return self.visitors_count - len(self.get_spectators())

    def get_spectators_percent(self):
        """Возвращает заполненность зрителями в процентах"""
        return int((len(self.get_spectators()) / self.visitors_count) * 100)

    @property
    def is_registration_open(self):
        """Открыта ли регистрация на мероприятие."""
        if self.is_past_due or len(self.get_spectators()) >= self.visitors_count:
            return False
        return True

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'
        ordering = ('date',)


class Spectator(TimeStampedModel):
    """Модель зрителя мероприятия."""
    event = models.ForeignKey(Event, verbose_name='Событие', on_delete=models.CASCADE)
    username = models.CharField('Имя', max_length=255)
    phone = models.CharField('Телефон', max_length=255)
    email = models.EmailField('E-Mail', max_length=255)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Зритель'
        verbose_name_plural = 'Зрители'
        ordering = ('username',)
