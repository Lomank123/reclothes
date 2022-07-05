from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from catalogue import serializers
from catalogue.filters import CatalogueFilter
from catalogue.models import Category, Product, Tag
from catalogue.services import HomeViewService, ProductDetailService


class ProductViewSet(ModelViewSet):
    serializer_class = serializers.ProductSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Product.objects.filter(is_active=True)

    @action(methods=["get"], detail=False)
    def get_home_products(self, request):
        return HomeViewService().execute()

    @action(methods=["get"], detail=False, url_path=r"get_product_detail/(?P<product_id>[^/.]+)")
    def get_product_detail(self, request, product_id):
        return ProductDetailService().execute(product_id)


class CatalogueViewSet(ModelViewSet):
    serializer_class = serializers.ProductCatalogueSerializer
    permission_classes = (AllowAny,)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = CatalogueFilter
    search_fields = ('title', 'description',)

    def get_queryset(self):
        return Product.objects.filter(is_active=True)


class CategoryViewSet(ModelViewSet):
    serializer_class = serializers.CategorySerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Category.objects.filter(is_active=True)


class TagViewSet(ModelViewSet):
    serializer_class = serializers.TagSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Tag.objects.all()
