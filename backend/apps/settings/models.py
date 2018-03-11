from django.db import models


class Setting(models.Model):
    """Модель настроек сайта."""
    key = models.CharField('Ключ', max_length=255)
    value = models.TextField('Значение')

    def __str__(self):
        return self.key

    class Meta:
        verbose_name = 'Настройка'
        verbose_name_plural = 'Настройки'
