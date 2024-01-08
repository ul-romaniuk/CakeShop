from django.shortcuts import render
from django.views.generic.list import ListView

from users.models import Feedback


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
