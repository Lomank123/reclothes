from django.urls import path
from rest_framework.routers import DefaultRouter

from orders.views import MyOrdersView, OrderSuccessView, OrderView
from orders.viewsets import AddressViewSet, OrderViewSet

router = DefaultRouter()
router.register('order', OrderViewSet, basename='order')
router.register('address', AddressViewSet, basename='address')

urlpatterns = [
    path('', OrderView.as_view(), name='order'),
    path('success/', OrderSuccessView.as_view(), name='order-success'),
    path('my-orders/', MyOrdersView.as_view(), name='my-orders'),
]
