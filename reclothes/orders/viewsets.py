from catalogue.pagination import DefaultCustomPagination
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from orders.serializers import OrderDetailSerializer, OrderSerializer
from orders.services import (CreateOrderService, OrderFileService,
                             OrderViewSetService)


class OrderViewSet(ModelViewSet):
    permission_classes = (AllowAny, )
    pagination_class = DefaultCustomPagination

    def get_permissions(self):
        # TODO: In future you may let users to update order status
        UNSAFE_ACTIONS = ['destroy', 'update', 'partial_update']

        if self.action in UNSAFE_ACTIONS:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

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
