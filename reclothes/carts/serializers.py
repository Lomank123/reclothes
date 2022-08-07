from rest_framework import serializers

from carts.models import Cart, CartItem


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ('id', )


class CartItemSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField()
    image = serializers.CharField()

    class Meta:
        depth = 1
        model = CartItem
        fields = ('id', 'quantity', 'image', 'product_id', 'product_title')
