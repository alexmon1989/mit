from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from backend.abstract_models import SeoModel, TimeStampedModel
from apps.theater.models import Person


class Partner(TimeStampedModel):
    """Модель партнёра проекта."""
    title = models.CharField('Название', max_length=255)
    image = models.ImageField(
        'Изображение',
        upload_to='partners',
        help_text='Оптимальный размер: 200px*100px.'
    )
    is_enabled = models.BooleanField('Включено', default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Партнёр проекта'
        verbose_name_plural = 'Партнёры проекта'


class About(SeoModel, TimeStampedModel):
    """Модель страницы Контакты."""
    article_title = models.CharField('Заголовок блока статьи', max_length=255)
    article_text = RichTextUploadingField('Текст блока статьи', blank=False)
    team_title = models.CharField('Заголовок блока команды', max_length=255)
    team_text = models.TextField('Текст блока команды', blank=True, null=True)
    persons = models.ManyToManyField(Person, verbose_name='Команда проекта')
    partners = models.ManyToManyField(Partner, verbose_name='Партнёры проекта')

    def __str__(self):
        return 'Страница "О нас"'

    class Meta:
        verbose_name = 'Данные страницы'
        verbose_name_plural = 'Данные страницы'
