from orders.repositories import (AddressRepository, OrderItemRepository,
                                 OrderRepository)


class OrderViewSetService:

    def execute(self):
        return OrderRepository.fetch()


class OrderItemViewSetService:

    def execute(self):
        return OrderItemRepository.fetch()


class AddressViewSetService:

    def execute(self):
        return AddressRepository.fetch()
