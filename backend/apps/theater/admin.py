from django.contrib import admin
from .models import Play, PlayPhoto, PlayVideo, PlayProperty, PersonPlayRole, Genre, Person, Position


class PlayPhotoInline(admin.TabularInline):
    model = PlayPhoto
    extra = 3


class PlayVideoInline(admin.TabularInline):
    model = PlayVideo
    extra = 3


class PlayPropertyInline(admin.TabularInline):
    model = PlayProperty
    extra = 3


class PlayRoleInline(admin.TabularInline):
    model = PersonPlayRole
    extra = 3


@admin.register(Play)
class PlayAdmin(admin.ModelAdmin):
    """Класс для описания интерфейса администрирования спектакля."""
    list_display = ('title', 'genre', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('title', 'genre', 'duration', 'text')
        }),
        ('SEO опции', {
            'classes': ('collapse',),
            'fields': ('meta_h1', 'meta_title', 'meta_keywords', 'meta_description'),
        }),
    )
    ordering = ('title',)
    search_fields = ('title',)
    list_filter = ('genre',)
    inlines = (PlayPropertyInline, PlayVideoInline, PlayPhotoInline, PlayRoleInline)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Класс для описания интерфейса администрирования спектакля."""
    list_display = ('title', 'created_at', 'updated_at')
    ordering = ('title',)
    search_fields = ('title',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    """Класс для описания интерфейса администрирования сотрудников."""
    list_display = ('name', 'position', 'created_at', 'updated_at')
    ordering = ('name',)
    search_fields = ('name', 'position')
    list_filter = ('position',)


@admin.register(Position)
class PositionsAdmin(admin.ModelAdmin):
    """Класс для описания интерфейса администрирования должностей."""
    list_display = ('title', 'weight', 'created_at', 'updated_at')
    search_fields = ('title',)
    list_editable = ('weight',)
