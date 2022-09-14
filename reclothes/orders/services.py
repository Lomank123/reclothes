import datetime

from carts.repositories import CartRepository
from carts.utils import CartSessionManager
from django.db import transaction
from payment.models import PaymentTypes
from reclothes.services import APIService

from orders import consts
from orders.repositories import (AddressRepository, OrderItemRepository,
                                 OrderRepository)
from orders.serializers import AddressSerializer, OrderDetailSerializer
from payment.repositories import PaymentRepository


class CreateOrderService(APIService):

    __slots__ = 'request', 'session_manager'

    def __init__(self, request):
        super().__init__()
        self.request = request
        self.session_manager = CartSessionManager(request)

    def _validate_card_data(self, payment_type):
        '''Return errors dict or None if valid.'''
        err = dict()

        if payment_type == PaymentTypes.CASH.value:
            return None

        name = self.request.data.get('card[name]', None)
        if name is None:
            err['name'] = consts.NAME_NOT_FOUND_MSG

        # Date format: MM/YY
        date = self.request.data.get('card[expiry_date]', None)
        date_list = date.split('/')
        if date_list is None:
            err['expiry_date'] = consts.EXPIRY_DATE_NOT_FOUND_MSG
        try:
            date = datetime.date(
                year=int(date_list[1]), month=int(date_list[0]), day=1)
        except ValueError:
            err['expiry_date'] = consts.INVALID_DATE_MSG

        card_number = self.request.data.get('card[number]', None)
        if card_number is None:
            err['number'] = consts.CART_NOT_FOUND_MSG
        elif len(card_number) != consts.CARD_NUMBER_SIZE:
            err['number'] = consts.INVALID_CARD_NUMBER_MSG

        code = self.request.data.get('card[code]', None)
        if code is None:
            err['code'] = consts.CODE_NOT_FOUND_MSG
        elif len(code) != consts.CODE_SIZE:
            err['code'] = consts.INVALID_CODE_MSG

        if err:
            return err
        return None

    def _create_order_with_items(self, cart, address_id):
        # Order
        order_data = {
            'user': cart.user,
            'address_id': address_id,
            'total_price': cart.total_price,
        }
        order = OrderRepository.create(**order_data)

        # Order Items
        for item in cart.cart_items.all():
            OrderItemRepository.create(order=order, cart_item=item)

        return order

    @transaction.atomic
    def execute(self):
        address_id = self.request.data.get('address_id', None)
        if address_id == 'NaN':
            address_id = None
        cart_id = self.session_manager.load_cart_id_from_session()
        # Payment
        payment_type = self.request.data.get('payment_type', None)
        card_errors = self._validate_card_data(payment_type)

        # Error handling
        if payment_type is None:
            self.errors['payment_type'] = consts.PAYMENT_TYPE_NOT_FOUND_MSG
        if card_errors is not None:
            self.errors['card'] = card_errors
        if address_id is None:
            self.errors['address_id'] = consts.ADDRESS_NOT_FOUND_MSG
        if cart_id is None:
            self.errors['cart_id'] = consts.CART_NOT_FOUND_MSG
        if self.errors:
            data = self._build_response_data()
            return self._build_response(data)

        cart = CartRepository.fetch_active(single=True, id=cart_id)
        order = self._create_order_with_items(cart, address_id)
        CartRepository.delete(cart=cart)
        new_cart = CartRepository.create(user=self.request.user)
        self.session_manager.set_cart_id_if_not_exists(
            cart_id=new_cart.pk, forced=True)
        PaymentRepository.create(
            type=payment_type,
            order=order,
            total_price=order.total_price,
        )

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
