from django.conf import settings

from catalog.constants import OrderStatusEnum
from catalog.models import Order


def create_basket(request):
    basket_obj = Order.objects.create(phone='-', status=OrderStatusEnum.BASKET)
    request.session.update({settings.CURRENT_BASKET_SESSION_FIELD: basket_obj.pk})
    return basket_obj


def get_basket(request):
    basket_id = request.session.get(settings.CURRENT_BASKET_SESSION_FIELD)
    if basket_id and Order.objects.filter(id=basket_id).exists():
        basket_obj = Order.objects.get(id=basket_id)
        if not basket_obj.status == OrderStatusEnum.BASKET:
            basket_obj = create_basket(request)
    else:
        basket_obj = create_basket(request)

    return basket_obj


