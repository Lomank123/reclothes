from django.db.models import Avg, Count, F, OuterRef, Q, Subquery

from catalogue.models import Category, Product, ProductImage, Tag


class ProductRepository:

    @staticmethod
    def fetch(single=False, **kwargs):
        qs = Product.objects.filter(**kwargs)
        if single:
            return qs.first()
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
        products = qs
        if limit:
            products = qs[:limit]
        return products

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
        products = qs
        if limit:
            products = qs[:limit]
        return products

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
        products = qs
        if limit:
            products = qs[:limit]
        return products


class CategoryRepository:

    @staticmethod
    def fetch(**kwargs):
        return Category.objects.filter(**kwargs)


class TagRepository:

    @staticmethod
    def fetch(**kwargs):
        return Tag.objects.filter(**kwargs)


class ProductImageRepository:

    @staticmethod
    def prepare_feature_image_subquery(outer_ref_value='id'):
        '''Return first feature image subquery.'''
        return Subquery(
            ProductImage.objects
            .filter(product_id=OuterRef(outer_ref_value), is_feature=True)
            .values('image')[:1]
        )
