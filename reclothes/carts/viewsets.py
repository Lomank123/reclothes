from catalogue.pagination import DefaultCustomPagination
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from carts.consts import RECENT_CART_ITEMS_LIMIT
from carts.serializers import CartItemSerializer, CartSerializer
from carts.services import (CartItemService, CartItemViewSetService,
                            CartService, CartViewSetService,
                            ChangeQuantityService)


class CartViewSet(ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = (AllowAny, )

    def get_queryset(self):
        return CartViewSetService().execute()

    @action(methods=['get'], detail=False, url_path='session_cart')
    def load_cart_from_session(self, request):
        return CartService(request).execute()


class CartItemViewSet(ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = (AllowAny, )
    pagination_class = DefaultCustomPagination

    @action(methods=['get'], detail=False, url_path='all_by_cart')
    def load_all_items_by_cart(self, request):
        return CartItemService(self).execute(
            cart_id=request.GET.get('cart_id'), paginate=True)

    @action(methods=['get'], detail=False, url_path='header')
    def load_header_items(self, request):
        return CartItemService(self).execute(
            cart_id=request.GET.get('cart_id'), limit=RECENT_CART_ITEMS_LIMIT)

    @action(methods=['post'], detail=False)
    def change_quantity(self, request):
        return ChangeQuantityService(request).execute()

    def get_queryset(self):
        return CartItemViewSetService().execute()
