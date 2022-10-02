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

    @staticmethod
    def fetch_products_ids(order):
        return order.order_items.values_list('cart_item__product', flat=True)


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
