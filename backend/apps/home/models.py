from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from backend.abstract_models import TimeStampedModel, SeoModel


class Home(SeoModel, TimeStampedModel):
    """Модель главной страницы."""
    promo_left = models.TextField('Левая часть (HTML)', blank=True, null=True)
    promo_right = models.TextField('Правая часть (HTML)', blank=True, null=True)
    icon1_icon = models.CharField('Иконка', max_length=255)
    icon1_title = models.CharField('Заголовок', max_length=255)
    icon1_text = models.TextField('Текст')
    icon2_icon = models.CharField('Иконка', max_length=255)
    icon2_title = models.CharField('Заголовок', max_length=255)
    icon2_text = models.TextField('Текст')
    icon3_icon = models.CharField('Иконка', max_length=255)
    icon3_title = models.CharField('Заголовок', max_length=255)
    icon3_text = models.TextField('Текст')
    about_title = models.CharField('Заголовок', max_length=255)
    about_text = RichTextUploadingField('Текст')

    def __str__(self):
        return 'Главная страница'

    def get_photos(self):
        """Возвращает фотографии страницы."""
        return self.photo_set.filter(is_visible=True).all()

    class Meta:
        verbose_name = 'Данные страницы'
        verbose_name_plural = 'Данные страницы'


class Photo(TimeStampedModel):
    """Модель фотографии."""

    image = models.ImageField(
        'Изображение',
        upload_to='home',
        help_text='Оптимальный размер: 900px*600px.'
    )
    home = models.ForeignKey(Home, on_delete=models.CASCADE, verbose_name='Главная страница')
    is_visible = models.BooleanField('Включено', default=True)

    def __str__(self):
        return 'Изображение #{}'.format(self.pk)

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
