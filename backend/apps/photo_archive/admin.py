from django.contrib import admin
from singlemodeladmin import SingleModelAdmin
from .models import Page


@admin.register(Page)
class PhotoArchiveAdmin(SingleModelAdmin):
    """Класс для описание интерфейса администрирования страницы Фотоархив."""
    fieldsets = (
        (None, {
            'fields': (
                'title',
                'text',
            )
        }),
        ('SEO опции', {
            'classes': ('collapse',),
            'fields': ('meta_h1', 'meta_title', 'meta_keywords', 'meta_description'),
        }),
    )
