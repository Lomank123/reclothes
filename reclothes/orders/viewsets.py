from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from orders.serializers import OrderDetailSerializer, OrderSerializer
from orders.services import CreateOrderService, OrderViewSetService


class OrderViewSet(ModelViewSet):
    permission_classes = (AllowAny, )

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return OrderDetailSerializer
        return OrderSerializer

    def get_queryset(self):
        return OrderViewSetService(self.request).execute()

    def create(self, request):
        return CreateOrderService(request).execute()
