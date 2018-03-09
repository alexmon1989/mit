from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from backend.abstract_models import SeoModel, TimeStampedModel


class Contact(SeoModel, TimeStampedModel):
    """Модель страницы Контакты."""
    text = RichTextUploadingField('Текст', blank=False)

    def __str__(self):
        return 'Страница "Контакты"'

    class Meta:
        verbose_name = 'Данные страницы'
        verbose_name_plural = 'Данные страницы'


class ContactFooter(TimeStampedModel):
    """Модель для контактных данных, отображаемых в шаблоне."""
    CONTACT_TYPES = (
        (1, 'Телефон'),
        (2, 'E-Mail'),
    )

    contact_type = models.PositiveSmallIntegerField('Тип контакта', choices=CONTACT_TYPES)
    value = models.CharField('Значение', max_length=255)
    is_enabled = models.BooleanField('Включено', default=True)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контактные данные в "подвале"'
