import json
from django.urls import reverse
from django.db import models
from django.db.models import Count
from django.utils import timezone
from django.template import loader
from colorful.fields import RGBColorField
from ckeditor_uploader.fields import RichTextUploadingField
from backend.abstract_models import TimeStampedModel, SeoModel
from apps.theater.models import Play


class EventManager(models.Manager):
    def enabled(self):
        """Возвращает категории с is_enabled=True."""
        return super(EventManager, self).get_queryset().filter(is_enabled=True)

    def future(self):
        """Возвращает категории с is_enabled=True."""
        return super(EventManager, self).get_queryset().filter(date__gte=timezone.now())

    def past(self):
        """Возвращает категории с is_enabled=True."""
        return super(EventManager, self).get_queryset().filter(date__lt=timezone.now())


class Event(SeoModel, TimeStampedModel):
    """Модель мероприятия."""
    play = models.ForeignKey(Play, verbose_name='Спектакль', on_delete=models.CASCADE)
    date = models.DateField('Дата')
    time = models.TimeField('Время')
    place = models.ForeignKey(
        'Place',
        verbose_name='Место проведения',
        null=True,
        on_delete=models.SET_NULL
    )
    visitors_count = models.PositiveSmallIntegerField('Зрителей допускается', default=25)
    text = RichTextUploadingField('Текст', null=True, blank=True)
    registration_closed = models.BooleanField(
        'Закрыть возможность регистрации',
        default=False,
        help_text='Принудительно запретить возможность регистрации посетителей на мероприятие, '
                  'в незавсимости от кол-ва уже зарегистрированных персон.'
    )
    is_enabled = models.BooleanField('Включено', default=True)

    objects = EventManager()

    def __str__(self):
        if self.place:
            return '{} {} - {}'.format(self.date, self.time, self.place.title)
        return 'Событие'

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

    def get_photos(self):
        """Возвращает список фотографий спектакля."""
        return self.eventphoto_set.filter(is_visible=True).order_by('created_at').all()

    def get_videos(self):
        """Возвращает список видео спектакля."""
        return self.eventvideo_set.filter(is_visible=True).order_by('created_at').all()

    def get_media_count(self):
        """Возвращает количество медиа (фото + видео)."""
        return len(self.get_photos()) + len(self.get_videos())

    @property
    def is_registration_open(self):
        """Открыта ли регистрация на мероприятие."""
        if self.registration_closed or self.is_past_due or len(self.get_spectators()) >= self.visitors_count:
            return False
        return True

    def get_absolute_url(self):
        return reverse('calendar_event_detail', args=[self.pk])

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'
        ordering = ('date', 'time')


class Spectator(TimeStampedModel):
    """Модель зрителя мероприятия."""
    event = models.ForeignKey(Event, verbose_name='Событие', on_delete=models.CASCADE)
    first_name = models.CharField('Имя', max_length=255)
    last_name = models.CharField('Фамилия', max_length=255, default='')
    patronymic_name = models.CharField('Отчество', max_length=255, default='')
    phone = models.CharField('Телефон', max_length=255)
    email = models.EmailField('E-Mail', max_length=255)

    def __str__(self):
        return '{} {} {}'.format(self.last_name, self.first_name, self.patronymic_name)

    class Meta:
        verbose_name = 'Зритель'
        verbose_name_plural = 'Зрители'
        ordering = ('last_name',)


class EventPhoto(TimeStampedModel):
    """Модель фотографии."""

    def upload_to(instance, filename):
        return 'events/{}/{}'.format(instance.event.pk, filename)

    image = models.ImageField(
        'Изображение',
        upload_to=upload_to,
        help_text='Оптимальный размер: 900px*600px.'
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='Мероприятие')
    is_visible = models.BooleanField('Включено', default=True)

    def __str__(self):
        return 'Изображение #{}'.format(self.pk)

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class EventVideo(TimeStampedModel):
    """Модель видео спектакля."""
    youtube_id = models.CharField(
        'Идентификатор на Youtube',
        help_text='Например, для видео https://www.youtube.com/watch?v=JMJXvsCLu6, '
                  'его идентификатором будет JMJXvsCLu6.',
        max_length=32
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='Мероприятие')
    is_visible = models.BooleanField('Включено', default=True)

    def __str__(self):
        return 'Видео #{}'.format(self.pk)

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'


class PlaceManager(models.Manager):
    def with_future_events(self):
        """Возвращает категории с is_enabled=True."""
        return super(PlaceManager, self).get_queryset().filter(event__date__gte=timezone.now())


class Place(TimeStampedModel):
    """Модель места проведения спектаклей."""
    title = models.CharField('Название места', max_length=255)
    address = models.CharField('Адрес', max_length=255)
    latitude = models.FloatField('Широта')
    longitude = models.FloatField('Долгота')
    color = RGBColorField('Цвет маркера на карте', default='#FF0000')

    objects = PlaceManager()

    def __str__(self):
        return '{} ({})'.format(self.title, self.address)

    def get_map_marker_balloon(self):
        """Возвращает JSON для баллуна метки на карте."""
        future_events = self.get_future_events().annotate(Count('spectator'))

        res = {
            'header': self.title,
            'body': loader.render_to_string(
                'mit_calendar/map_marker_balloon.html', {
                    'place': self,
                    'future_events': future_events
                }
            )
        }
        return json.dumps(res)

    def get_future_events(self):
        """Возвращает будущие мероприятия в этом месте."""
        return self.event_set.filter(date__gte=timezone.now()).values(
            'pk', 'play__title', 'date', 'time', 'visitors_count'
        )

    class Meta:
        verbose_name = 'Место'
        verbose_name_plural = 'Места'
        ordering = ('title',)
