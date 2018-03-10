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
    """Модель мероприятия."""
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
