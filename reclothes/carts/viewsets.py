from catalogue.pagination import DefaultCustomPagination
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from carts.permissions import IsCartInSession
from carts.serializers import CartItemViewSetSerializer, CartSerializer
from carts.services import (CartItemViewSetService, CartService,
                            CartViewSetService, ChangeQuantityService)


class CartViewSet(ModelViewSet):
    serializer_class = CartSerializer

    def get_permissions(self):
        if self.action == 'current':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return CartViewSetService().execute()

    @action(methods=['get'], detail=False)
    def current(self, request):
        return CartService(request).execute()


class CartItemViewSet(ModelViewSet):
    serializer_class = CartItemViewSetSerializer
    permission_classes = (IsCartInSession, )
    pagination_class = DefaultCustomPagination

    def get_queryset(self):
        return CartItemViewSetService().execute()

    @action(methods=['patch'], detail=False)
    def change_quantity(self, request):
        return ChangeQuantityService(request).execute()
