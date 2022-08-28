from orders.repositories import (CityRepository, OrderItemRepository,
                                 OrderRepository)


class OrderViewSetService:

    def execute(self):
        return OrderRepository.fetch()


class OrderItemViewSetService:

    def execute(self):
        return OrderItemRepository.fetch()


class CityViewSetService:

    def execute(self):
        return CityRepository.fetch()
