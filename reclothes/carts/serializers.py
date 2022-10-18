from catalogue.serializers import MyOrdersProductSerializer
from rest_framework import serializers

from carts.consts import QUANTITY_MAX_ERROR_MSG, QUANTITY_MIN_ERROR_MSG
from carts.models import Cart, CartItem


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ('id', 'items_count', 'total_price')


class CartItemListSerializer(serializers.ModelSerializer):
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


class CartItemDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = '__all__'

    def validate_quantity(self, quantity):
        current_count = self.instance.product.active_keys.count()
        required_count = quantity * self.instance.product.keys_limit
        if required_count > current_count:
            raise serializers.ValidationError(QUANTITY_MAX_ERROR_MSG)
        elif required_count <= 0:
            raise serializers.ValidationError(QUANTITY_MIN_ERROR_MSG)
        return quantity


class CartItemViewSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = '__all__'


class MyOrdersCartItemSerializer(serializers.ModelSerializer):
    product = MyOrdersProductSerializer(required=False)

    class Meta:
        model = CartItem
        fields = '__all__'
