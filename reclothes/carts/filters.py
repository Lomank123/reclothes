from django_filters import rest_framework as filters

from carts.models import CartItem


class CartItemListFilter(filters.FilterSet):

    class Meta:
        model = CartItem
        fields = ['cart']
