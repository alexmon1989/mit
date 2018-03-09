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


class SocialLinksModel(models.Model):
    """Модель ссылок на соц. сети."""
    fb = models.URLField('Facebook', max_length=255, null=True, blank=True)
    vk = models.URLField('Вконтакте', max_length=255, null=True, blank=True)
    instagram = models.URLField('Instagram', max_length=255, null=True, blank=True)
    ok = models.URLField('Одноклассники', max_length=255, null=True, blank=True)
    twitter = models.URLField('Twitter', max_length=255, null=True, blank=True)
    youtube = models.URLField('Youtube', max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Ссылки на соц. сети'
        verbose_name_plural = 'Ссылки на соц. сети'
