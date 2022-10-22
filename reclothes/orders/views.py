from catalogue.models import OneTimeUrl
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import FileResponse
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView, View
from reclothes.pagination import DefaultCustomPagination
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (CreateModelMixin, ListModelMixin,
                                   RetrieveModelMixin)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from orders.models import Order
from orders.serializers import (CreateOrderSerializer, OrderDetailSerializer,
                                OrderListSerializer)
from orders.services import CreateOrderService


class OrderView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/order.html'


class MyOrdersView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/my_orders.html'


class OrderDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/order_detail.html'

    def get(self, request, pk, **kwargs):
        return super().get(request, order_id=pk, **kwargs)


class DownloadFileView(LoginRequiredMixin, View):
    """Delete used url and download file."""

    def get(self, request, url_token):
        url = get_object_or_404(
            OneTimeUrl.objects.active(), url_token=url_token)
        url.delete()
        return FileResponse(url.file.file, as_attachment=True)


class OrderListAPIView(ListModelMixin, CreateModelMixin, GenericAPIView):
    permission_classes = (IsAuthenticated, )
    pagination_class = DefaultCustomPagination

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        return OrderListSerializer

    def get(self, request, *args, **kwargs):
        # Paginated user orders list
        return self.list(request, *args, **kwargs)

    def post(self, request):
        order = CreateOrderService(request).execute()
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderDetailAPIView(RetrieveModelMixin, GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = OrderDetailSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
