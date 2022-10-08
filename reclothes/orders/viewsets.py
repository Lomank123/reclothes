from catalogue.pagination import DefaultCustomPagination
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from orders.serializers import OrderDetailSerializer, OrderSerializer
from orders.services import (CreateOrderService, MyOrdersService,
                             OrderFileService, OrderViewSetService)


class OrderViewSet(ModelViewSet):
    permission_classes = (AllowAny, )
    pagination_class = DefaultCustomPagination

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return OrderDetailSerializer
        return OrderSerializer

    def get_queryset(self):
        return OrderViewSetService(self.request).execute()

    def create(self, request):
        return CreateOrderService(request).execute()

    @action(methods=['get'], detail=False, url_path=r'files/(?P<pk>[0-9]+)')
    def files(self, request, pk):
        return OrderFileService(request, order_id=pk).execute()

    @action(methods=['get'], detail=False)
    def my_orders(self, request):
        return MyOrdersService(request).execute()
