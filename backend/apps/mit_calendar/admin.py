from django.contrib import admin
from .models import Event, Spectator, EventPhoto, EventVideo


class EventPhotoInline(admin.TabularInline):
    model = EventPhoto
    extra = 3


class EventVideoInline(admin.TabularInline):
    model = EventVideo
    extra = 3


class SpectatorInline(admin.TabularInline):
    model = Spectator
    extra = 3


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Класс для описания интерфейса администрирования событий."""
    list_display = ('play', 'date', 'time', 'place', 'address', 'is_enabled', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': (
                'play',
                'date',
                'time',
                'place',
                'address',
                'latitude',
                'longitude',
                'color',
                'visitors_count',
                'text',
                'is_enabled',
            )
        }),
        ('SEO опции', {
            'classes': ('collapse',),
            'fields': ('meta_h1', 'meta_title', 'meta_keywords', 'meta_description'),
        }),
    )
    ordering = ('-created_at',)
    search_fields = ('play__title', 'place', 'address')
    list_editable = ('is_enabled',)
    inlines = (SpectatorInline, EventPhotoInline, EventVideoInline)
