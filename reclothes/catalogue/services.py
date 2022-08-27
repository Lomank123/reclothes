import collections

from reclothes.services import APIService

from catalogue.consts import (BEST_PRODUCT_IN_PAGE_LIMIT,
                              HOT_PRODUCT_IN_PAGE_LIMIT,
                              MOST_POPULAR_TAGS_LIMIT,
                              NEWEST_PRODUCT_IN_PAGE_LIMIT)
from catalogue.repositories import (CategoryRepository, ProductImageRepository,
                                    ProductRepository, TagRepository)
from catalogue.serializers import (CategorySerializer, ProductDetailSerializer,
                                   SubCategorySerializer, TagSerializer)


class HomeViewService(APIService):

    @staticmethod
    def _build_response_data(best, hot, newest):
        return {
            "best_products": list(best[:BEST_PRODUCT_IN_PAGE_LIMIT]),
            "hot_products": list(hot[:HOT_PRODUCT_IN_PAGE_LIMIT]),
            "newest_products": list(newest[:NEWEST_PRODUCT_IN_PAGE_LIMIT]),
        }

    def execute(self):
        img_subquery = ProductImageRepository.prepare_feature_image_subquery()
        best_products = ProductRepository.fetch_best_products(img_subquery)
        hot_products = ProductRepository.fetch_hot_products(img_subquery)
        newest_products = ProductRepository.fetch_newest_products(img_subquery)
        data = self._build_response_data(
            best_products, hot_products, newest_products)
        return self._build_response(data)


class ProductDetailService(APIService):

    @staticmethod
    def _build_response_data(product):
        data = {}
        if product is not None:
            product_serializer = ProductDetailSerializer(product)
            complete_data = {"product": product_serializer.data}
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
    def _fetch_categories(id):
        filters = {}
        if id is None:
            filters["parent__isnull"] = True
        else:
            filters["id"] = id
        return CategoryRepository.fetch(**filters)

    def _build_response_data(self, queryset, serializer_class):
        category_serializer = serializer_class(queryset, many=True)
        return {"items": category_serializer.data}

    def execute(self, id=None):
        """Return root categories if id is None otherwise sub categories."""
        queryset = self._fetch_categories(id)
        serializer_class = self._get_serializer_class(id is None)
        data = self._build_response_data(queryset, serializer_class)
        return self._build_response(data)


class CatalogueService(APIService):

    __slots__ = 'viewset',

    def __init__(self, viewset):
        self.viewset = viewset

    def _fetch_popular_tags(self, products, limit=MOST_POPULAR_TAGS_LIMIT):
        """Fetch most popular tags based on products queryset."""
        tags_ids = ProductRepository.fetch_tags_ids(products)
        counter = collections.Counter(tags_ids)
        popular_ids = [key for key, _ in counter.most_common(limit)]
        filters = {'id__in': popular_ids}
        popular_tags = TagRepository.fetch(**filters)
        return popular_tags

    def _serialize_products(self, products, paginate=False):
        serializer_class = self.viewset.get_serializer_class()
        if paginate:
            page = self.viewset.paginate_queryset(products)
            if page is not None:
                serializer = serializer_class(page, many=True)
                return self.viewset.paginator.get_paginated_data(
                    serializer.data)
        serializer = serializer_class(products, many=True)
        return serializer.data

    def _build_response_data(self, tags, products):
        return {'products': products, 'popular_tags': tags}

    def execute(self, paginate=False):
        """Return popular tags with filtered and paginated products."""
        products = self.viewset.get_queryset()
        filtered_products = self.viewset.filter_queryset(products)
        popular_tags = self._fetch_popular_tags(filtered_products)
        serialized_tags = TagSerializer(popular_tags, many=True).data
        serialized_products = self._serialize_products(
            filtered_products, paginate=paginate)
        data = self._build_response_data(serialized_tags, serialized_products)
        return self._build_response(data)


class ProductViewSetService:

    def execute(self):
        return ProductRepository.fetch_active_with_category()


class CategoryViewSetService:

    def execute(self):
        return CategoryRepository.fetch(is_active=True)


class TagViewSetService:

    def execute(self):
        return TagRepository.fetch()
