from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from catalogue.filters import CatalogueFilter
from reclothes.pagination import DefaultCustomPagination
from catalogue.serializers import (CategorySerializer,
                                   ProductCatalogueSerializer, TagSerializer)
from catalogue.services import (CatalogueService, CategoryService,
                                CategoryViewSetService, HomeViewService,
                                ProductDetailService, ProductViewSetService,
                                TagViewSetService)


class ProductViewSet(ModelViewSet):
    serializer_class = ProductCatalogueSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = CatalogueFilter
    search_fields = ('title', 'tags__name')
    pagination_class = DefaultCustomPagination

    def get_permissions(self):
        UNSAFE_ACTIONS = ['create', 'destroy', 'update', 'partial_update']

        if self.action in UNSAFE_ACTIONS:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return ProductViewSetService().execute()

    def retrieve(self, request, pk):
        return ProductDetailService().execute(pk)

    @action(methods=['get'], detail=False)
    def home(self, request):
        return HomeViewService().execute()

    @action(methods=['get'], detail=False)
    def catalogue(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        return CatalogueService(request).execute(queryset)


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer

    def get_permissions(self):
        UNSAFE_ACTIONS = ['create', 'destroy', 'update', 'partial_update']

        if self.action in UNSAFE_ACTIONS:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def list(self, request):
        return CategoryService(request).execute()

    def get_queryset(self):
        return CategoryViewSetService().execute()


class TagViewSet(ModelViewSet):
    serializer_class = TagSerializer

    def get_permissions(self):
        UNSAFE_ACTIONS = ['create', 'destroy', 'update', 'partial_update']

        if self.action in UNSAFE_ACTIONS:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return TagViewSetService().execute()
