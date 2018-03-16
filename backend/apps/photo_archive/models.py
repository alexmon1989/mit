from django.db import models
from apps.mit_calendar.models import EventPhoto
from ckeditor_uploader.fields import RichTextUploadingField
from backend.abstract_models import TimeStampedModel, SeoModel


class Like(TimeStampedModel):
    """Модель лайка фото."""
    photo = models.ForeignKey(EventPhoto, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField('IP адрес лайкнувшего')


class Page(SeoModel, TimeStampedModel):
    """Модель страницы Контакты."""
    title = models.CharField('Заголовок', max_length=255, blank=True, null=True)
    text = RichTextUploadingField('Текст', blank=False)

    def __str__(self):
        return 'Страница "Фотоархив"'

    class Meta:
        verbose_name = 'Данные страницы'
        verbose_name_plural = 'Данные страницы'
