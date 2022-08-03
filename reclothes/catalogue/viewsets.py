from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from catalogue import serializers
from catalogue.filters import CatalogueFilter
from catalogue import services
from catalogue.pagination import DefaultCustomPagination


class ProductViewSet(ModelViewSet):
    serializer_class = serializers.ProductSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return services.ProductViewSetService().execute()

    def retrieve(self, request, pk):
        return services.ProductDetailService().execute(pk)

    @action(methods=["get"], detail=False)
    def get_home_products(self, request):
        return services.HomeViewService().execute()


class CatalogueViewSet(ModelViewSet):
    serializer_class = serializers.ProductCatalogueSerializer
    permission_classes = (AllowAny,)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = CatalogueFilter
    search_fields = ('title', 'tags__name')
    pagination_class = DefaultCustomPagination

    def get_queryset(self):
        return services.CatalogueViewSetService().get_products_queryset()

    @action(methods=["get"], detail=False, url_path="prods-and-tags")
    def get_products_with_popular_tags(self, request):
        # This is where filters are implied
        filtered_queryset = self.filter_queryset(self.get_queryset())
        return services.CatalogueViewSetService().get_tags_with_products(
            filtered_queryset, self)


class CategoryViewSet(ModelViewSet):
    serializer_class = serializers.CategorySerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return services.CategoryViewSetService().execute()

    @action(methods=["get"], detail=False, url_path=r"sub/(?P<pk>\w+)")
    def get_sub_categories(self, request, pk):
        return services.CategoryService().execute(pk)

    @action(methods=["get"], detail=False, url_path="root")
    def get_root_categories(self, request):
        return services.CategoryService().execute()


class TagViewSet(ModelViewSet):
    serializer_class = serializers.TagSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return services.TagViewSetService().execute()
