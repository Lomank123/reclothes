import logging

from catalogue.repositories import ProductImageRepository
from rest_framework import status
from rest_framework.response import Response

from carts import consts
from carts.repositories import CartItemRepository, CartRepository
from carts.serializers import CartItemSerializer, CartSerializer
from carts.utils import CartSessionManager


logger = logging.getLogger('django')


class CartMiddlewareService:

    __slots__ = 'session_manager',

    def __init__(self, request):
        self.session_manager = CartSessionManager(request)

    def _get_or_create_cart_id(self):
        """
        Return cart id if it's in current session. Otherwise create new cart
        and return it's id. Also return flag whether to update session value.
        """
        cart_id = self.session_manager.get_cart_id()
        forced = False
        exists = CartRepository.is_cart_exists_by_id(cart_id)
        if not exists:
            forced = True
            new_cart = CartRepository.create()
            logger.info(consts.NEW_CART_CREATED_MSG)
            # In case user cart is gone
            user = self.session_manager.request.user
            if user.is_authenticated:
                CartRepository.attach_user_to_cart_by_id(new_cart.id, user.id)
                logger.info(consts.NEW_CART_ATTACHED_MSG)
            cart_id = new_cart.id
        return cart_id, forced

    def execute(self):
        cart_id, forced = self._get_or_create_cart_id()
        self.session_manager.set_cart_id_if_not_exists(cart_id, forced=forced)


class CartViewSetService:

    __slots__ = 'session_manager',

    def __init__(self, request):
        self.session_manager = CartSessionManager(request)

    def _build_response_data(self, cart, cart_items):
        cart_serializer = CartSerializer(cart)
        cart_item_serializer = CartItemSerializer(cart_items, many=True)
        return {
            "cart": cart_serializer.data,
            "cart_items": cart_item_serializer.data,
        }

    @staticmethod
    def _build_response(data, is_none):
        response = Response(data=data, status=status.HTTP_200_OK)
        if is_none:
            response.status_code = status.HTTP_404_NOT_FOUND
        return response

    @staticmethod
    def _build_cart_items_qs(cart):
        img_subquery = ProductImageRepository.get_feature_image_by_product_id(
            subquery=True,
            outer_ref_value="product_id"
        )
        cart_items = CartRepository.get_cart_items(cart)
        image_qs = CartItemRepository.attach_feature_image(cart_items, img_subquery)
        return CartItemRepository.attach_product_info(image_qs)

    def execute_get_cart(self):
        cart_id = self.session_manager.get_cart_id()
        data = {}
        if cart_id is not None:
            cart = CartRepository.get_by_id(cart_id)
            cart_items = self._build_cart_items_qs(cart)
            data = self._build_response_data(cart, cart_items)
        return self._build_response(data, cart_id is None)
