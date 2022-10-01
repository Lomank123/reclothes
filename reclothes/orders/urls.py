from django.urls import path, re_path
from rest_framework.routers import DefaultRouter

from orders.views import (DownloadFileView, MyOrdersView, OrderSuccessView,
                          OrderView)
from orders.viewsets import OrderViewSet

router = DefaultRouter()
router.register('order', OrderViewSet, basename='order')


urlpatterns = [
    path('', OrderView.as_view(), name='order'),
    path('success/', OrderSuccessView.as_view(), name='order-success'),
    path('my-orders/', MyOrdersView.as_view(), name='my-orders'),
    re_path(
        r'^download/(?P<url_token>\w+)/$',
        DownloadFileView.as_view(),
        name='download',
    ),
]
