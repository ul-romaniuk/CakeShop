from django.db.models import F, Q
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView
from django.views.generic.list import ListView

from catalog.forms import CatalogProductsSearchForm
from catalog.models import Product, Category


class CatalogView(ListView):
    model = Product
    template_name = 'shop.html'
    paginate_by = 8

    def filtered_queryset(self, qs):

        search_value = self.request.GET.get('search')
        if search_value:
            qs = qs.filter(
                    Q(name__icontains=search_value) | Q(description__icontains=search_value)
            )

        ordering = self.request.GET.get('ordering')
        if ordering:
            if ordering == 'price_up':
                qs = qs.order_by('price', '-id')
            if ordering == 'price_down':
                qs = qs.order_by('-price', '-id')
            if ordering == 'name':
                qs = qs.order_by('name', '-id')

        category = self.request.GET.get('category')
        if category == 'cakes':
            qs = qs.filter(category__name='Торти')
        if category == 'cupcakes':
            qs = qs.filter(category__name='Капкейки')
        if category == 'zefir':
            qs = qs.filter(category__name='Зефір')

        return qs

    def base_queryset(self):
        return self.model.objects.all()

    def get_queryset(self):
        filtered_queryset = self.filtered_queryset(self.base_queryset())
        return filtered_queryset

    def get_ordering_name(self):
        ordering = self.request.GET.get('ordering', '')
        values = {
            'name': 'Назва',
            'price_up': 'Ціна вверх',
            'price_down': 'Ціна вниз',
        }
        return values.get(ordering)

    def get_category_name(self):
        category = self.request.GET.get('category', '')
        values = {
            'cakes': 'Торти',
            'cupcakes': 'Капкейки',
            'zefir': 'Зефір',
        }
        return values.get(category)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        search_form = CatalogProductsSearchForm(self.request.GET)
        page_obj = context.get('page_obj')

        if page_obj is not None:
            page_obj_start = page_obj.number * self.paginate_by - self.paginate_by + 1
            page_obj_end = page_obj.number * self.paginate_by
            page_obj_end = page_obj_end if page_obj_end <= self.get_queryset().count() else self.get_queryset().count()
            page_obj_count_string = f'{page_obj_start} - {page_obj_end} of {self.get_queryset().count()}'
        else:
            page_obj_count_string = "No page information available."

        context.update({
            'title': 'Catalog',
            'search_form': search_form,
            'products': self.get_queryset(),
            'page_obj': page_obj,
            'page_obj_count_string': page_obj_count_string,
            'ordering_name': self.get_ordering_name(),
            'category_name': self.get_category_name(),
            'menu_key': 'product_catalog'

        })
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop-details.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        product = self.get_object()
        # print(product.category.all().values_list('name', flat=True))
        categories = Category.objects.all().values_list('name', flat=True)
        related_products = Product.objects.exclude(pk=product.pk).filter(category__in=product.category.all()).distinct()

        context.update({
            'title': 'Product Details',
            'categories': categories,
            'related_products': related_products,

        })
        return context






