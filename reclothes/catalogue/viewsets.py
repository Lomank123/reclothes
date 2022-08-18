from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from catalogue.filters import CatalogueFilter
from catalogue.pagination import DefaultCustomPagination
from catalogue.serializers import (CategorySerializer,
                                   ProductCatalogueSerializer, TagSerializer)
from catalogue.services import (CatalogueService, CategoryService,
                                CategoryViewSetService, HomeViewService,
                                ProductDetailService, ProductViewSetService,
                                TagViewSetService)


class ProductViewSet(ModelViewSet):
    serializer_class = ProductCatalogueSerializer
    permission_classes = (AllowAny, )
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = CatalogueFilter
    search_fields = ('title', 'tags__name')
    pagination_class = DefaultCustomPagination

    def get_queryset(self):
        return ProductViewSetService().execute()

    def retrieve(self, request, pk):
        return ProductDetailService().execute(pk)

    @action(methods=['get'], detail=False, url_path='home')
    def fetch_home_products(self, request):
        return HomeViewService().execute()

    @action(methods=['get'], detail=False, url_path='catalogue')
    def fetch_products_with_popular_tags(self, request):
        return CatalogueService(self).execute(paginate=True)


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = (AllowAny, )

    def get_queryset(self):
        return CategoryViewSetService().execute()

    @action(methods=['get'], detail=False, url_path=r'sub/(?P<pk>\w+)')
    def fetch_sub_categories(self, request, pk):
        return CategoryService().execute(pk)

    @action(methods=['get'], detail=False, url_path='root')
    def fetch_root_categories(self, request):
        return CategoryService().execute()


class TagViewSet(ModelViewSet):
    serializer_class = TagSerializer
    permission_classes = (AllowAny, )

    def get_queryset(self):
        return TagViewSetService().execute()
