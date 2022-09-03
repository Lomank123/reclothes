from orders.repositories import (AddressRepository, OrderItemRepository,
                                 OrderRepository)
from reclothes.services import APIService
from orders.serializers import AddressSerializer


class LoadByUserCityService(APIService):

    __slots__ = 'request',

    def __init__(self, request):
        super().__init__()
        self.request = request

    def _build_response_data(self, addresses):
        data = {'addresses': addresses}
        return super()._build_response_data(**data)

    def execute(self):
        city_id = self.request.user.city.pk
        addresses = AddressRepository.fetch(**{'city_id': city_id})
        serialized_addresses = AddressSerializer(addresses, many=True).data
        data = self._build_response_data(serialized_addresses)
        return self._build_response(data)


class OrderViewSetService:

    def execute(self):
        return OrderRepository.fetch()


class OrderItemViewSetService:

    def execute(self):
        return OrderItemRepository.fetch()


class AddressViewSetService:

    def execute(self):
        return AddressRepository.fetch()
