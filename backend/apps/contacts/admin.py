from django.contrib import admin
from singlemodeladmin import SingleModelAdmin
from .models import Contact, ContactFooter


class ContactsAdmin(SingleModelAdmin):
    """Класс для описание интерфейса администрирования модели Contact."""
    fieldsets = (
        (None, {
            'fields': ('text',)
        }),
        ('SEO опции', {
            'classes': ('collapse',),
            'fields': ('meta_title', 'meta_keywords', 'meta_description'),
        }),
    )


admin.site.register(Contact, ContactsAdmin)
admin.site.register(ContactFooter, admin.ModelAdmin)
