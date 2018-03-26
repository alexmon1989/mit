from django.views.generic import DetailView
from django.http import Http404
from django.db.models import Count
from .models import Play
from apps.mit_calendar.models import Event


class PlayDetailView(DetailView):
    """Отображает страницу со спектаклем."""
    model = Play
    template_name = 'theater/plays/detail/detail.html'

    def get_object(self):
        play = Play.objects.first()
        if not play:
            raise Http404('Отсутствуют спектали в БД.')
        return play

    def get_context_data(self, **kwargs):
        context = super(PlayDetailView, self).get_context_data(**kwargs)

        context['future_events'] = Event.objects.future().values(
            'pk', 'date', 'time', 'place__title', 'place__address', 'visitors_count', 'registration_closed',
            'show_full_visitors'
        ).annotate(Count('spectator')).filter(play=self.object)
        for event in context['future_events']:
            event['spectator__percent'] = int(event['spectator__count'] / event['visitors_count'] * 100)

        context['roles'] = self.object.personplayrole_set.values('person__image', 'person__name', 'role', 'text').all()

        return context
