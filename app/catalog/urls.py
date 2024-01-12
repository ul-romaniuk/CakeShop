from django.urls import path

from catalog.views import CatalogView, ProductDetailView, AddToCartView, ApplyOrderView

urlpatterns = [
    path('catalog/', CatalogView.as_view(), name='product_catalog'),
    path('catalog/product/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('catalog/product/add_to_cart/', AddToCartView.as_view(), name='product_add_to_cart'),

    path('order/<int:pk>', ApplyOrderView.as_view(), name='apply_order'),

]
