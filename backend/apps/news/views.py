from django.views.generic import DetailView
from .models import News


class NewsDetailView(DetailView):
    """Отображает страницу новости."""
    model = News
    queryset = News.objects.enabled()
    template_name = 'news/detail/news_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['last_news'] = News.objects.enabled().exclude(pk=self.object.pk)[:10]
        return context
