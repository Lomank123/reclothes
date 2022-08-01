from rest_framework import status
from rest_framework.response import Response

from reclothes.services import APIService
from catalogue import consts, serializers
from catalogue.repositories import ProductImageRepository, ProductRepository, \
    CategoryRepository, TagRepository


class HomeViewService:

    # TODO: Rewrite using serializers
    @staticmethod
    def _get_response_data(best, hot, newest):
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
        data = self._get_response_data(
            best_products[:consts.BEST_PRODUCT_IN_PAGE_LIMIT],
            hot_products[:consts.HOT_PRODUCT_IN_PAGE_LIMIT],
            newest_products[:consts.NEWEST_PRODUCT_IN_PAGE_LIMIT]
        )
        return Response(data=data, status=status.HTTP_200_OK)


class ProductDetailService(APIService):

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


class TagViewSetService:

    def execute(self):
        return TagRepository.get_all()


class CategoryService(APIService):

    @staticmethod
    def _get_serializer_class(is_root=False):
        if is_root:
            return serializers.CategorySerializer
        return serializers.SubCategorySerializer

    @staticmethod
    def _get_queryset(id):
        filters = {}
        if id is None:
            filters["parent__isnull"] = True
        else:
            filters["id"] = id
        return CategoryRepository.get_filtered_queryset(**filters)

    def _get_response_data(self, queryset, is_root=False):
        data = {}
        if queryset.exists():
            serializer_class = self._get_serializer_class(is_root)
            category_serializer = serializer_class(queryset, many=True)
            complete_data = {"items": category_serializer.data}
            data.update(complete_data)
        return data

    def execute(self, id=None):
        queryset = self._get_queryset(id)
        data = self._get_response_data(queryset, id is None)
        return self._get_response(data)
