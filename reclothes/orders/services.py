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

    def _validate_card_data(self, card):
        '''Return errors dict or None if valid.'''
        name = card.get('name', None)
        date = card.get('expiry_date', None)    # Date format: MM/YY
        card_number = card.get('number', None)
        code = card.get('code', None)
        err = dict()

        # TODO: Use card[name] if not serializer
        # If data is not full
        if date is None:
            err['expiry_date'] = consts.EXPIRY_DATE_NOT_FOUND_MSG
        if name is None:
            err['name'] = consts.NAME_NOT_FOUND_MSG
        if card_number is None:
            err['number'] = consts.CART_NOT_FOUND_MSG
        if code is None:
            err['code'] = consts.CODE_NOT_FOUND_MSG
        if err:
            return err

        # Additional validation
        try:
            date_list = date.split('/')
            date = datetime.date(
                year=int(date_list[1]), month=int(date_list[0]), day=1)
        except Exception:
            err['expiry_date'] = consts.INVALID_DATE_MSG
        if len(card_number) != consts.CARD_NUMBER_SIZE:
            err['number'] = consts.INVALID_CARD_NUMBER_MSG
        if len(code) != consts.CODE_SIZE:
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
        payment_type = self.request.data.get('payment_type', None)
        cart_id = self.session_manager.load_cart_id_from_session()

        # Card validation
        if payment_type != PaymentTypes.CASH.value:
            card = self.request.data.get('card', dict())
            card_errors = self._validate_card_data(card)
            if card_errors is not None:
                self.errors['card'] = card_errors

        # Error handling
        if payment_type is None:
            self.errors['payment_type'] = consts.PAYMENT_TYPE_NOT_FOUND_MSG
        if address_id is None or address_id == 'NaN':
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

    __slots__ = 'request',

    def __init__(self, request):
        self.request = request

    def _build_filters(self):
        filters = dict()
        if not self.request.user.is_superuser:
            filters['user'] = self.request.user
        return filters

    def execute(self):
        filters = self._build_filters()
        return OrderRepository.fetch(**filters)


class AddressViewSetService:

    def execute(self):
        return AddressRepository.fetch()
