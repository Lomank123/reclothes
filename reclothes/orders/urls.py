from django.urls import path
from rest_framework.routers import DefaultRouter

from orders.views import OrderView


router = DefaultRouter()

urlpatterns = [
    path('', OrderView.as_view(), name='order'),
]
