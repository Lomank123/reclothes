from carts.utils import CartSessionManager
from django.db import transaction
from reclothes.services import APIService

from orders.repositories import (AddressRepository, OrderItemRepository,
                                 OrderRepository)
from orders.serializers import AddressSerializer, OrderDetailSerializer
from carts.repositories import CartRepository


class CreateOrderService(APIService):

    __slots__ = 'request', 'session_manager'

    def __init__(self, request):
        super().__init__()
        self.request = request
        self.session_manager = CartSessionManager(request)

    def _create_order_with_items(self, cart, address_id):
        cart_items = cart.cart_items

    def _remove_old_cart(self, old_cart):
        '''Mark old_cart as deleted and remove it from session.'''
        pass

    def _create_and_attach_new_cart(self):
        '''Create new cart, attach to user and add to session.'''
        user = self.request.user

    @transaction.atomic
    def execute(self):
        # TODO: Add Payment choice here
        address_id = self.request.data['address_id']
        cart_id = self.session_manager.load_cart_id_from_session()
        cart = CartRepository.fetch_active(single=True, id=cart_id)
        order = self._create_order_with_items(cart, address_id)
        serialized_order_data = OrderDetailSerializer(order).data

        # Cart manupulations
        self._remove_old_cart(cart)
        self._create_and_attach_new_cart()

        # Response
        data = self._build_response_data(**serialized_order_data)
        return self._build_response(data)


class LoadAddressesService(APIService):

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
