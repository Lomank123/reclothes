from rest_framework import serializers

from carts import models


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Cart
        fields = ('id',)


class CartItemSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField()
    image = serializers.CharField()

    class Meta:
        depth = 1
        model = models.CartItem
        fields = ('id', 'quantity', 'image', 'product_id', 'product_title')
