from enum import Enum


class OrderStatusEnum(str, Enum):
    BASKET = 'Корзина'
    IN_WORK = 'В роботі'
    DONE = 'Готово'

    @classmethod
    def choices(cls):
        res = tuple([(e.value, e.value) for e in cls])
        return res

