from accounts.serializers import CompanySerializer, CustomUserSerializer
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


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategoryDetailSerializer(required=False)
    product_type = ProductTypeSerializer(required=False)
    tags = TagSerializer(required=False, many=True)
    ordered_images = ProductImageSerializer(required=False, many=True)
    attrs_with_values = ProductAttributeValueSerializer(
        required=False, many=True)
    reviews_with_users = ProductReviewSerializer(required=False, many=True)
    company = CompanySerializer(required=False)
    avg_rate = serializers.FloatField(default=0.00)

    class Meta:
        model = Product
        fields = (
            'id',
            'category',
            'company',
            'product_type',
            'tags',
            'avg_rate',
            'in_stock',
            'is_limited',
            'title',
            'description',
            'regular_price',
            'is_active',
            'created_at',
            'updated_at',
            'ordered_images',
            'attrs_with_values',
            'reviews_with_users',
        )


class ProductCatalogueSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=False)
    company = CompanySerializer(required=False)

    class Meta:
        model = Product
        fields = (
            'id',
            'company',
            'title',
            'regular_price',
            'is_active',
            'quantity',
            'category',
        )
