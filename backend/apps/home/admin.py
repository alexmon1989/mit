from django.contrib import admin
from singlemodeladmin import SingleModelAdmin
from .models import Home, Photo


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 3


@admin.register(Home)
class HomeAdmin(SingleModelAdmin):
    """Класс для описания интерфейса администрирования событий."""
    fieldsets = (
        ('Промоблок', {
            'fields': (
                'promo_left', 'promo_right'
            )
        }),
        ('Иконка 1', {
            'fields': (
                'icon1_icon', 'icon1_title', 'icon1_text'
            )
        }),
        ('Иконка 2', {
            'fields': (
                'icon2_icon', 'icon2_title', 'icon2_text'
            )
        }),
        ('Иконка 3', {
            'fields': (
                'icon3_icon', 'icon3_title', 'icon3_text'
            )
        }),
        ('О нас', {
            'fields': (
                'about_title', 'about_text',
            )
        }),
        ('SEO опции', {
            'classes': ('collapse',),
            'fields': ('meta_h1', 'meta_title', 'meta_keywords', 'meta_description'),
        }),
    )
    inlines = (PhotoInline, )
