from carts.serializers import MyOrdersCartItemSerializer
from rest_framework import serializers

from orders.models import Order, OrderItem


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'


class OrderDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'


class MyOrderItemsSerializer(serializers.ModelSerializer):
    cart_item = MyOrdersCartItemSerializer(required=False)

    class Meta:
        model = OrderItem
        fields = '__all__'


class MyOrdersSerializer(serializers.ModelSerializer):
    order_items = MyOrderItemsSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = '__all__'
