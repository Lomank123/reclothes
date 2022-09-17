import datetime

from carts.repositories import CartRepository
from carts.utils import CartSessionManager
from django.db import transaction
from reclothes.services import APIService

from orders import consts
from orders.repositories import OrderItemRepository, OrderRepository
from orders.serializers import OrderDetailSerializer


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

    def _create_order_with_items(self, cart):
        # Order
        order_data = {
            'user': cart.user,
            'total_price': cart.total_price,
        }
        order = OrderRepository.create(**order_data)
        # Order Items
        for item in cart.cart_items.all():
            OrderItemRepository.create(order=order, cart_item=item)
        return order

    # TODO: Implement this
    def _decrease_product_quantity(self, cart):
        # Decrease only if is_limited set to True!
        pass

    @transaction.atomic
    def execute(self):
        data = self.request.data
        cart_id = self.session_manager.load_cart_id_from_session()
        card = {
            'name': data.get('card[name]'),
            'number': data.get('card[number]'),
            'code': data.get('card[code]'),
            'expiry_date': data.get('card[expiry_date]'),
        }
        card_errors = self._validate_card_data(card)

        # Error handling
        if card_errors is not None:
            self.errors['card'] = card_errors
        if cart_id is None:
            self.errors['cart_id'] = consts.CART_NOT_FOUND_MSG
        if self.errors:
            data = self._build_response_data()
            return self._build_response(data)

        cart = CartRepository.fetch_active(single=True, id=cart_id)
        order = self._create_order_with_items(cart)
        CartRepository.delete(cart=cart)
        new_cart = CartRepository.create(user=self.request.user)
        self.session_manager.set_cart_id_if_not_exists(
            cart_id=new_cart.pk, forced=True)
        self._decrease_product_quantity(cart)

        # Response
        serialized_order_data = OrderDetailSerializer(order).data
        data = self._build_response_data(**serialized_order_data)
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
