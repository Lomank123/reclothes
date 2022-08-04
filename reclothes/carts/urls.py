from django.urls import path
from rest_framework.routers import DefaultRouter
from carts import viewsets
from carts import views


router = DefaultRouter()
router.register("cart", viewsets.CartViewSet, basename="cart")
router.register("cart_item", viewsets.CartItemViewSet, basename="cart_item")

urlpatterns = [
    path("", views.CartView.as_view(), name="cart"),
]
