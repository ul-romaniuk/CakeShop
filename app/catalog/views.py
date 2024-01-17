from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from catalog.constants import OrderStatusEnum
from catalog.forms import CatalogProductsSearchForm, AddToCartForm, ApplyOrderForm
from catalog.models import Product, Category, Order, OrderItem
from catalog.utils import get_basket


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
            'title': 'Каталог',
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
        categories = Category.objects.all().values_list('name', flat=True)
        related_products = Product.objects.exclude(pk=product.pk).filter(category__in=product.category.all()).distinct()
        title = product.name

        add_form = AddToCartForm(initial={
            'product': product,
            'order': get_basket(self.request),
        })

        context.update({
            'title': title,
            'categories': categories,
            'related_products': related_products,
            'add_form': add_form,


        })
        return context


class AddToCartView(CreateView):
    form_class = AddToCartForm
    success_url = reverse_lazy('product_catalog')


class ApplyOrderView(DetailView, UpdateView):
    model = Order
    fields = ['phone', 'status']
    template_name = 'shoping-cart.html'
    success_url = reverse_lazy('home_page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        order = self.get_object()

        form = ApplyOrderForm(initial={
            'status': OrderStatusEnum.IN_WORK.value,
        })

        context.update({
            'title': 'Корзина',
            'order': order,
            'form': form,
        })
        return context


class OrderItemDeleteView(DetailView):
    model = OrderItem
    template_name = 'shoping-cart.html'

    def get(self, request, *args, **kwargs):
        basket = get_basket(self.request)
        self.get_object().delete()
        return redirect(reverse_lazy('apply_order', kwargs={'pk': basket.pk}))
