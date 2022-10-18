from django.views.generic.base import TemplateView
from django_filters.rest_framework import DjangoFilterBackend
from reclothes.pagination import DefaultCustomPagination
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from carts.filters import CartItemListFilter
from carts.models import CartItem
from carts.selectors import CurrentCartSelector
from carts.serializers import (CartItemDetailSerializer,
                               CartItemListSerializer, CartSerializer)


class CartView(TemplateView):
    template_name = 'carts/cart.html'


class CurrentCartView(APIView):
    """Fetch current session cart."""

    permission_classes = (AllowAny, )

    def get(self, request):
        selector = CurrentCartSelector(request)
        cart = selector.select()
        serializer = CartSerializer(cart)
        return Response(data=serializer.data)


class CartItemListView(GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = CartItemListSerializer
    pagination_class = DefaultCustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = CartItemListFilter

    def get_queryset(self):
        return CartItem.objects.available(self.request)

    def _prepare_data(self, queryset):
        # Pagination
        is_paginate = self.request.GET.get('paginate', False)
        if is_paginate:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.paginator.get_paginated_data(serializer.data)
        return self.get_serializer(queryset, many=True).data

    def get(self, request):
        initial_queryset = self.filter_queryset(self.get_queryset())
        ready_queryset = initial_queryset.annotate_product_with_image()
        data = self._prepare_data(ready_queryset)
        return Response(data)

    # TODO: Add post method (When adding new item to cart)


class CartItemDetailView(UpdateModelMixin, GenericAPIView):
    serializer_class = CartItemDetailSerializer

    def get_queryset(self):
        return CartItem.objects.available(self.request)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    # TODO: Add delete method (when removing items from cart)
