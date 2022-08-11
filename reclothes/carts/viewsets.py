from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from carts.consts import RECENT_CART_ITEMS_LIMIT
from carts.serializers import CartItemSerializer, CartSerializer
from carts.services import (CartItemViewSetService, CartService,
                            CartViewSetService)


class CartViewSet(ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = (AllowAny, )

    def get_queryset(self):
        return CartViewSetService().execute()

    @action(methods=['get'], detail=False)
    def fetch_cart_with_items_from_session(self, request):
        return CartService(request).execute()

    @action(methods=['get'], detail=False, url_path='header')
    def fetch_cart_with_items_for_header(self, request):
        return CartService(request).execute(limit=RECENT_CART_ITEMS_LIMIT)


class CartItemViewSet(ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = (AllowAny, )

    def get_queryset(self):
        return CartItemViewSetService().execute()
