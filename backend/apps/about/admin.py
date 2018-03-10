from django.contrib import admin
from singlemodeladmin import SingleModelAdmin
from .models import About, Partner


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    """Класс для описание интерфейса администрирования модели Partner."""
    list_display = ('title', 'is_enabled', 'created_at', 'updated_at')
    ordering = ('title',)
    search_fields = ('title',)
    list_editable = ('is_enabled',)


@admin.register(About)
class AboutAdmin(SingleModelAdmin):
    """Класс для описание интерфейса администрирования модели About."""
    fieldsets = (
        (None, {
            'fields': (
                'article_title',
                'article_text',
                'team_title',
                'team_text',
                'persons',
                'partners',
            )
        }),
        ('SEO опции', {
            'classes': ('collapse',),
            'fields': ('meta_title', 'meta_keywords', 'meta_description'),
        }),
    )


