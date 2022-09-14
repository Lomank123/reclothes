from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from orders.serializers import (AddressSerializer, OrderDetailSerializer,
                                OrderSerializer)
from orders.services import (AddressViewSetService, CreateOrderService,
                             LoadAddressesService, OrderViewSetService)


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


class AddressViewSet(ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = (AllowAny, )

    def get_queryset(self):
        return AddressViewSetService().execute()

    @action(methods=['get'], detail=False, url_path='user_city')
    def load_by_user_city(self, request):
        return LoadAddressesService(request).execute()
