from django.urls import path

from users.views import HomeView, ContactView

urlpatterns = [
    path('home/', HomeView.as_view(), name='home_page'),
    path('contact/', ContactView.as_view(), name='contact'),

]
