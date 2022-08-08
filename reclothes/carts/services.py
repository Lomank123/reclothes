import logging

from django.db.models import Subquery, F

from catalogue.repositories import ProductImageRepository
from reclothes.services import APIService
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
        exists = CartRepository.get_filtered_queryset(id=cart_id).exists()
        if not exists:
            forced = True
            new_cart = CartRepository.create()
            logger.info(consts.NEW_CART_CREATED_MSG)
            # In case user cart is gone
            user = self.session_manager.request.user
            if user.is_authenticated:
                cart = CartRepository.fetch_active(id=new_cart.pk)
                CartRepository.attach_user_to_cart(cart, user.pk)
                logger.info(consts.NEW_CART_ATTACHED_MSG)
            cart_id = new_cart.pk
        return cart_id, forced

    def execute(self):
        cart_id, forced = self._get_or_create_cart_id()
        self.session_manager.set_cart_id_if_not_exists(cart_id, forced=forced)


class CartService(APIService):

    __slots__ = 'session_manager',

    def __init__(self, request):
        self.session_manager = CartSessionManager(request)

    @staticmethod
    def _get_response_data(cart, cart_items):
        data = {}
        if cart is not None:
            serializer = CartSerializer(cart)
            data["cart"] = serializer.data
        if cart_items.exists():
            serializer = CartItemSerializer(cart_items, many=True)
            data["cart_items"] = serializer.data
        return data

    @staticmethod
    def _get_cart_items(cart):
        """Return queryset with annotated product title and feature image."""

        if cart is None:
            return CartItemRepository.empty()

        img_subquery = ProductImageRepository.get_feature_image_by_product_id(
            subquery=True, outer_ref_value="product_id")
        annotate_data = {
            'product_title': F('product__title'),
            'image': Subquery(img_subquery),
        }
        return CartItemRepository.annotate(
            cart.cart_items, **annotate_data)

    def execute(self):
        cart_id = self.session_manager.get_cart_id()
        cart = CartRepository.fetch_active(id=cart_id)
        cart_items = self._get_cart_items(cart)
        data = self._get_response_data(cart, cart_items)
        return self._get_response(data)


class CartViewSetService:

    def execute(self):
        return CartRepository.get_filtered_queryset(
            is_archived=False, is_deleted=False)


class CartItemViewSetService:

    def execute(self):
        return CartItemRepository.get_filtered_queryset()
