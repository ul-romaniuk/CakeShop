from django.db import models
from django.db.models import Sum, F
from django.urls import reverse

from catalog.constants import OrderStatusEnum


class Category(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    min_order = models.DecimalField(decimal_places=1, max_digits=10)
    unit = models.CharField(max_length=16)
    category = models.ManyToManyField(to=Category, related_name='products')
    is_active = models.BooleanField(default=False)
    image = models.ImageField(upload_to='media/static/img/product/', null=True, blank=True,)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.pk])


class Order(models.Model):
    phone = models.CharField(max_length=16)
    status = models.CharField(choices=OrderStatusEnum.choices(), null=True, blank=True)

    def calc_price(self):
        total_price = (self.items.all()
                       .aggregate(total_price=Sum(F('product__price') * F('quantity'))).get('total_price') or 0.00)

        return round(float(total_price), 2)

    def get_count_product(self):
        count_product = self.items.all().count()
        return count_product

    def to_work(self):
        self.status = OrderStatusEnum.IN_WORK
        self.save()

    def get_absolute_url(self):
        return reverse('apply_order', args=[self.pk])

    def __str__(self):
        return f'{self.phone}'


class OrderItem(models.Model):
    product = models.ForeignKey(to=Product,  related_name='order_items', on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=1)
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, related_name='items')

    @property
    def calc_total_product_price(self):
        total_product_price = self.product.price * self.quantity
        return round(total_product_price, 2)



