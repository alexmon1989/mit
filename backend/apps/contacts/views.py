from django.views.generic import FormView
from django.http import Http404, HttpResponse
from .models import Contact
from .forms import ContactForm


class ContactView(FormView):
    """Отображает страницу Контакты."""
    template_name = 'contacts/contacts.html'
    form_class = ContactForm

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return HttpResponse(status=200)

    def form_invalid(self, form):
        response = HttpResponse()
        response.status_code = 400
        return response

    def get_context_data(self, **kwargs):
        context = super(ContactView, self).get_context_data(**kwargs)
        context['page_data'] = Contact.objects.first()
        if not context['page_data']:
            raise Http404("Contact model does not exist.")
        return context
