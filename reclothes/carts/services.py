import logging

from catalogue.pagination import DefaultCustomPagination
from catalogue.repositories import ProductImageRepository, ProductRepository
from django.db.models import F
from reclothes.services import APIService
from rest_framework import status
from rest_framework.response import Response

from carts.consts import (INVALID_QUANTITY_ERROR_MSG, NEW_CART_ATTACHED_MSG,
                          NEW_CART_CREATED_MSG)
from carts.repositories import CartItemRepository, CartRepository
from carts.serializers import CartItemSerializer, CartSerializer
from carts.utils import CartSessionManager


logger = logging.getLogger('django')


class CartMiddlewareService:

    __slots__ = 'session_manager',

    def __init__(self, request):
        self.session_manager = CartSessionManager(request)

    def _fetch_session_cart(self):
        cart_id = self.session_manager.get_cart_id()
        return CartRepository.fetch_active(single=True, id=cart_id)

    def _check_or_create_cart(self, session_cart):
        forced = False
        if session_cart is None:
            forced = True
            user = self.session_manager.request.user
            if user.is_authenticated:
                user_cart = CartRepository.fetch_active(
                    single=True, user_id=user.pk)
                if user_cart is None:
                    new_user_cart = CartRepository.create(user_id=user.pk)
                    cart = new_user_cart
                    logger.info(NEW_CART_ATTACHED_MSG)
                else:
                    cart = user_cart
            else:
                new_cart = CartRepository.create()
                cart = new_cart
                logger.info(NEW_CART_CREATED_MSG)
        else:
            cart = session_cart
        return cart, forced

    def execute(self):
        session_cart = self._fetch_session_cart()
        cart, forced = self._check_or_create_cart(session_cart)
        self.session_manager.set_cart_id_if_not_exists(cart.pk, forced=forced)


class CartService(APIService):

    __slots__ = 'session_manager',

    def __init__(self, request):
        self.session_manager = CartSessionManager(request)

    @staticmethod
    def _build_response_data(cart):
        data = {}
        if cart is not None:
            cart_serializer = CartSerializer(cart)
            complete_data = {
                'cart': cart_serializer.data,
            }
            data.update(complete_data)
        return data

    def execute(self, limit=None):
        cart_id = self.session_manager.get_cart_id()
        cart = CartRepository.fetch_active(single=True, id=cart_id)
        data = self._build_response_data(cart)
        return self._build_response(data)


class CartItemService(APIService):

    __slots__ = 'request',

    def __init__(self, request):
        self.request = request

    def _build_response_data(self, items):
        return {'cart_items': items}

    def _serialize_data(self, items, paginate=False):
        if paginate:
            paginator = DefaultCustomPagination()
            page = paginator.paginate_queryset(items, request=self.request)
            if page is not None:
                serializer = CartItemSerializer(page, many=True)
                return paginator.get_paginated_data(serializer.data)
        serializer = CartItemSerializer(items, many=True)
        return serializer.data

    @staticmethod
    def _annotate_product_with_image(qs):
        """Return queryset with annotated product title and feature image."""

        if len(qs) == 0:
            return qs

        img_subquery = (
            ProductImageRepository
            .prepare_feature_image_subquery(outer_ref_value="product_id")
        )
        annotate_data = {
            'product_title': F('product__title'),
            'image': img_subquery,
        }
        return CartItemRepository.annotate(qs, **annotate_data)

    def execute(self, cart_id=None, paginate=False, limit=None):
        qs = CartItemRepository.fetch(limit=limit, cart_id=cart_id)
        annotated_qs = self._annotate_product_with_image(qs=qs)
        serialized_data = self._serialize_data(annotated_qs, paginate=paginate)
        data = self._build_response_data(items=serialized_data)
        return self._build_response(data)


class ChangeQuantityService(APIService):

    __slots__ = 'request'

    def __init__(self, request):
        self.request = request

    def _change_quantity(self, cart_item, product_quantity):
        new_quantity = int(self.request.POST['value'])
        if 0 < new_quantity <= product_quantity:
            CartItemRepository.change_quantity(cart_item, new_quantity)
            return new_quantity
        else:
            return -1

    def _build_response_data(self, quantity):
        return {'value': quantity}

    @staticmethod
    def _build_response(data):
        response = Response(data=data, status=status.HTTP_200_OK)
        if data['value'] < 0:
            response.status_code = status.HTTP_400_BAD_REQUEST
            response.data = {'msg': INVALID_QUANTITY_ERROR_MSG}
        return response

    def execute(self):
        product_id = self.request.POST['product_id']
        product = ProductRepository.fetch(single=True, id=product_id)
        cart_item_id = self.request.POST['cart_item_id']
        cart_item = CartItemRepository.fetch(single=True, id=cart_item_id)
        result = self._change_quantity(cart_item, product.quantity)
        data = self._build_response_data(result)
        return self._build_response(data)


class CartViewSetService:

    def execute(self):
        return CartRepository.fetch_active()


class CartItemViewSetService:

    def execute(self):
        return CartItemRepository.fetch()
