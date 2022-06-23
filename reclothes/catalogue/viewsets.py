from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from catalogue import models
from catalogue import serializers


class ProductViewSet(ModelViewSet):
    serializer_class = serializers.ProductSerializer
    permission_classes = (AllowAny, )

    def get_queryset(self):
        qs = models.Product.objects.all()
        return qs


class CategoryViewSet(ModelViewSet):
    serializer_class = serializers.CategorySerializer
    permission_classes = (AllowAny, )

    def get_queryset(self):
        qs = models.Category.objects.all()
        return qs


class TagViewSet(ModelViewSet):
    serializer_class = serializers.TagSerializer
    permission_classes = (AllowAny, )

    def get_queryset(self):
        qs = models.Tag.objects.all()
        return qs
