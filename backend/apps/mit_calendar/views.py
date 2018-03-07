from django.views.generic import ListView, DetailView
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


class EventDetailView(DetailView):
    """Отображает страницу """
    model = Event
    queryset = Event.objects.enabled()

    def get_template_names(self):
        """Возвращает путь к шаблону в зависимости от того прошло ли уже мероприятие."""
        if self.object.is_past_due:
            return ['mit_calendar/event_detail/past/event_detail.html']
        return ['mit_calendar/event_detail/future/event_detail.html']
