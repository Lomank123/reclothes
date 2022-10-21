from django.db.models import Avg, Count, F, OuterRef, Q, Subquery
from django.utils import timezone

from catalogue.models import (Category, OneTimeUrl, Product, ProductFile,
                              ProductImage, Tag)


class ProductRepository:

    @staticmethod
    def fetch(first=False, limit=None, **kwargs):
        qs = Product.objects.filter(**kwargs)
        if first:
            return qs.first()
        elif limit:
            return qs[:limit]
        return qs

    @staticmethod
    def fetch_active(first=False, limit=None, **kwargs):
        """
        Return active products which either have 0 or enough keys.
        """
        no_order = Q(activation_keys__order__isnull=True)
        not_expired = Q(activation_keys__expired_at__gte=timezone.now())
        active_keys_count = Count(
            'activation_keys', filter=no_order & not_expired)
        active_products = Q(is_active=True) & (
            Q(keys_limit=0) | Q(keys_diff__gte=0))

        qs = (
            Product.objects
            .annotate(keys_diff=active_keys_count - F('keys_limit'))
            .filter(active_products)
            .order_by('-id')
        )
        if first:
            return qs.first()
        elif limit:
            return qs[:limit]
        return qs

    @staticmethod
    def fetch_active_with_category():
        return (
            ProductRepository
            .fetch_active()
            .select_related('category')
        )

    @staticmethod
    def fetch_single_detailed(**kwargs):
        '''Return product with average rating and related category and type.'''
        return (
            Product.objects
            .select_related('category', 'product_type')
            .filter(**kwargs)
            .annotate(avg_rate=Avg('reviews__rating'))
            .first()
        )

    @staticmethod
    def fetch_tags_ids(products):
        '''Return list of tags ids without nulls.'''
        return products.filter(tags__isnull=False).values_list(
            'tags__id', flat=True)

    @staticmethod
    def fetch_by_ids_with_files_and_keys(ids):
        return (
            Product.objects
            .prefetch_related('files', 'activation_keys')
            .filter(id__in=ids)
        )


class CategoryRepository:

    @staticmethod
    def fetch(first=False, limit=None, **kwargs):
        qs = Category.objects.filter(**kwargs)
        if first:
            return qs.first()
        elif limit:
            return qs[:limit]
        return qs


class TagRepository:

    @staticmethod
    def fetch(first=False, limit=None, **kwargs):
        qs = Tag.objects.filter(**kwargs)
        if first:
            return qs.first()
        elif limit:
            return qs[:limit]
        return qs


# TODO: Remove this
class ProductImageRepository:

    @staticmethod
    def prepare_feature_image_subquery(outer_ref='id'):
        '''Return first feature image subquery.'''
        return Subquery(
            ProductImage.objects
            .filter(product_id=OuterRef(outer_ref), is_feature=True)
            .values('image')[:1]
        )


class ProductFileRepository:

    @staticmethod
    def fetch(first=False, limit=None, **kwargs):
        qs = ProductFile.objects.filter(**kwargs)
        if first:
            return qs.first()
        elif limit:
            return qs[:limit]
        return qs


class OneTimeUrlRepository:

    @staticmethod
    def fetch(first=False, limit=None, **kwargs):
        qs = OneTimeUrl.objects.filter(**kwargs)
        if first:
            return qs.first()
        elif limit:
            return qs[:limit]
        return qs

    @staticmethod
    def delete(url):
        url.delete()

    @staticmethod
    def create(**kwargs):
        return OneTimeUrl.objects.create(**kwargs)
