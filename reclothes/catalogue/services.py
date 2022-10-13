import collections

from reclothes.services import APIService
from rest_framework.exceptions import NotFound

from catalogue.consts import (BEST_PRODUCT_IN_PAGE_LIMIT,
                              HOT_PRODUCT_IN_PAGE_LIMIT,
                              MOST_POPULAR_TAGS_LIMIT,
                              NEWEST_PRODUCT_IN_PAGE_LIMIT)
from catalogue.repositories import (CategoryRepository, ProductImageRepository,
                                    ProductRepository, TagRepository)
from catalogue.serializers import (CategorySerializer, ProductDetailSerializer,
                                   SubCategorySerializer, TagSerializer)


class HomeViewService(APIService):

    def _build_response_data(self, best, hot, newest, **kwargs):
        data = {
            'best_products': list(best[:BEST_PRODUCT_IN_PAGE_LIMIT]),
            'hot_products': list(hot[:HOT_PRODUCT_IN_PAGE_LIMIT]),
            'newest_products': list(newest[:NEWEST_PRODUCT_IN_PAGE_LIMIT]),
        }
        data.update(kwargs)
        return super()._build_response_data(**data)

    def execute(self):
        img_subquery = ProductImageRepository.prepare_feature_image_subquery()
        best = ProductRepository.fetch_best_products(img_subquery)
        hot = ProductRepository.fetch_hot_products(img_subquery)
        newest = ProductRepository.fetch_newest_products(img_subquery)
        data = self._build_response_data(best, hot, newest)
        return self._build_response(data)


class ProductDetailService(APIService):

    @staticmethod
    def _validate(product):
        if product is None:
            raise NotFound()

    def execute(self, product_id):
        product = ProductRepository.fetch_single_detailed(id=product_id)
        self._validate(product)
        serializer = ProductDetailSerializer(product)
        data = self._build_response_data(**serializer.data)
        return self._build_response(data)


class CategoryService(APIService):
    """Return root or sub categories based on provided category_id."""

    def __init__(self, request):
        super().__init__()
        self.request = request

    @staticmethod
    def _get_serializer_class(is_root=False):
        if is_root:
            return CategorySerializer
        return SubCategorySerializer

    @staticmethod
    def _prepare_filters(category_id):
        filters = dict()
        if category_id is None:
            filters['parent__isnull'] = True
        else:
            filters['id'] = category_id
        return filters

    def execute(self):
        category_id = self.request.GET.get('category_id', None)
        filters = self._prepare_filters(category_id)
        categories = CategoryRepository.fetch(**filters)
        serializer_class = self._get_serializer_class(category_id is None)
        serializer = serializer_class(categories, many=True)
        data = self._build_response_data(categories=serializer.data)
        return self._build_response(data)


# TODO: Refactor this
class CatalogueService(APIService):

    __slots__ = 'viewset',

    def __init__(self, viewset):
        super().__init__()
        self.viewset = viewset

    def _fetch_popular_tags(self, products, limit=MOST_POPULAR_TAGS_LIMIT):
        '''Fetch most popular tags based on products queryset.'''
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

    def execute(self, paginate=False):
        '''Return popular tags with filtered and paginated products.'''
        products = self.viewset.get_queryset()
        filtered_products = self.viewset.filter_queryset(products)
        popular_tags = self._fetch_popular_tags(filtered_products)
        serialized_tags = TagSerializer(popular_tags, many=True).data
        serialized_products = self._serialize_products(
            filtered_products, paginate=paginate)
        data = self._build_response_data(
            popular_tags=serialized_tags, products=serialized_products)
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
