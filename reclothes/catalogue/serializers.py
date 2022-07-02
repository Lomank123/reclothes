from rest_framework import serializers
from catalogue import models
from accounts.serializers import CustomUserSerializer


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Tag
        fields = ('id', 'name',)


class CategorySerializer(serializers.ModelSerializer):
    parent_node = serializers.SerializerMethodField()

    class Meta:
        depth = 1
        model = models.Category
        fields = ('id', 'name', 'parent_node',)

    def get_parent_node(self, obj):
        return obj.get_ancestors().values("id", "name")


class ProductTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProductType
        fields = ('name',)


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    product_type = ProductTypeSerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = models.Product
        fields = '__all__'


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
        fields = ('id', 'user', 'text', 'rating')
