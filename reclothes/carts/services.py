import logging

from django.db.models import F

from catalogue.repositories import ProductImageRepository
from reclothes.services import APIService
from carts.consts import NEW_CART_CREATED_MSG, NEW_CART_ATTACHED_MSG
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
        return CartRepository.fetch_single_active(id=cart_id)

    def _check_or_create_cart(self, session_cart):
        forced = False
        if session_cart is None:
            forced = True
            user = self.session_manager.request.user
            if user.is_authenticated:
                user_cart = CartRepository.fetch_single_active(user_id=user.pk)
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
    def _build_response_data(cart, cart_items):
        data = {}
        if cart is not None:
            cart_serializer = CartSerializer(cart)
            cart_item_serializer = CartItemSerializer(cart_items, many=True)
            complete_data = {
                'cart': cart_serializer.data,
                'cart_items': cart_item_serializer.data,
            }
            data.update(complete_data)
        return data

    @staticmethod
    def _fetch_annotated_cart_items_or_none(cart):
        """Return queryset with annotated product title and feature image."""

        if cart is None:
            return CartItemRepository.empty()

        img_subquery = (
            ProductImageRepository
            .prepare_feature_image_subquery(outer_ref_value="product_id")
        )
        annotate_data = {
            'product_title': F('product__title'),
            'image': img_subquery,
        }
        return CartItemRepository.annotate(
            cart.cart_items, **annotate_data)

    def execute(self):
        cart_id = self.session_manager.get_cart_id()
        cart = CartRepository.fetch_single_active(id=cart_id)
        cart_items = self._fetch_annotated_cart_items_or_none(cart)
        data = self._build_response_data(cart, cart_items)
        return self._build_response(data)


class CartViewSetService:

    def execute(self):
        return CartRepository.fetch_single_active()


class CartItemViewSetService:

    def execute(self):
        return CartItemRepository.fetch()
