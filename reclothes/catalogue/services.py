from catalogue.repositories import ProductRepository
from rest_framework.response import Response
from rest_framework import status

from catalogue import consts


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
