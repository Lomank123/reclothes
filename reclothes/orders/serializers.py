from rest_framework import serializers

from orders.models import City, Order, OrderItem


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = '__all__'


class OrderDetailSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = '__all__'
