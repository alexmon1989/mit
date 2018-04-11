from django.http import JsonResponse, Http404
from django.views.generic.base import TemplateView
from django.views.generic import DetailView
from django.db.models import Count
from easy_thumbnails.files import get_thumbnailer
from .models import Like, Page
from apps.mit_calendar.models import Event, EventPhoto
from .utils import get_client_ip


class GalleryListView(TemplateView):
    """Отображает страницу Фотоархив."""
    template_name = 'photo_archive/list/photo_archive.html'

    def get_context_data(self, **kwargs):
        context = super(GalleryListView, self).get_context_data(**kwargs)
        context['page_data'] = Page.objects.first()
        if not context['page_data']:
            raise Http404("Page model does not exist.")
        context['events'] = Event.objects.past().values(
            'pk', 'date', 'time', 'place__title'
        )
        context['no_photo'] = True
        for event in context['events']:
            event['photo'] = EventPhoto.objects.filter(is_visible=True, event_id=event['pk']).first()
            if context['no_photo'] and event['photo']:
                context['no_photo'] = False
        return context


class GalleryDetailView(DetailView):
    """Отображает страницу галереи мероприятия в разделе Фотоархив"""
    model = Event
    queryset = Event.objects.past()
    template_name = 'photo_archive/detail/gallery.html'


def photos(request):
    """Возвращает JSON со всеми фотографиями со спектаклей."""
    try:
        event_id = int(request.GET.get('event_id'))
    except (ValueError, TypeError):
        return JsonResponse({'error': 1}, status=400)
    photos_list = EventPhoto.objects.filter(
        for_archive=True,
        is_visible=True,
        event_id=event_id
    ).values('id', 'image').annotate(Count('like'))
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
    """Обрабатывает запрос на лайк фотографии."""
    photo = EventPhoto.objects.filter(
        is_visible=True,
        pk=request.POST.get('id')
    ).exclude(like__ip=get_client_ip(request)).first()

    if not photo:
        return JsonResponse({'error': 1}, status=400)

    Like.objects.create(ip=get_client_ip(request), photo=photo)
    return JsonResponse({'success': 1})
