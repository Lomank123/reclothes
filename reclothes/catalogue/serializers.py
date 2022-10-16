from accounts.serializers import CompanySerializer, CustomUserSerializer
from django.utils import timezone
from rest_framework import serializers

from catalogue.models import (ActivationKey, Category, OneTimeUrl, Product,
                              ProductAttribute, ProductAttributeValue,
                              ProductFile, ProductImage, ProductReview,
                              ProductType, Tag)


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
    reviews_with_users = serializers.SerializerMethodField()
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

    def get_reviews_with_users(self, instance):
        """Return qs without current user's review if context was specified."""
        qs = instance.reviews.select_related('user')
        user = self.context.get('exclude_user', None)
        if not user.is_authenticated:
            user = None
        return ProductReviewSerializer(qs.exclude(user=user), many=True).data


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
            'category',
        )


class ActivationKeySerializer(serializers.ModelSerializer):

    class Meta:
        model = ActivationKey
        fields = ('key', )


class OneTimeUrlSerializer(serializers.ModelSerializer):

    class Meta:
        model = OneTimeUrl
        fields = ('url_token', 'id')


class ProductFileSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()
    token = serializers.SerializerMethodField()

    class Meta:
        model = ProductFile
        fields = ('id', 'name', 'size', 'is_main', 'link', 'token')

    def get_token(self, product_file):
        url = product_file.one_time_urls.filter(
            is_used=False, expired_at__gte=timezone.now()).first()
        if url is None:
            url = OneTimeUrl.objects.create(file=product_file)
        return url.url_token.hex

    def get_name(self, product_file):
        file = product_file.file
        if file is not None:
            return file.name.split('/')[-1]
        return ''

    def get_size(self, product_file):
        file = product_file.file
        if file is not None:
            return file.size
        return 0


class DownloadProductSerializer(serializers.ModelSerializer):
    files = ProductFileSerializer(many=True, required=False)
    keys = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'files', 'keys', 'guide', 'title')

    def get_keys(self, product):
        order_id = self.context.get('order_id')
        keys = product.activation_keys.filter(order_id=order_id)
        return ActivationKeySerializer(keys, many=True).data


class MyOrdersProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'
