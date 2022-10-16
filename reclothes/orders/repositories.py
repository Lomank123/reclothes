from reclothes.repositories import BaseRepository

from orders.models import Order, OrderItem


class OrderRepository(BaseRepository):

    def __init__(self):
        super().__init__(Order)


class OrderItemRepository(BaseRepository):

    def __init__(self):
        super().__init__(OrderItem)
