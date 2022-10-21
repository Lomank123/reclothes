from django.views.generic.base import TemplateView
from django_filters.rest_framework import DjangoFilterBackend
from reclothes.pagination import DefaultCustomPagination
from rest_framework.filters import SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from catalogue.consts import HOME_PAGE_PRODUCTS_LIMIT
from catalogue.filters import CatalogueFilter
from catalogue.models import Category, Product
from catalogue.selectors import PopularTagSelector, ImageSubquerySelector
from catalogue.serializers import (BestProductSerializer, CategorySerializer,
                                   HotProductSerializer,
                                   NewestProductSerializer,
                                   ProductCatalogueSerializer,
                                   ProductDetailSerializer,
                                   SubCategorySerializer, TagSerializer)


class HomeView(TemplateView):
    template_name = 'catalogue/home.html'


class ProductDetailView(TemplateView):
    template_name = 'catalogue/product-detail.html'

    def get(self, request, pk, **kwargs):
        return super().get(request, product_id=pk, **kwargs)


class CatalogueView(TemplateView):
    template_name = 'catalogue/catalogue.html'


class CategoriesView(TemplateView):
    template_name = 'catalogue/categories.html'


class ProductDetailAPIView(RetrieveModelMixin, GenericAPIView):
    queryset = Product.active.detailed()
    permission_classes = (AllowAny, )
    serializer_class = ProductDetailSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


# Catalogue
class ProductListAPIView(GenericAPIView):
    queryset = Product.active.all()
    permission_classes = (AllowAny, )
    serializer_class = ProductCatalogueSerializer
    filterset_class = CatalogueFilter
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ('title', 'tags__name')
    pagination_class = DefaultCustomPagination

    def get(self, request):
        """Return products with popular tags."""
        queryset = self.filter_queryset(self.get_queryset())

        # Tags
        popular_tags = PopularTagSelector.select(queryset)
        tag_serializer = TagSerializer(popular_tags, many=True)
        data = {'popular_tags': tag_serializer.data}

        # Pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data['products'] = self.paginator.get_paginated_data(
                serializer.data)
        else:
            data['products'] = self.get_serializer(queryset, many=True).data
        return Response(data)


class HomeListAPIView(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        queryset = Product.active.all()
        img_subquery = ImageSubquerySelector.build_subquery()
        best = queryset.best().annotate(
            feature_image=img_subquery)[:HOME_PAGE_PRODUCTS_LIMIT]
        hot = queryset.hot().annotate(
            feature_image=img_subquery)[:HOME_PAGE_PRODUCTS_LIMIT]
        newest = queryset.newest().annotate(
            feature_image=img_subquery)[:HOME_PAGE_PRODUCTS_LIMIT]
        data = {
            'best_products': BestProductSerializer(best, many=True).data,
            'hot_products': HotProductSerializer(hot, many=True).data,
            'newest_products': NewestProductSerializer(newest, many=True).data,
        }
        return Response(data)


class CategoryListAPIView(GenericAPIView):
    queryset = Category.active.all()
    permission_classes = (AllowAny, )

    @staticmethod
    def _prepare_filters(category_id):
        filters = dict()
        if category_id is None:
            filters['parent__isnull'] = True
        else:
            filters['id'] = category_id
        return filters

    def get_serializer_class(self, **kwargs):
        is_root = kwargs.get('is_root')
        if is_root:
            return CategorySerializer
        return SubCategorySerializer

    def get(self, request):
        category_id = request.GET.get('category_id')
        is_root = category_id is None
        filters = self._prepare_filters(category_id)
        queryset = self.get_queryset().filter(**filters)
        serializer_class = self.get_serializer_class(is_root=is_root)
        data = serializer_class(queryset, many=True).data
        return Response(data)


class CategoryDetailAPIView(RetrieveModelMixin, GenericAPIView):
    queryset = Category.active.all()
    permission_classes = (AllowAny, )
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
