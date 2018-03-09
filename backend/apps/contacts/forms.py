from django import forms
from django.core.mail import mail_managers
from django.template import loader


class ContactForm(forms.Form):
    """Класс формы контактов."""
    username = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    subject = forms.CharField(max_length=100, required=False)
    phone = forms.CharField(max_length=100, required=False)
    message = forms.CharField(max_length=2048)

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        html_message = loader.render_to_string(
            'contacts/email/contacts.html',
            {
                'username': self.cleaned_data['username'],
                'phone': self.cleaned_data['phone'],
                'email': self.cleaned_data['email'],
                'subject': self.cleaned_data['subject'],
                'message': self.cleaned_data['message'],
            }
        )
        mail_managers('Сообщение клиента с сайта', '', fail_silently=False, html_message=html_message)
