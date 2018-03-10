from django.views.generic.base import TemplateView
from django.http import Http404
from .models import About


class AboutView(TemplateView):
    """Отображает страницу О нас."""
    template_name = 'about/about.html'

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        context['page_data'] = About.objects.first()
        context['team'] = context['page_data'].persons.order_by('-position__weight').all()
        context['partners'] = context['page_data'].partners.filter(is_enabled=True).all()
        if not context['page_data']:
            raise Http404("About model does not exist.")
        return context
