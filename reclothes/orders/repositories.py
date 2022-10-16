from reclothes.repositories import BaseRepository

from orders.models import Order, OrderItem


class OrderRepository(BaseRepository):

    def __init__(self):
        super().__init__(Order)

    @staticmethod
    def fetch_products_ids(order):
        return order.order_items.values_list('cart_item__product', flat=True)


class OrderItemRepository(BaseRepository):

    def __init__(self):
        super().__init__(OrderItem)
