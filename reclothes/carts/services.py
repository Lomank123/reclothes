import logging

from catalogue.models import Product
from catalogue.pagination import DefaultCustomPagination
from catalogue.repositories import ProductImageRepository
from django.db.models import F
from django.shortcuts import get_object_or_404
from reclothes.services import APIService

from carts.consts import (NEW_CART_ATTACHED_MSG, NEW_CART_CREATED_MSG,
                          QUANTITY_MAX_ERROR_MSG, QUANTITY_MIN_ERROR_MSG)
from carts.exceptions import BadRequest
from carts.models import Cart, CartItem
from carts.repositories import CartItemRepository, CartRepository
from carts.serializers import CartItemSerializer, CartSerializer
from carts.utils import CartSessionManager

logger = logging.getLogger('django')


class CartMiddlewareService:

    __slots__ = 'session_manager',

    def __init__(self, request):
        self.session_manager = CartSessionManager(request)

    def _fetch_session_cart(self):
        cart_id = self.session_manager.load_cart_id_from_session()
        return CartRepository.fetch_active(first=True, id=cart_id)

    def _check_or_create_cart(self, session_cart):
        forced = False
        if session_cart is None:
            forced = True
            user = self.session_manager.request.user
            if user.is_authenticated:
                user_cart = CartRepository.fetch_active(
                    first=True, user_id=user.pk)
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
    """
    Return cart data which id is in current session.

    Query params:
    - 'items=true' to add cart items as well
    - 'paginate=true' to paginate cart items
    """

    __slots__ = 'request', 'session_manager'

    def __init__(self, request):
        super().__init__()
        self.request = request
        self.session_manager = CartSessionManager(request)

    def _serialize_cart_items(self, items):
        is_paginate = self.request.GET.get('paginate', False)
        if is_paginate:
            paginator = DefaultCustomPagination()
            page = paginator.paginate_queryset(items, request=self.request)
            if page is not None:
                serializer = CartItemSerializer(page, many=True)
                return paginator.get_paginated_data(serializer.data)
        serializer = CartItemSerializer(items, many=True)
        return serializer.data

    @staticmethod
    def _annotate_product_with_image(cart_items):
        """Return queryset with annotated product title and feature image."""

        if len(cart_items) == 0:
            return cart_items

        img_subquery = (
            ProductImageRepository
            .prepare_feature_image_subquery(outer_ref='product_id')
        )
        annotate_data = {
            'product_title': F('product__title'),
            'product_is_limited': F('product__keys_limit'),
            'image': img_subquery,
        }
        return cart_items.annotate(**annotate_data)

    def execute(self):
        # Serialize cart
        cart_id = self.session_manager.load_cart_id_from_session()
        cart = get_object_or_404(Cart, id=cart_id)
        raw_data = {'cart': CartSerializer(cart).data}
        # Cart items are optional
        is_items = self.request.GET.get('items', False)
        if is_items:
            cart_items = self._annotate_product_with_image(
                cart.cart_items.all())
            serialized_items = self._serialize_cart_items(cart_items)
            raw_data['cart_items'] = serialized_items
        # Build response
        data = self._build_response_data(**raw_data)
        return self._build_response(data=data)


# TODO: This can be rewritten as a Serializer with custom validation
class ChangeQuantityService(APIService):

    __slots__ = 'request'

    def __init__(self, request):
        super().__init__()
        self.request = request

    @staticmethod
    def _validate(required_count, current_count):
        if required_count > current_count:
            raise BadRequest(detail=QUANTITY_MAX_ERROR_MSG)
        elif required_count <= 0:
            raise BadRequest(detail=QUANTITY_MIN_ERROR_MSG)
        return True

    def execute(self):
        # Initial data
        product_id = self.request.POST['product_id']
        cart_item_id = self.request.POST['cart_item_id']
        product = get_object_or_404(Product, id=product_id)
        cart_item = get_object_or_404(CartItem, id=cart_item_id)
        # Change quantity
        new_quantity = int(self.request.POST['value'])
        current_count = product.active_keys.count()
        required_count = new_quantity * product.keys_limit
        self._validate(required_count, current_count)
        CartItemRepository.change_quantity(cart_item, new_quantity)
        # Build response
        data = self._build_response_data(value=new_quantity)
        return self._build_response(data)


class CartViewSetService:

    def execute(self):
        return CartRepository.fetch_active()


class CartItemViewSetService:

    def execute(self):
        return CartItemRepository.fetch()
