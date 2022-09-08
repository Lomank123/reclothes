from carts.repositories import CartRepository
from carts.utils import CartSessionManager
from django.db import transaction
from reclothes.services import APIService

from orders.consts import ADDRESS_NOT_FOUND_MSG, CART_NOT_FOUND_MSG
from orders.repositories import (AddressRepository, OrderItemRepository,
                                 OrderRepository)
from orders.serializers import AddressSerializer, OrderDetailSerializer


class CreateOrderService(APIService):

    __slots__ = 'request', 'session_manager'

    def __init__(self, request):
        super().__init__()
        self.request = request
        self.session_manager = CartSessionManager(request)

    def _create_order_with_items(self, cart, address_id):
        # Order
        order_data = {
            'user': cart.user,
            'address_id': address_id,
            'total_price': cart.total_price,
        }
        order = OrderRepository.create(**order_data)

        # Order Items
        for item in cart.cart_items:
            OrderItemRepository.create(order=order, cart_item=item)

        return order

    @transaction.atomic
    def execute(self):
        # TODO: Add Payment choice here
        address_id = self.request.data.get('address_id', None)
        cart_id = self.session_manager.load_cart_id_from_session()

        # Error handling
        if address_id is None:
            self.errors['address_id'] = ADDRESS_NOT_FOUND_MSG
        if cart_id is None:
            self.errors['cart_id'] = CART_NOT_FOUND_MSG
        if self.errors:
            return self._build_response(dict())

        cart = CartRepository.fetch_active(single=True, id=cart_id)
        order = self._create_order_with_items(cart, address_id)
        CartRepository.delete(cart=cart)
        new_cart = CartRepository.create(user=self.request.user)
        self.session_manager.set_cart_id_if_not_exists(
            cart_id=new_cart.pk, forced=True)

        # Response
        serialized_order_data = OrderDetailSerializer(order).data
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
