from rest_framework import status
from rest_framework.response import Response

from catalogue import consts, serializers
from catalogue.repositories import ProductImageRepository, ProductRepository, \
    CategoryRepository, TagRepository


class HomeViewService:

    @staticmethod
    def _build_response_data(best, hot, newest):
        return {
            "best_products": list(best),
            "hot_products": list(hot),
            "newest_products": list(newest),
        }

    def execute(self):
        feature_image = ProductImageRepository.get_feature_image_by_product_id(
            subquery=True
        )
        best_products = ProductRepository.get_best_products(feature_image)
        hot_products = ProductRepository.get_hot_products(feature_image)
        newest_products = ProductRepository.get_newest_products(feature_image)
        data = self._build_response_data(
            best_products[:consts.BEST_PRODUCT_IN_PAGE_LIMIT],
            hot_products[:consts.HOT_PRODUCT_IN_PAGE_LIMIT],
            newest_products[:consts.NEWEST_PRODUCT_IN_PAGE_LIMIT]
        )
        return Response(data=data, status=status.HTTP_200_OK)


class ProductDetailService:

    @staticmethod
    def _get_response_data(product):
        data = {}
        if product is not None:
            # Querysets
            images = ProductRepository.get_images(product)
            attr_values = ProductRepository.get_values_with_attrs(product)
            reviews = ProductRepository.get_reviews_with_user(product)

            # Serialization
            product_serializer = serializers.ProductSerializer(product)
            images_serializer = serializers.ProductImageSerializer(
                images,
                many=True
            )
            attrs_serializer = serializers.ProductAttributeValueSerializer(
                attr_values,
                many=True
            )
            reviews_serializer = serializers.ProductReviewSerializer(
                reviews,
                many=True
            )

            # Final data representation
            complete_data = {
                "product": product_serializer.data,
                "attrs": attrs_serializer.data,
                "images": images_serializer.data,
                "reviews": reviews_serializer.data,
            }

            data.update(complete_data)
        return data

    @staticmethod
    def _get_response(data):
        response = Response(data=data, status=status.HTTP_200_OK)
        if len(data) == 0:
            response.status_code = status.HTTP_404_NOT_FOUND
        return response

    def execute(self, product_id):
        product = ProductRepository.get_by_id(product_id)
        data = self._get_response_data(product)
        return self._get_response(data)


class ProductViewSetService:

    def execute(self):
        return ProductRepository.get_active()


class CatalogueViewSetService:

    def execute(self):
        return ProductRepository.get_active_with_category()


class CategoryViewSetService:

    def execute(self):
        return CategoryRepository.get_active()


class CategoryDetailService:

    @staticmethod
    def _get_response(data):
        response = Response(data=data, status=status.HTTP_200_OK)
        if len(data) == 0:
            response.status_code = status.HTTP_404_NOT_FOUND
        return response

    @staticmethod
    def _get_response_data(category):
        data = {}
        if category is not None:
            category_serializer = serializers.CategoryDetailSerializer(
                category
            )
            complete_data = {
                "category": category_serializer.data,
            }
            data.update(complete_data)
        return data

    def execute(self, id):
        category = CategoryRepository.get_by_id(id)
        data = self._get_response_data(category)
        return self._get_response(data)


class CategoryRootService:

    @staticmethod
    def _get_response(data):
        response = Response(data=data, status=status.HTTP_200_OK)
        if len(data) == 0:
            response.status_code = status.HTTP_404_NOT_FOUND
        return response

    @staticmethod
    def _get_response_data(categories):
        data = {}
        if categories is not None:
            category_serializer = serializers.CategoryDetailSerializer(
                categories,
                many=True
            )
            complete_data = {
                "roots": category_serializer.data,
            }
            data.update(complete_data)
        return data

    def execute(self):
        root_categories = CategoryRepository.get_roots()
        data = self._get_response_data(root_categories)
        return self._get_response(data)


class TagViewSetService:

    def execute(self):
        return TagRepository.get_all()
