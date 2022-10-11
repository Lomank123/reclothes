from catalogue.pagination import DefaultCustomPagination
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from carts.permissions import IsCartInSession
from carts.serializers import CartItemViewSetSerializer, CartSerializer
from carts.services import (CartItemService, CartItemViewSetService,
                            CartService, CartViewSetService,
                            ChangeQuantityService)


class CartViewSet(ModelViewSet):
    serializer_class = CartSerializer

    def get_permissions(self):
        ALLOW_ANY_ACTIONS = ['load_cart_from_session']
        SESSION_CART_ACTIONS = ['retrieve']

        if self.action in ALLOW_ANY_ACTIONS:
            permission_classes = [AllowAny]
        elif self.action in SESSION_CART_ACTIONS:
            permission_classes = [IsCartInSession]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return CartViewSetService().execute()

    @action(methods=['get'], detail=False, url_path='session_cart')
    def load_cart_from_session(self, request):
        return CartService(request).execute()


class CartItemViewSet(ModelViewSet):
    serializer_class = CartItemViewSetSerializer
    permission_classes = (IsCartInSession, )
    pagination_class = DefaultCustomPagination

    def get_queryset(self):
        return CartItemViewSetService().execute()

    @action(methods=['get'], detail=False, url_path='all_by_cart')
    def load_all_items_by_cart(self, request):
        return CartItemService(request).execute(paginate=True)

    @action(methods=['get'], detail=False, url_path='header')
    def load_header_items(self, request):
        return CartItemService(request).execute()

    @action(methods=['patch'], detail=False)
    def change_quantity(self, request):
        return ChangeQuantityService(request).execute()
