from django.urls import path

from users.views import HomeView

urlpatterns = [
    path('home/', HomeView.as_view(), name='home_page'),
]
