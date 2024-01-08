from django.urls import path
from django.urls import path

from catalog.views import CatalogView, ProductDetailView

urlpatterns = [
    path('catalog/', CatalogView.as_view(), name='product_catalog'),
    path('catalog/product/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
]
