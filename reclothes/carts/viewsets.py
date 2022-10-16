from catalogue.pagination import DefaultCustomPagination
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from carts.models import Cart, CartItem
from carts.permissions import IsCartInSession
from carts.serializers import CartItemViewSetSerializer, CartSerializer
from carts.services import CartService, ChangeQuantityService


class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_permissions(self):
        if self.action == 'current':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(methods=['get'], detail=False)
    def current(self, request):
        return CartService(request).execute()


class CartItemViewSet(ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemViewSetSerializer
    permission_classes = (IsCartInSession, )
    pagination_class = DefaultCustomPagination

    @action(methods=['patch'], detail=False)
    def change_quantity(self, request):
        return ChangeQuantityService(request).execute()
