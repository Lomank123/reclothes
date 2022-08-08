import collections

from reclothes.services import APIService

from catalogue.consts import (BEST_PRODUCT_IN_PAGE_LIMIT,
                              HOT_PRODUCT_IN_PAGE_LIMIT,
                              MOST_POPULAR_TAGS_LIMIT,
                              NEWEST_PRODUCT_IN_PAGE_LIMIT)
from catalogue.repositories import (CategoryRepository, ProductImageRepository,
                                    ProductRepository, TagRepository)
from catalogue.serializers import (CategorySerializer,
                                   ProductAttributeValueSerializer,
                                   ProductImageSerializer,
                                   ProductReviewSerializer, ProductSerializer,
                                   SubCategorySerializer, TagSerializer)


class HomeViewService(APIService):

    @staticmethod
    def _build_response_data(best, hot, newest):
        return {
            "best_products": list(best),
            "hot_products": list(hot),
            "newest_products": list(newest),
        }

    def execute(self):
        feature_image = (
            ProductImageRepository
            .fetch_feature_image_by_product_id(subquery=True)
        )
        best_products = ProductRepository.fetch_best_products(feature_image)
        hot_products = ProductRepository.fetch_hot_products(feature_image)
        newest_products = ProductRepository.fetch_newest_products(feature_image)
        data = self._build_response_data(
            best_products[:BEST_PRODUCT_IN_PAGE_LIMIT],
            hot_products[:HOT_PRODUCT_IN_PAGE_LIMIT],
            newest_products[:NEWEST_PRODUCT_IN_PAGE_LIMIT],
        )
        return self._build_response(data)


class ProductDetailService(APIService):

    @staticmethod
    def _build_response_data(product):
        data = {}
        if product is not None:
            product_serializer = ProductSerializer(product)
            images_serializer = ProductImageSerializer(
                product.ordered_images,
                many=True
            )
            attrs_serializer = ProductAttributeValueSerializer(
                product.attrs_with_values,
                many=True
            )
            reviews_serializer = ProductReviewSerializer(
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
        product = ProductRepository.fetch_single_detailed(id=product_id)
        data = self._build_response_data(product)
        return self._build_response(data)


class CategoryService(APIService):

    @staticmethod
    def _get_serializer_class(is_root=False):
        if is_root:
            return CategorySerializer
        return SubCategorySerializer

    @staticmethod
    def _fetch_queryset(id):
        filters = {}
        if id is None:
            filters["parent__isnull"] = True
        else:
            filters["id"] = id
        return CategoryRepository.fetch(**filters)

    def _build_response_data(self, queryset, is_root=False):
        data = {}
        if queryset.exists():
            serializer_class = self._get_serializer_class(is_root)
            category_serializer = serializer_class(queryset, many=True)
            complete_data = {"items": category_serializer.data}
            data.update(complete_data)
        return data

    def execute(self, id=None):
        """Return root categories if id is None otherwise sub categories."""
        queryset = self._fetch_queryset(id)
        data = self._build_response_data(queryset, id is None)
        return self._build_response(data)


class CatalogueService(APIService):

    __slots__ = 'viewset',

    def __init__(self, viewset):
        self.viewset = viewset

    def _fetch_popular_tags(self, products, limit=MOST_POPULAR_TAGS_LIMIT):
        """Fetch most popular tags based on products queryset."""
        tags_id = ProductRepository.fetch_values_list(
            products, "tags__id")
        counter = collections.Counter(tags_id)
        most_popular_tags_id = [key for key, _ in counter.most_common(limit)]
        filters = {'id__in': most_popular_tags_id}
        most_popular_tags = TagRepository.fetch(**filters)
        return most_popular_tags

    def _build_response_data(self, tags, products):
        data = {}
        if tags.exists():
            serializer = TagSerializer(tags, many=True)
            data["popular_tags"] = serializer.data
        if products.exists():
            page = self.viewset.paginate_queryset(products)
            serializer = self.viewset.get_serializer(page, many=True)
            data["products"] = self.viewset.get_paginated_response(
                serializer.data).data
        return data

    def execute(self):
        """Return popular tags with filtered products queryset."""
        initial_qs = self.viewset.get_queryset()
        products = self.viewset.filter_queryset(initial_qs)
        popular_tags = self._fetch_popular_tags(products)
        data = self._build_response_data(popular_tags, products)
        return self._build_response(data)


class ProductViewSetService:

    def execute(self):
        return ProductRepository.fetch(is_active=True)


class CatalogueViewSetService:

    def execute(self):
        return ProductRepository.fetch_active_with_category()


class CategoryViewSetService:

    def execute(self):
        return CategoryRepository.fetch(is_active=True)


class TagViewSetService:

    def execute(self):
        return TagRepository.fetch()
