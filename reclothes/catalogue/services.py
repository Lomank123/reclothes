import collections

from reclothes.services import APIService

from catalogue.consts import (BEST_PRODUCT_IN_PAGE_LIMIT,
                              HOT_PRODUCT_IN_PAGE_LIMIT,
                              MOST_POPULAR_TAGS_LIMIT,
                              NEWEST_PRODUCT_IN_PAGE_LIMIT,
                              PRODUCT_NOT_FOUND_MSG)
from catalogue.repositories import (CategoryRepository, OneTimeUrlRepository,
                                    ProductImageRepository, ProductRepository,
                                    TagRepository, ProductFileRepository)
from catalogue.serializers import (CategorySerializer, OneTimeUrlSerializer,
                                   ProductDetailSerializer,
                                   SubCategorySerializer, TagSerializer)


class HomeViewService(APIService):

    def __init__(self):
        super().__init__()

    def _build_response_data(self, best, hot, newest, **kwargs):
        data = {
            'best_products': list(best[:BEST_PRODUCT_IN_PAGE_LIMIT]),
            'hot_products': list(hot[:HOT_PRODUCT_IN_PAGE_LIMIT]),
            'newest_products': list(newest[:NEWEST_PRODUCT_IN_PAGE_LIMIT]),
        }
        data.update(kwargs)
        return super()._build_response_data(**data)

    def execute(self, **kwargs):
        img_subquery = ProductImageRepository.prepare_feature_image_subquery()
        best = ProductRepository.fetch_best_products(img_subquery)
        hot = ProductRepository.fetch_hot_products(img_subquery)
        newest = ProductRepository.fetch_newest_products(img_subquery)
        data = self._build_response_data(best, hot, newest, **kwargs)
        return self._build_response(data)


class ProductDetailService(APIService):

    def __init__(self):
        super().__init__()

    def _validate_data(self, product):
        if product is None:
            self.errors['product'] = PRODUCT_NOT_FOUND_MSG
            return False
        return True

    def _serialize_data(self, product, is_valid):
        if not is_valid:
            return dict()
        return ProductDetailSerializer(product).data

    def _build_response_data(self, product):
        if self.errors:
            return {'detail': self.errors}
        return {'data': product}

    def execute(self, product_id):
        product = ProductRepository.fetch_single_detailed(id=product_id)
        is_valid = self._validate_data(product)
        serialized_product = self._serialize_data(product, is_valid)
        data = self._build_response_data(serialized_product)
        return self._build_response(data)


class CategoryService(APIService):

    def __init__(self):
        super().__init__()

    @staticmethod
    def _get_serializer_class(is_root=False):
        if is_root:
            return CategorySerializer
        return SubCategorySerializer

    @staticmethod
    def _fetch_categories(id):
        filters = {}
        if id is None:
            filters['parent__isnull'] = True
        else:
            filters['id'] = id
        return CategoryRepository.fetch(**filters)

    def _build_response_data(self, categories):
        data = {'items': categories}
        return super()._build_response_data(**data)

    def execute(self, id=None):
        '''Return root categories if id is None otherwise sub categories.'''
        queryset = self._fetch_categories(id)
        serializer_class = self._get_serializer_class(id is None)
        serialized_data = serializer_class(queryset, many=True).data
        data = self._build_response_data(categories=serialized_data)
        return self._build_response(data)


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

    def _build_response_data(self, tags, products):
        data = {'products': products, 'popular_tags': tags}
        return super()._build_response_data(**data)

    def execute(self, paginate=False):
        '''Return popular tags with filtered and paginated products.'''
        products = self.viewset.get_queryset()
        filtered_products = self.viewset.filter_queryset(products)
        popular_tags = self._fetch_popular_tags(filtered_products)
        serialized_tags = TagSerializer(popular_tags, many=True).data
        serialized_products = self._serialize_products(
            filtered_products, paginate=paginate)
        data = self._build_response_data(serialized_tags, serialized_products)
        return self._build_response(data)


class GenerateOneTimeUrlService(APIService):

    def __init__(self, request):
        self.request = request

    def execute(self):
        file_id = self.request.data.get('file_id', None)
        file = ProductFileRepository.fetch(first=True, id=file_id)

        if file is None:
            self.errors['file'] = 'File not found.'
            data = self._build_response_data()
            return self._build_response(data)

        new_url = OneTimeUrlRepository.create(file=file)
        serializer = OneTimeUrlSerializer(new_url)
        data = self._build_response_data(**serializer.data)
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
