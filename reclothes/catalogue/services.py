from catalogue.repositories import ProductRepository, CategoryRepository, TagRepository
from rest_framework.response import Response
from rest_framework import status


class HomeViewService:

    @staticmethod
    def _build_response_data(best, hot, newest):
        return {
            "best_products": best,
            "hot_products": hot,
            "newest_products": newest,
        }

    def execute(self):
        best_products = ProductRepository.get_best_products()
        hot_products = ProductRepository.get_hot_products()
        newest_products = ProductRepository.get_newest_products()
        data = self._build_response_data(best_products, hot_products, newest_products)
        return Response(data=data, status=status.HTTP_200_OK)
