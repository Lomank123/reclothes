from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from orders.serializers import (AddressSerializer, OrderDetailSerializer,
                                OrderItemSerializer, OrderSerializer)
from orders.services import (AddressViewSetService, OrderItemViewSetService,
                             OrderViewSetService)


class OrderViewSet(ModelViewSet):
    permission_classes = (AllowAny, )

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderDetailSerializer
        return OrderSerializer

    def get_queryset(self):
        return OrderViewSetService().execute()


class OrderItemViewSet(ModelViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = (AllowAny, )

    def get_queryset(self):
        return OrderItemViewSetService().execute()


class AddressViewSet(ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = (AllowAny, )

    def get_queryset(self):
        return AddressViewSetService().execute()
