from carts.serializers import OrderCartItemDetailSerializer
from rest_framework import serializers

from orders.models import Order, OrderItem


class OrderListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'


class CreateOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'


class OrderItemDetailSerializer(serializers.ModelSerializer):
    cart_item = OrderCartItemDetailSerializer(required=False)

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderDetailSerializer(serializers.ModelSerializer):
    order_items = OrderItemDetailSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = '__all__'
