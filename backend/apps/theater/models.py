from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from backend.abstract_models import TimeStampedModel, SeoModel


class Position(TimeStampedModel):
    """Модель должности."""
    title = models.CharField('Название', max_length=255)
    weight = models.PositiveIntegerField(
        'Вес',
        default=10000,
        help_text='Чем выше вес, тем "выше" сотрудник с этой должностью на странице.'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'
        ordering = ('title',)


class Person(TimeStampedModel):
    """Модель сотрудника театра."""
    name = models.CharField('ФИО', max_length=255)
    image = models.ImageField(
        'Фото',
        upload_to='people/',
        null=True,
        blank=True,
        help_text='Оптимальный размер: 400px*450px.'
    )
    position = models.ForeignKey(Position, on_delete=models.CASCADE, verbose_name='Должность')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Персона'
        verbose_name_plural = 'Персоны'
        ordering = ('name',)


class Genre(TimeStampedModel):
    """Модель жанра."""
    title = models.CharField('Название', max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('title',)


class Play(SeoModel, TimeStampedModel):
    """Модель спектакля."""
    title = models.CharField('Название', max_length=255)
    genre = models.ForeignKey(Genre, verbose_name='Жанр', on_delete=models.SET_NULL, null=True, blank=True)
    duration = models.DurationField('Продолжительность', null=True, blank=True, help_text='Используйте формат ЧЧ:ММ:СС')
    text = RichTextUploadingField('Текст', null=True, blank=True)

    def __str__(self):
        return self.title

    def get_first_photo(self):
        """Возвращает первое фото спектакля или None."""
        photos = self.get_photos()
        if photos:
            return photos.first()
        return None

    def get_photos(self):
        """Возвращает список фотографий спектакля."""
        return self.playphoto_set.filter(is_visible=True).order_by('created_at').all()

    def get_videos(self):
        """Возвращает список видео спектакля."""
        return self.playvideo_set.filter(is_visible=True).order_by('created_at').all()

    def get_properties(self):
        """Возвращает список свойств спектакля."""
        return self.playproperty_set.order_by('created_at').all()

    def get_future_events(self):
        """Возвращает список будущих событий со спектаклем."""
        return self.event_set.filter(date__gte=timezone.now(), is_enabled=True).all()

    class Meta:
        verbose_name = 'Спектакль'
        verbose_name_plural = 'Спектакли'
        ordering = ('title',)


class PlayProperty(TimeStampedModel):
    """Модель свойства спектакля (режиссёр, автор и т.д.)."""
    play = models.ForeignKey(Play, on_delete=models.CASCADE, verbose_name='Спектакль')
    key = models.CharField('Ключ', max_length=255)
    value = models.CharField('Значение', max_length=255)

    def __str__(self):
        return self.key

    class Meta:
        verbose_name = 'Свойство'
        verbose_name_plural = 'Свойства'
        ordering = ('created_at',)


class PlayPhoto(TimeStampedModel):
    """Модель фотографии."""

    def upload_to(instance, filename):
        return 'plays/{}/{}'.format(instance.play.pk, filename)

    image = models.ImageField(
        'Изображение',
        upload_to=upload_to,
        help_text='Оптимальный размер: 800px*500px.'
    )
    play = models.ForeignKey(Play, on_delete=models.CASCADE, verbose_name='Спектакль')
    is_visible = models.BooleanField('Включено', default=True)

    def __str__(self):
        return 'Изображение #{}'.format(self.pk)

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class PlayVideo(TimeStampedModel):
    """Модель видео спектакля."""
    youtube_id = models.CharField(
        'Идентификатор на Youtube',
        help_text='Например, для видео https://www.youtube.com/watch?v=JMJXvsCLu6, '
                  'его идентификатором будет JMJXvsCLu6.',
        max_length=32
    )
    play = models.ForeignKey(Play, on_delete=models.CASCADE, verbose_name='Спектакль')
    is_visible = models.BooleanField('Включено', default=True)

    def __str__(self):
        return 'Видео #{}'.format(self.pk)

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'


class PersonPlayRole(models.Model):
    """Модель для связи многие-ко-многим моделей Person и Play (роли)."""
    person = models.ForeignKey(Person, verbose_name='Актёр', on_delete=models.CASCADE)
    play = models.ForeignKey(Play, verbose_name='Спектакль', on_delete=models.CASCADE)
    role = models.CharField('Роль', max_length=255)
    text = models.CharField('Краткий текст', max_length=255, null=True, blank=True)

    def __str__(self):
        return 'Роль #{}'.format(self.pk)

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'
