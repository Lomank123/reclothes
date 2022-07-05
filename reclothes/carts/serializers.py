from rest_framework import serializers

from carts import models


class CartSerializer(serializers.ModelSerializer):
    cart_items_count = serializers.IntegerField()

    class Meta:
        model = models.Cart
        fields = ('id', 'cart_items_count',)


class CartItemSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField()
    image = serializers.CharField()

    class Meta:
        depth = 1
        model = models.CartItem
        fields = ('id', 'quantity', 'image', 'product_id', 'product_title',)
