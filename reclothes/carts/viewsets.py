from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from carts.serializers import CartSerializer, CartItemSerializer
from carts.services import CartService, CartItemViewSetService, \
    CartViewSetService


class CartViewSet(ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = (AllowAny, )

    def get_queryset(self):
        return CartViewSetService().execute()

    @action(methods=['get'], detail=False)
    def fetch_from_session(self, request):
        return CartService(request).execute()


class CartItemViewSet(ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = (AllowAny, )

    def get_queryset(self):
        return CartItemViewSetService().execute()
