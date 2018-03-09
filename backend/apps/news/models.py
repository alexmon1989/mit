from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from backend.abstract_models import TimeStampedModel, SeoModel


class NewsManager(models.Manager):
    def enabled(self):
        """Возвращает новости с is_enabled=True."""
        return super(NewsManager, self).get_queryset().filter(is_enabled=True)


class News(SeoModel, TimeStampedModel):
    """Модель новости."""
    title = models.CharField('Заголовок', max_length=255, blank=False)
    slug = models.SlugField(
        'Slug (для url)',
        max_length=255,
        default='',
        unique=True
    )
    text = RichTextUploadingField('Текст', blank=False)
    is_enabled = models.BooleanField('Включено', default=True)
    image = models.ImageField(
        'Изображение',
        upload_to='news',
        null=True,
        blank=True,
        help_text='Оптимальный размер: 900px*600px.'
    )

    objects = NewsManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news_detail', args=[self.slug])

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ('-created_at',)
