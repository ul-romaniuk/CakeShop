from django.urls import path
from django.urls import path

from catalog.views import CatalogView

urlpatterns = [
    path('catalog/', CatalogView.as_view(), name='product_catalog'),
]
