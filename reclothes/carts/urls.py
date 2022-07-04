from rest_framework.routers import DefaultRouter
from carts import viewsets


router = DefaultRouter()
router.register("cart", viewsets.CartViewSet, basename="cart")
router.register("cart_item", viewsets.CartItemViewSet, basename="cart_item")

urlpatterns = []
