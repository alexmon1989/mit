from django.contrib import sitemaps
from django.urls import reverse
from apps.news.models import News
from apps.mit_calendar.models import Event


class StaticViewSitemap(sitemaps.Sitemap):
    """Карта сайта для стат. страниц."""
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['home', 'about', 'contacts', 'play', 'calendar_event_list', 'photo_archive']

    def location(self, item):
        return reverse(item)


class EventSitemap(sitemaps.Sitemap):
    """Карта сайта для новостей."""
    changefreq = 'daily'
    priority = 0.8

    def items(self):
        return Event.objects.enabled()

    def lastmod(self, obj):
        return obj.updated_at


class NewsSitemap(sitemaps.Sitemap):
    """Карта сайта для новостей."""
    changefreq = 'daily'
    priority = 0.6

    def items(self):
        return News.objects.published()

    def lastmod(self, obj):
        return obj.updated_at


class GallerySitemap(sitemaps.Sitemap):
    """Карта сайта для галерей."""
    changefreq = 'daily'
    priority = 0.6

    def items(self):
        return Event.objects.past()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('photo_archive_gallery', args=(obj.pk,))
