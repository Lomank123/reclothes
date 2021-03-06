from django.urls import path
from rest_framework.routers import DefaultRouter
from catalogue import views, viewsets


router = DefaultRouter()
router.register("product", viewsets.ProductViewSet, basename="product")
router.register("category", viewsets.CategoryViewSet, basename="category")
router.register("tag", viewsets.TagViewSet, basename="tag")
router.register("catalogue", viewsets.CatalogueViewSet, basename="catalogue")

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name="product-detail"),
    path('catalogue/', views.CatalogueView.as_view(), name="catalogue"),
]
