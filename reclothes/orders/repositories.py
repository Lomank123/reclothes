from orders.models import Order, OrderItem


class OrderRepository:

    @staticmethod
    def fetch(first=False, limit=None, **kwargs):
        qs = Order.objects.filter(**kwargs)
        if first:
            return qs.first()
        elif limit:
            return qs[:limit]
        return qs

    @staticmethod
    def create(**kwargs):
        return Order.objects.create(**kwargs)


class OrderItemRepository:

    @staticmethod
    def fetch(first=False, limit=None, **kwargs):
        qs = OrderItem.objects.filter(**kwargs)
        if first:
            return qs.first()
        elif limit:
            return qs[:limit]
        return qs

    @staticmethod
    def create(**kwargs):
        return OrderItem.objects.create(**kwargs)
