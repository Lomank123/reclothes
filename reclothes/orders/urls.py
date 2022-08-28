from django.urls import path
from rest_framework.routers import DefaultRouter

from orders.views import OrderView
from orders.viewsets import OrderViewSet, OrderItemViewSet, AddressViewSet


router = DefaultRouter()
router.register('order', OrderViewSet, basename='order')
router.register('order-item', OrderItemViewSet, basename='order-item')
router.register('address', AddressViewSet, basename='address')

urlpatterns = [
    path('', OrderView.as_view(), name='order'),
]
