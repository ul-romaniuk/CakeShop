from django.db import models
from django.urls import reverse

from catalog.constants import OrderStatusEnum
from users.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    min_order = models.DecimalField(decimal_places=1, max_digits=10)
    unit = models.CharField(max_length=16) #одиницявиміру
    category = models.ManyToManyField(to=Category, related_name='products')
    is_active = models.BooleanField(default=False)
    image = models.ImageField(upload_to='media/static/img/product/', null=True, blank=True,)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.pk])




class Order(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE,
                             related_name='user')
    phone = models.CharField(max_length=16)
    status = models.CharField(choices=OrderStatusEnum.choices(), null=True, blank=True)

    def __str__(self):
        return f'{self.user}'


class OrderItem(models.Model):
    product = models.ForeignKey(to=Product,  related_name='order_items', on_delete=models.CASCADE)
    quantity = models.FloatField()
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, related_name='items')

