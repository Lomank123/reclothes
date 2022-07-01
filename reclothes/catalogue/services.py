from catalogue.repositories import ProductRepository
from rest_framework.response import Response
from rest_framework import status

from catalogue import consts
from catalogue.serializers import ProductSerializer


class HomeViewService:

    @staticmethod
    def _build_response_data(best, hot, newest):
        return {
            "best_products": list(best),
            "hot_products": list(hot),
            "newest_products": list(newest),
        }

    def execute(self):
        best_products = ProductRepository.get_best_products()[:consts.BEST_PRODUCT_IN_PAGE_LIMIT]
        hot_products = ProductRepository.get_hot_products()[:consts.HOT_PRODUCT_IN_PAGE_LIMIT]
        newest_products = ProductRepository.get_newest_products()[:consts.NEWEST_PRODUCT_IN_PAGE_LIMIT]
        data = self._build_response_data(best_products, hot_products, newest_products)
        return Response(data=data, status=status.HTTP_200_OK)


class ProductDetailService:

    @staticmethod
    def _build_response_data(product, attrs):
        serializer = ProductSerializer(product)
        return {
            "product": serializer.data,
            "attrs": list(attrs),
        }

    @staticmethod
    def _build_response(data, is_none):
        response = Response(data=data, status=status.HTTP_200_OK)
        if is_none:
            response.status_code = status.HTTP_404_NOT_FOUND
        return response

    def execute(self, product_id):
        product = ProductRepository.get_by_id(product_id)
        attrs = ProductRepository.get_product_attrs(product_id)
        data = self._build_response_data(product, attrs)
        return self._build_response(data, product is None)
