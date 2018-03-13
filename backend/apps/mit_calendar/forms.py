from django.forms import ModelForm, forms
from django.core.mail import mail_managers, send_mail
from django.conf import settings
from django.template import loader
from .models import Spectator


class SpectatorForm(ModelForm):
    """Класс формы регистрации посетителя."""
    def send_email_spectator(self):
        """Отправляет email зарегистрированному клиенту."""
        html_message = loader.render_to_string(
            'mit_calendar/event_detail/future/emails/spectator.html',
            {
                'event': self.cleaned_data['event'],
                'first_name': self.cleaned_data['first_name'],
                'last_name': self.cleaned_data['last_name'],
                'patronymic_name': self.cleaned_data['patronymic_name'],
                'phone': self.cleaned_data['phone'],
                'email': self.cleaned_data['email'],
            }
        )
        send_mail(
            subject='Регистрация зрителя',
            message='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.cleaned_data['email']],
            fail_silently=False,
            html_message=html_message)

    def send_email_manager(self):
        """Отправляет email менеджерам сайта."""
        html_message = loader.render_to_string(
            'mit_calendar/event_detail/future/emails/manager.html',
            {
                'event': self.cleaned_data['event'],
                'first_name': self.cleaned_data['first_name'],
                'last_name': self.cleaned_data['last_name'],
                'patronymic_name': self.cleaned_data['patronymic_name'],
                'phone': self.cleaned_data['phone'],
                'email': self.cleaned_data['email'],
            }
        )
        mail_managers('Регистрация зрителя', '', fail_silently=False, html_message=html_message)

    def clean(self):
        """Проверка есть ли свободные места для зриетлей."""
        cleaned_data = super().clean()
        event = cleaned_data.get('event')
        if len(event.get_spectators()) >= event.visitors_count:
            raise forms.ValidationError("Свободных мест для зрителей не осталось.")

    class Meta:
        model = Spectator
        fields = ('event', 'first_name', 'last_name', 'patronymic_name', 'phone', 'email')
