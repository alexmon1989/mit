from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Класс для описания интерфейса администрирования событий."""
    list_display = ('play', 'date', 'time', 'place', 'address', 'is_enabled', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    search_fields = ('play__title', 'place', 'address')
    list_editable = ('is_enabled',)
