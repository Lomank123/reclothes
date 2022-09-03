from orders.models import Address, Order, OrderItem


class OrderRepository:

    @staticmethod
    def fetch(first=False, limit=None, **kwargs):
        qs = Order.objects.filter(**kwargs)
        if first:
            return qs.first()
        elif limit:
            return qs[:limit]
        return qs


class OrderItemRepository:

    @staticmethod
    def fetch(first=False, limit=None, **kwargs):
        qs = OrderItem.objects.filter(**kwargs)
        if first:
            return qs.first()
        elif limit:
            return qs[:limit]
        return qs


class AddressRepository:

    @staticmethod
    def fetch(first=False, limit=None, **kwargs):
        qs = Address.objects.filter(**kwargs)
        if first:
            return qs.first()
        elif limit:
            return qs[:limit]
        return qs
