from django.forms import HiddenInput
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.list import ListView

from users.forms import CreateMessageForm
from users.models import Feedback, Contact


class HomeView(ListView):
    model = Feedback
    template_name = 'home.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        feedbacks = self.model.objects.all()
        context_data = {
            'title': 'Cake Shop',
            'feedbacks': feedbacks,
            'menu_key': 'home_page'
        }

        return context_data


class ContactView(CreateView):
    model = Contact
    template_name = 'contact.html'
    form_class = CreateMessageForm
    success_url = reverse_lazy('contact')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        objects = self.model.objects.all()

        context.update({
            'title': "Зв'язок з нами",
            'objects': objects,
            'menu_key': 'contact'

        })
        return context

