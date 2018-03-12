from django.contrib import admin
from .models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """Класс для описания интерфейса администрирования событий."""
    list_display = ('title', 'is_enabled', 'publish_date', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': (
                'title',
                'slug',
                'publish_date',
                'image',
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
    search_fields = ('title',)
    list_editable = ('is_enabled',)
    prepopulated_fields = {"slug": ("title",)}

