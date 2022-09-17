from django.urls import path
from rest_framework.routers import DefaultRouter

from orders.views import MyOrdersView, OrderSuccessView, OrderView, DonwloadFileView
from orders.viewsets import OrderViewSet

router = DefaultRouter()
router.register('order', OrderViewSet, basename='order')

urlpatterns = [
    path('', OrderView.as_view(), name='order'),
    path('success/', OrderSuccessView.as_view(), name='order-success'),
    path('my-orders/', MyOrdersView.as_view(), name='my-orders'),
    path('download/', DonwloadFileView.as_view(), name='download'),
]
