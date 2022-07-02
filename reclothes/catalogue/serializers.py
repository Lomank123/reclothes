from rest_framework import serializers
from catalogue import models


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
        fields = ('name', )


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    product_type = ProductTypeSerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = models.Product
        fields = '__all__'
