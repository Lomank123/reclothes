from django.db.models import Avg, Count, F, OuterRef, Q, Subquery

from catalogue.models import Category, Product, ProductImage, Tag, ProductFile


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
    def fetch_active_with_category():
        return (
            Product.objects
            .select_related('category')
            .filter(
                (Q(is_active=True) & Q(quantity__gt=0)) |
                Q(is_limited=False)
            )
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
    def fetch_newest_products(img_subquery, limit=None):
        '''Return newest active products.'''
        qs = (
            Product.objects
            .filter(
                (Q(is_active=True) & Q(quantity__gt=0)) |
                Q(is_limited=False)
            )
            .annotate(
                type=F('product_type__name'), feature_image=img_subquery)
            .values(
                'id',
                'title',
                'description',
                'type',
                'regular_price',
                'product_type',
                'feature_image',
            )
            .order_by('-created_at')
        )
        if limit:
            return qs[:limit]
        return qs

    @staticmethod
    def fetch_hot_products(img_subquery, limit=None):
        '''
        Get active products with most number of purchases.

        Number of purchases means count of order items.
        '''
        qs = (
            Product.objects
            .filter(
                (Q(is_active=True) & Q(quantity__gt=0)) |
                Q(is_limited=False)
            )
            .annotate(
                purchases=Count('cart_items__orderitem'),
                type=F('product_type__name'),
                feature_image=img_subquery,
            )
            .values(
                'id',
                'title',
                'description',
                'regular_price',
                'type',
                'purchases',
                'feature_image',
            )
            .order_by('-purchases')
        )
        if limit:
            return qs[:limit]
        return qs

    @staticmethod
    def fetch_best_products(img_subquery, limit=None):
        '''Get active products with best reviews rating ratio.'''
        qs = (
            Product.objects
            .filter(
                (Q(is_active=True) & Q(quantity__gt=0)) |
                Q(is_limited=False)
            )
            .annotate(
                avg_rate=Avg('reviews__rating'),
                type=F('product_type__name'),
                feature_image=img_subquery,
            )
            .values(
                'id',
                'title',
                'description',
                'regular_price',
                'type',
                'avg_rate',
                'feature_image',
            )
            .order_by('-avg_rate')
        )
        if limit:
            return qs[:limit]
        return qs

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


class ProductImageRepository:

    @staticmethod
    def prepare_feature_image_subquery(outer_ref_value='id'):
        '''Return first feature image subquery.'''
        return Subquery(
            ProductImage.objects
            .filter(product_id=OuterRef(outer_ref_value), is_feature=True)
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
