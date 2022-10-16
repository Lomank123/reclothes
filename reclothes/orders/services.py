import json

from carts.models import Cart
from carts.repositories import CartRepository
from carts.utils import CartSessionManager
from catalogue.repositories import OneTimeUrlRepository, ProductRepository
from catalogue.serializers import DownloadProductSerializer
from catalogue.utils import valid_uuid
from django.db import transaction
from rest_framework import status
from django.http.response import (FileResponse, HttpResponseBadRequest,
                                  HttpResponseNotFound)
from django.shortcuts import get_object_or_404
from reclothes.services import APIService
from carts.exceptions import BadRequest

from orders.models import Order
from orders.repositories import OrderItemRepository, OrderRepository
from orders.serializers import CardSerializer, OrderDetailSerializer
from orders.consts import NOT_ENOUGH_KEYS_MSG


class CreateOrderService(APIService):

    __slots__ = 'request', 'session_manager'

    def __init__(self, request):
        self.request = request
        self.session_manager = CartSessionManager(request)

    def _create_order_items(self, cart, order):
        cart_items = cart.cart_items.select_related('product')
        for item in cart_items:
            limit = item.product.keys_limit * item.quantity
            keys = item.product.active_keys[:limit]

            if len(keys) < limit:
                raise BadRequest(detail=NOT_ENOUGH_KEYS_MSG)

            for key in keys:
                key.order = order
                key.save()
            OrderItemRepository.create(order=order, cart_item=item)

    @transaction.atomic
    def execute(self):
        data = self.request.data

        # Credit card validation
        card_data = json.loads(data.get('card'))
        card_serializer = CardSerializer(data=card_data)
        card_serializer.is_valid(raise_exception=True)

        # Cart validation
        cart_id = self.session_manager.load_cart_id_from_session()
        cart = get_object_or_404(Cart, id=cart_id)

        # Order with keys and items
        order = OrderRepository.create(
            user=cart.user, total_price=cart.total_price)
        self._create_order_items(cart, order)

        CartRepository.delete(cart=cart)
        new_cart = CartRepository.create(user=self.request.user)
        self.session_manager.set_cart_id_if_not_exists(
            cart_id=new_cart.pk, forced=True)

        # Response
        serializer = OrderDetailSerializer(order)
        data = self._build_response_data(**serializer.data)
        return self._build_response(data, status_code=status.HTTP_201_CREATED)


class OrderFileService(APIService):

    def __init__(self, request, order_id):
        self.request = request
        self.order_id = order_id

    def execute(self):
        order = get_object_or_404(Order, id=self.order_id)
        products_ids = OrderRepository.fetch_products_ids(order)
        products = ProductRepository.fetch_by_ids_with_files_and_keys(
            products_ids)
        serializer = DownloadProductSerializer(
            products, many=True, context={'order_id': self.order_id})
        order_serializer = OrderDetailSerializer(order)
        data = self._build_response_data(
            products=serializer.data, order=order_serializer.data)
        return self._build_response(data=data)


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

        url.delete()

        return FileResponse(url.file.file, as_attachment=True)
