from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from django.utils import timezone
from backend.abstract_models import TimeStampedModel, SeoModel


class NewsManager(models.Manager):
    def published(self):
        """Возвращает новости с is_enabled=True."""
        return super(NewsManager, self).get_queryset().filter(is_enabled=True, publish_date__lte=timezone.now())


class News(SeoModel, TimeStampedModel):
    """Модель новости."""
    title = models.CharField('Заголовок', max_length=255, blank=False)
    slug = models.SlugField(
        'Slug (для url)',
        max_length=255,
        default='',
        unique=True,
        db_index=True
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
    publish_date = models.DateTimeField('Дата и время публикации', default=timezone.now)

    objects = NewsManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news_detail', args=[self.slug])

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ('-publish_date',)
