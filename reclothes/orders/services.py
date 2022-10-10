import datetime

from carts.repositories import CartRepository
from carts.utils import CartSessionManager
from catalogue.repositories import OneTimeUrlRepository, ProductRepository
from catalogue.serializers import DownloadProductSerializer
from catalogue.utils import valid_uuid
from django.db import transaction
from django.http.response import (FileResponse, HttpResponseBadRequest,
                                  HttpResponseNotFound)
from reclothes.services import APIService
from rest_framework import status
from rest_framework.response import Response

from orders import consts
from orders.repositories import OrderItemRepository, OrderRepository
from orders.serializers import OrderDetailSerializer


# TODO: Should return 201 when create
class CreateOrderService(APIService):

    __slots__ = 'request', 'session_manager'

    def __init__(self, request):
        super().__init__()
        self.request = request
        self.session_manager = CartSessionManager(request)

    def _validate_card_data(self, card):
        """Return errors dict or None if valid."""
        name = card.get('name', None)
        date = card.get('expiry_date', None)    # Date format: MM/YY
        card_number = card.get('number', None)
        code = card.get('code', None)
        err = dict()

        # If data is not full
        if date is None:
            err['expiry_date'] = consts.EXPIRY_DATE_NOT_FOUND_MSG
        if name is None or name == '':
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

    def _create_order(self, cart):
        """Create order with items and add activation keys to it."""
        order_data = {
            'user': cart.user,
            'total_price': cart.total_price,
        }
        order = OrderRepository.create(**order_data)
        items = cart.cart_items.select_related('product')

        for item in items:
            limit = item.product.keys_limit * item.quantity
            keys = item.product.active_keys[:limit]

            if len(keys) < limit and item.product.is_limited:
                raise ValueError('Not enough keys.')

            for key in keys:
                key.order = order
                key.save()
            OrderItemRepository.create(order=order, cart_item=item)
        return order

    @transaction.atomic
    def execute(self):
        data = self.request.data
        cart_id = self.session_manager.load_cart_id_from_session()
        card_1 = {
            'name': data.get('card[name]'),
            'number': data.get('card[number]'),
            'code': data.get('card[code]'),
            'expiry_date': data.get('card[expiry_date]'),
        }
        card = data.get('card', card_1)
        card_errors = self._validate_card_data(card)

        # Error handling
        if card_errors is not None:
            self.errors['card'] = card_errors
        if cart_id is None:
            self.errors['cart_id'] = consts.CART_NOT_FOUND_MSG
        if self.errors:
            data = self._build_response_data()
            return self._build_response(data)

        cart = CartRepository.fetch_active(first=True, id=cart_id)

        # https://docs.djangoproject.com/en/4.1/topics/db/transactions/#controlling-transactions-explicitly
        try:
            with transaction.atomic():
                order = self._create_order(cart)
        except ValueError as e:
            self.errors['order'] = str(e)
            data = self._build_response_data()
            return self._build_response(data)

        CartRepository.delete(cart=cart)
        new_cart = CartRepository.create(user=self.request.user)
        self.session_manager.set_cart_id_if_not_exists(
            cart_id=new_cart.pk, forced=True)

        # Response
        serialized_order_data = OrderDetailSerializer(order).data
        data = self._build_response_data(**serialized_order_data)
        return self._build_response(data)


class OrderViewSetService:

    __slots__ = 'request',

    def __init__(self, request):
        self.request = request

    def execute(self):
        filters = {'user': self.request.user}
        return OrderRepository.fetch(**filters)


class OrderFileService(APIService):

    def __init__(self, request, order_id):
        super().__init__()
        self.request = request
        self.order_id = order_id

    def _validate_order(self, order):
        status_code = status.HTTP_200_OK
        if order is None:
            self.errors['order'] = consts.ORDER_NOT_FOUND_MSG
            status_code = status.HTTP_404_NOT_FOUND
        else:
            # Check if user owns the order
            if not order.user == self.request.user:
                self.errors['order'] = consts.NOT_ORDER_OWNER_MSG
                status_code = status.HTTP_403_FORBIDDEN
        return status_code

    def _build_response(self, data, status_code):
        return Response(data=data, status=status_code)

    def execute(self):
        order = OrderRepository.fetch(first=True, id=self.order_id)
        status_code = self._validate_order(order)

        # Error handling
        if status_code != status.HTTP_200_OK:
            data = self._build_response_data()
            return self._build_response(data, status_code)

        products_ids = OrderRepository.fetch_products_ids(order)
        products = ProductRepository.fetch_by_ids_with_files_and_keys(
            products_ids)
        serializer = DownloadProductSerializer(
            products, many=True, context={'order_id': self.order_id})
        order_serializer = OrderDetailSerializer(order)
        data = self._build_response_data(
            products=serializer.data, order=order_serializer.data)
        return self._build_response(data, status_code=status_code)


class DownloadFileService:

    def __init__(self, url_token):
        self.url_token = url_token

    def execute(self):
        if not valid_uuid(self.url_token):
            return HttpResponseBadRequest(content='Invalid token.')

        url = OneTimeUrlRepository.fetch(url_token=self.url_token).first()

        if url is None:
            return HttpResponseNotFound(content='Token not found.')
        if url.is_used:
            return HttpResponseBadRequest(content='Already in use.')

        OneTimeUrlRepository.delete(url)

        return FileResponse(url.file.file, as_attachment=True)
