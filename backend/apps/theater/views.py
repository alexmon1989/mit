from django.views.generic import DetailView
from django.http import Http404
from .models import Play


class PlayDetailView(DetailView):
    """Отображает страницу со спектаклем."""
    model = Play
    template_name = 'theater/plays/detail/detail.html'

    def get_object(self):
        play = Play.objects.first()
        if not play:
            raise Http404('Отсутствуют спектали в БД.')
        return play
