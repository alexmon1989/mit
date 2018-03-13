from django.views.generic import TemplateView, DetailView, FormView
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from .models import Event, Place
from .forms import SpectatorForm


class EventListView(TemplateView):
    """Отображает страницу с расписанием мероприятий."""
    template_name = 'mit_calendar/calendar/event_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['places'] = Place.objects.with_future_events()
        context['future_events'] = Event.objects.future().values(
            'pk', 'date', 'time', 'place__title', 'place__address', 'visitors_count'
        ).annotate(Count('spectator'))
        for event in context['future_events']:
            event['spectator__percent'] = int(event['spectator__count'] / event['visitors_count'] * 100)
        context['past_events'] = Event.objects.past()
        context['places'] = Place.objects.with_future_events()
        return context


class EventDetailView(DetailView, FormView):
    """Отображает страницу """
    model = Event
    queryset = Event.objects.enabled()
    form_class = SpectatorForm

    def get_form(self, form_class=None):
        """Создаёт объёкт формы."""
        data = {
            'first_name': self.request.POST.get('first_name'),
            'last_name': self.request.POST.get('last_name'),
            'patronymic_name': self.request.POST.get('patronymic_name'),
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
