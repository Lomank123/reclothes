from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from catalogue import serializers
from catalogue.models import Category, Product, Tag
from catalogue.services import HomeViewService


class ProductViewSet(ModelViewSet):
    serializer_class = serializers.ProductSerializer
    permission_classes = (AllowAny, )

    def get_queryset(self):
        qs = Product.objects.filter(is_active=True)
        return qs

    @action(methods=["get"], detail=False)
    def get_home_products(self):
        return HomeViewService().execute()


class CategoryViewSet(ModelViewSet):
    serializer_class = serializers.CategorySerializer
    permission_classes = (AllowAny, )

    def get_queryset(self):
        qs = Category.objects.filter(is_active=True)
        return qs


class TagViewSet(ModelViewSet):
    serializer_class = serializers.TagSerializer
    permission_classes = (AllowAny, )

    def get_queryset(self):
        qs = Tag.objects.all()
        return qs
