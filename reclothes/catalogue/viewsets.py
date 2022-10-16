from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from catalogue.filters import CatalogueFilter
from catalogue.models import Category, ProductReview, Tag
from catalogue.pagination import DefaultCustomPagination
from catalogue.serializers import (CategorySerializer,
                                   ProductCatalogueSerializer,
                                   ProductReviewSerializer, TagSerializer)
from catalogue.services import (CatalogueService, CategoryService,
                                HomeViewService, ProductDetailService)
from catalogue.repositories import ProductRepository


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
        return ProductRepository.fetch_active().select_related(
            'category', 'company')

    def retrieve(self, request, pk):
        return ProductDetailService(request).execute(pk)

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

    def get_queryset(self):
        return Category.objects.filter(is_active=True)

    def list(self, request):
        return CategoryService(request).execute()


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_permissions(self):
        UNSAFE_ACTIONS = ['create', 'destroy', 'update', 'partial_update']

        if self.action in UNSAFE_ACTIONS:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class ProductReviewViewSet(ModelViewSet):
    serializer_class = ProductReviewSerializer

    def get_permissions(self):
        AUTH_REQUIRED_ACTIONS = ['retrieve', 'create']

        if self.action in AUTH_REQUIRED_ACTIONS:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        filters = dict()
        if action == 'retrieve':
            filters['user'] = self.request.user
        return ProductReview.objects.filter(**filters)
