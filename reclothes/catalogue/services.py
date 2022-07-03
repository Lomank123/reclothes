from catalogue.repositories import ProductRepository, ProductImageRepository
from rest_framework.response import Response
from rest_framework import status

from catalogue import consts
from catalogue import serializers


class HomeViewService:

    @staticmethod
    def _build_response_data(best, hot, newest):
        return {
            "best_products": list(best),
            "hot_products": list(hot),
            "newest_products": list(newest),
        }

    def execute(self):
        feature_image = ProductImageRepository.get_feature_image_by_product_id(subquery=True)
        best_products = ProductRepository.get_best_products(feature_image)[:consts.BEST_PRODUCT_IN_PAGE_LIMIT]
        hot_products = ProductRepository.get_hot_products(feature_image)[:consts.HOT_PRODUCT_IN_PAGE_LIMIT]
        newest_products = ProductRepository.get_newest_products(feature_image)[:consts.NEWEST_PRODUCT_IN_PAGE_LIMIT]
        data = self._build_response_data(best_products, hot_products, newest_products)
        return Response(data=data, status=status.HTTP_200_OK)


class ProductDetailService:

    @staticmethod
    def _build_response_data(product):
        product_serializer = serializers.ProductSerializer(product)
        images_serializer = serializers.ProductImageSerializer(product.images, many=True)
        attrs_serializer = serializers.ProductAttributeValueSerializer(product.attr_values, many=True)
        reviews_serializer = serializers.ProductReviewSerializer(product.reviews, many=True)
        return {
            "product": product_serializer.data,
            "attrs": attrs_serializer.data,
            "images": images_serializer.data,
            "reviews": reviews_serializer.data,
        }

    @staticmethod
    def _build_response(data, is_none):
        response = Response(data=data, status=status.HTTP_200_OK)
        if is_none:
            response.status_code = status.HTTP_404_NOT_FOUND
        return response

    def execute(self, product_id):
        product = ProductRepository.get_by_id(product_id)
        data = {}
        if product is not None:
            data = self._build_response_data(product)
        return self._build_response(data, product is None)
