from django.db.models import F, Q
from django.shortcuts import render
from django.views.generic.list import ListView

from catalog.forms import CatalogProductsSearchForm
from catalog.models import Product, Category


class CatalogView(ListView):
    model = Product
    template_name = 'shop.html'
    paginate_by = 8

    # def filtered_queryset(self, qs):
    #
    #     search_value = self.request.GET.get('search')
    #     if search_value:
    #         qs = qs.filter(
    #                 Q(name__icontains=search_value) | Q(description__icontains=search_value)
    #         )
    #
    #     ordering = self.request.GET.get('ordering')
    #     desc = True if self.request.GET.get('ordering_type') == 'Desc' else False
    #     if ordering:
    #         if 'price' in ordering:
    #             qs = qs.order_by('price', '-id')
    #         else:
    #             qs = qs.order_by('-price', '-id')
    #     else:
    #         if desc:
    #             qs = qs.order_by(F(ordering).desc(nulls_last=True), '-id')
    #         else:
    #             qs = qs.order_by(F(ordering).asc(nulls_last=True), '-id')
    #     return qs
    #
    # def base_queryset(self):
    #     return self.model.objects.all()
    #
    # def get_queryset(self):
    #     filtered_queryset = self.filtered_queryset(self.base_queryset())
    #     return filtered_queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        search_form = CatalogProductsSearchForm(self.request.GET)
        products = self.model.objects.all()
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
            'products': products,
            'page_obj': page_obj,
            'page_obj_count_string': page_obj_count_string,

        })
        print(page_obj)
        return context

