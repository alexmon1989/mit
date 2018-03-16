from django.http import JsonResponse, Http404
from django.views.generic.base import TemplateView
from django.db.models import Count
from easy_thumbnails.files import get_thumbnailer
from apps.mit_calendar.models import EventPhoto
from .models import Like, Page
from .utils import get_client_ip


class PageView(TemplateView):
    """Отображает страницу Фотоархив."""
    template_name = 'photo_archive/photo_archive.html'

    def get_context_data(self, **kwargs):
        context = super(PageView, self).get_context_data(**kwargs)
        context['page_data'] = Page.objects.first()
        if not context['page_data']:
            raise Http404("Page model does not exist.")
        return context


def photos(request):
    """Возвращает JSON со всеми фотографиями со спектаклей."""
    photos_list = EventPhoto.objects.filter(is_visible=True).values('id', 'image').annotate(Count('like'))
    liked_ids = Like.objects.filter(ip=get_client_ip(request)).values_list('photo_id', flat=True)
    data = []
    for photo in photos_list:
        data.append({
            'id': photo['id'],
            'img_sm': get_thumbnailer(photo['image'])['play_sm'].url,
            'img_lg': get_thumbnailer(photo['image'])['play_lg'].url,
            'likes_count': photo['like__count'],
            'can_like': photo['id'] not in liked_ids
        })
    return JsonResponse(data, safe=False)


def like(request):
    pass
