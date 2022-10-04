from catalogue.serializers import MyOrdersProductSerializer
from rest_framework import serializers

from carts.models import Cart, CartItem


class CartSerializer(serializers.ModelSerializer):
    items_count = serializers.IntegerField()

    class Meta:
        model = Cart
        fields = ('id', 'items_count', 'total_price')


class CartItemSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(required=False)
    product_is_limited = serializers.IntegerField(required=False)
    image = serializers.CharField(required=False)

    class Meta:
        depth = 1
        model = CartItem
        fields = (
            'id',
            'quantity',
            'image',
            'product_id',
            'product_title',
            'product_is_limited',
            'total_price',
        )


class CartItemViewSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = '__all__'


class MyOrdersCartItemSerializer(serializers.ModelSerializer):
    product = MyOrdersProductSerializer(required=False)

    class Meta:
        model = CartItem
        fields = '__all__'
