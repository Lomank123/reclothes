from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from carts import serializers
from carts.models import Cart, CartItem
from carts.services import CartService


class CartViewSet(ModelViewSet):
    serializer_class = serializers.CartSerializer
    permission_classes = (AllowAny, )

    def get_queryset(self):
        qs = Cart.objects.filter(is_archived=False, is_deleted=False)
        return qs

    @action(methods=["get"], detail=False)
    def get_cart_from_session(self, request):
        return CartService(request).execute()


class CartItemViewSet(ModelViewSet):
    serializer_class = serializers.CartItemSerializer
    permission_classes = (AllowAny, )

    def get_queryset(self):
        qs = CartItem.objects.all()
        return qs
