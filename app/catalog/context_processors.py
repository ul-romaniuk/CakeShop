
from catalog.utils import get_basket


def current_basket(request):
    basket = get_basket(request)
    return {
        'current_basket': basket
    }
