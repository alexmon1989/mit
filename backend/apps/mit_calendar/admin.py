from django.contrib import admin
from .models import Event, Spectator, EventPhoto, EventVideo, Place


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
    list_display = ('play', 'date', 'time', 'place', 'registered_spectators_count',
                    'registration_closed', 'is_enabled', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': (
                'play',
                'date',
                'time',
                'place',
                'visitors_count',
                'text',
                'registration_closed',
                'show_full_visitors',
                'is_enabled',
            )
        }),
        ('SEO опции', {
            'classes': ('collapse',),
            'fields': ('meta_h1', 'meta_title', 'meta_keywords', 'meta_description'),
        }),
    )
    ordering = ('-date',)
    search_fields = ('play__title', 'place', 'address')
    list_editable = ('registration_closed', 'is_enabled',)
    inlines = (SpectatorInline, EventPhotoInline, EventVideoInline)

    def registered_spectators_count(self, obj):
        return '{}/{}'.format(len(obj.get_spectators()), obj.visitors_count)

    registered_spectators_count.short_description = 'Зрители'


@admin.register(Place)
class EventAdmin(admin.ModelAdmin):
    """Класс для описания интерфейса администрирования мест проведения спектаклей."""
    list_display = ('title', 'address', 'created_at', 'updated_at')
    search_fields = ('title', 'address')
