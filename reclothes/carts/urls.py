from django.urls import path
from rest_framework.routers import DefaultRouter

from carts.views import CartView
from carts.viewsets import CartItemViewSet, CartViewSet


router = DefaultRouter()
router.register("cart", CartViewSet, basename="cart")
router.register("cart_item", CartItemViewSet, basename="cart_item")

urlpatterns = [
    path("", CartView.as_view(), name="cart"),
]
