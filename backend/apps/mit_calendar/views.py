from django.views.generic import ListView
from .models import Event


class EventListView(ListView):
    """Отображает страницу с расписанием мероприятий."""
    model = Event
    template_name = 'mit_calendar/calendar/event_list.html'
    queryset = Event.objects.enabled()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['future_events_count'] = Event.get_future_events_count()
        context['past_events_count'] = Event.get_past_events_count()
        return context
