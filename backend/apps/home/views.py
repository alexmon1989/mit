from django.views.generic.base import TemplateView
from django.http import Http404
from .models import Home
from apps.mit_calendar.models import Event, Place
from apps.news.models import News


class HomeView(TemplateView):
    """Отображает главную страницу."""
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['page_data'] = Home.objects.first()
        context['places'] = Place.objects.with_future_events()
        context['last_news'] = News.objects.enabled()[:3]
        if not context['page_data']:
            raise Http404("Home model does not exist.")
        return context
