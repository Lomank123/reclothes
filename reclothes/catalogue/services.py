import collections

from reclothes.services import APIService
from catalogue import consts, serializers
from catalogue.repositories import ProductImageRepository, ProductRepository, \
    CategoryRepository, TagRepository


class HomeViewService(APIService):

    @staticmethod
    def _get_response_data(best, hot, newest):
        return {
            "best_products": list(best),
            "hot_products": list(hot),
            "newest_products": list(newest),
        }

    def execute(self):
        feature_image = (
            ProductImageRepository
            .get_feature_image_by_product_id(subquery=True)
        )
        best_products = ProductRepository.get_best_products(feature_image)
        hot_products = ProductRepository.get_hot_products(feature_image)
        newest_products = ProductRepository.get_newest_products(feature_image)
        data = self._get_response_data(
            best_products[:consts.BEST_PRODUCT_IN_PAGE_LIMIT],
            hot_products[:consts.HOT_PRODUCT_IN_PAGE_LIMIT],
            newest_products[:consts.NEWEST_PRODUCT_IN_PAGE_LIMIT]
        )
        return self._get_response(data)


class ProductDetailService(APIService):

    @staticmethod
    def _get_response_data(product):
        data = {}
        if product is not None:
            product_serializer = serializers.ProductSerializer(product)
            images_serializer = serializers.ProductImageSerializer(
                product.all_images,
                many=True
            )
            attrs_serializer = serializers.ProductAttributeValueSerializer(
                product.attrs_with_values,
                many=True
            )
            reviews_serializer = serializers.ProductReviewSerializer(
                product.reviews_with_users,
                many=True
            )

            complete_data = {
                "product": product_serializer.data,
                "attrs": attrs_serializer.data,
                "images": images_serializer.data,
                "reviews": reviews_serializer.data,
            }

            data.update(complete_data)
        return data

    def execute(self, product_id):
        product = ProductRepository.get_detailed_by_id(product_id)
        data = self._get_response_data(product)
        return self._get_response(data)


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


class ProductViewSetService:

    def execute(self):
        return ProductRepository.get_filtered_queryset(is_active=True)


class CatalogueViewSetService(APIService):

    def _get_popular_tags(self, products, limit=consts.MOST_POPULAR_TAGS_LIMIT):
        """Get most popular tags based on products queryset."""
        tags_id = ProductRepository().get_values_list(
            products, "tags__id")
        counter = collections.Counter(tags_id)
        most_popular_tags_id = [key for key, _ in counter.most_common(limit)]
        most_popular_tags = TagRepository().get_by_ids(most_popular_tags_id)
        return most_popular_tags

    def _get_response_data(self, tags, products, viewset):
        data = {}
        if tags.exists():
            serializer = serializers.TagSerializer(tags, many=True)
            data["popular_tags"] = serializer.data
        if products.exists():
            page = viewset.paginate_queryset(products)
            serializer = viewset.get_serializer(page, many=True)
            data["products"] = viewset.get_paginated_response(
                serializer.data).data
        return data

    def get_tags_with_products(self, products, viewset):
        """Return popular tags with filtered products queryset."""
        popular_tags = self._get_popular_tags(products)
        data = self._get_response_data(popular_tags, products, viewset)
        return self._get_response(data)

    def get_products_queryset(self):
        return ProductRepository.get_active_with_category()


class CategoryViewSetService:

    def execute(self):
        return CategoryRepository.get_filtered_queryset(is_active=True)


class TagViewSetService:

    def execute(self):
        return TagRepository.get_all()
