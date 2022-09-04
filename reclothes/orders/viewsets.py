from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from orders.serializers import (AddressSerializer, OrderDetailSerializer,
                                OrderItemSerializer, OrderSerializer)
from orders.services import (AddressViewSetService, LoadByUserCityService,
                             OrderItemViewSetService, OrderViewSetService)


class OrderViewSet(ModelViewSet):
    permission_classes = (AllowAny, )

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderDetailSerializer
        return OrderSerializer

    def get_queryset(self):
        return OrderViewSetService().execute()

    def create(self, request):
        # TODO: Create order with items here
        return Response(data={}, status=200)


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

    @action(methods=['get'], detail=False, url_path='user_city')
    def load_by_user_city(self, request):
        return LoadByUserCityService(request).execute()
