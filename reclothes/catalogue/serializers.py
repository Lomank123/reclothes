from accounts.serializers import CustomUserSerializer
from rest_framework import serializers

from catalogue.models import (Category, Product, ProductAttribute,
                              ProductAttributeValue, ProductImage,
                              ProductReview, ProductType, Tag)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        depth = 1
        model = Category
        fields = ('id', 'name')


class CategoryDetailSerializer(serializers.ModelSerializer):
    category_tree = serializers.SerializerMethodField()

    class Meta:
        depth = 1
        model = Category
        fields = ('category_tree', )

    def get_category_tree(self, obj):
        '''Return info about all parent categories including itself.'''
        return obj.get_ancestors(include_self=True).values('id', 'name')


class SubCategorySerializer(serializers.ModelSerializer):
    category_tree = serializers.SerializerMethodField()

    class Meta:
        depth = 1
        model = Category
        fields = ('category_tree', )

    def get_category_tree(self, obj):
        '''Return info about all children.'''
        return obj.get_children().values('id', 'name')


class ProductTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductType
        fields = ('id', 'name')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategoryDetailSerializer()
    product_type = ProductTypeSerializer()
    tags = TagSerializer(many=True)
    avg_rate = serializers.FloatField(default=0.00)

    class Meta:
        model = Product
        fields = (
            'id',
            'category',
            'product_type',
            'tags',
            'avg_rate',
            'in_stock',
            'title',
            'description',
            'regular_price',
            'is_active',
            'created_at',
            'updated_at',
        )


class ProductCatalogueSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = (
            'id',
            'title',
            'regular_price',
            'is_active',
            'quantity',
            'category',
        )


class ProductAttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductAttribute
        fields = ('name', )


class ProductAttributeValueSerializer(serializers.ModelSerializer):
    attribute = ProductAttributeSerializer()

    class Meta:
        model = ProductAttributeValue
        fields = ('attribute', 'value')


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ('id', 'image', 'alt_text', 'is_feature')


class ProductReviewSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = ProductReview
        fields = ('id', 'user', 'text', 'rating', 'created_at')
