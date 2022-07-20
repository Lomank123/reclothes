from accounts.serializers import CustomUserSerializer
from rest_framework import serializers

from catalogue import models


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Tag
        fields = ('id', 'name',)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = ('id', 'name',)


class CategoryDetailSerializer(serializers.ModelSerializer):
    category_tree = serializers.SerializerMethodField()

    class Meta:
        depth = 1
        model = models.Category
        fields = ('category_tree',)

    def get_category_tree(self, obj):
        """
        Return info about all parent categories including itself.
        """
        return obj.get_ancestors(include_self=True).values("id", "name")


class ProductTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProductType
        fields = ('id', 'name',)


class ProductSerializer(serializers.ModelSerializer):
    category = CategoryDetailSerializer()
    product_type = ProductTypeSerializer()
    tags = TagSerializer(many=True)
    avg_rate = serializers.FloatField(default=0.00)

    class Meta:
        model = models.Product
        fields = '__all__'


class ProductCatalogueSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = models.Product
        fields = ('id', 'title', 'regular_price', 'is_active', 'quantity', 'category',)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        depth = 1
        model = models.Category
        fields = ('id', 'name', )


class ProductAttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProductAttribute
        fields = ('name',)


class ProductAttributeValueSerializer(serializers.ModelSerializer):
    attribute = ProductAttributeSerializer()

    class Meta:
        model = models.ProductAttributeValue
        fields = ('attribute', 'value',)


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProductImage
        fields = ('id', 'image', 'alt_text', 'is_feature',)


class ProductReviewSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = models.ProductReview
        fields = ('id', 'user', 'text', 'rating', 'creation_date',)
