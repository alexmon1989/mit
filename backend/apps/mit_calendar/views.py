from django.views.generic import ListView, DetailView, FormView
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Event
from .forms import SpectatorForm


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


class EventDetailView(DetailView, FormView):
    """Отображает страницу """
    model = Event
    queryset = Event.objects.enabled()
    form_class = SpectatorForm

    def get_form(self, form_class=None):
        """Создаёт объёкт формы."""
        data = {
            'username': self.request.POST.get('username'),
            'phone': self.request.POST.get('phone'),
            'email': self.request.POST.get('email'),
            'event': self.kwargs.get('pk'),
        }

        return SpectatorForm(data)

    def form_valid(self, form):
        """Обрабатывает запрос если валидация успешна и возвращает код 200."""
        form.save()
        form.send_email_spectator()
        form.send_email_manager()
        return HttpResponse(status=200)

    def form_invalid(self, form):
        """Обрабатывает запрос если валидация неуспешна и возвращает код 400."""
        return HttpResponse(status=400)

    def get_template_names(self):
        """Возвращает путь к шаблону в зависимости от того прошло ли уже мероприятие."""
        if self.object.is_past_due:
            return ['mit_calendar/event_detail/past/event_detail.html']
        return ['mit_calendar/event_detail/future/event_detail.html']


def show_spectators(request, pk):
    """Отображает список зарегистрированных посетителей мероприятия."""
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'mit_calendar/event_detail/future/spectators_list.html', {'event': event})
