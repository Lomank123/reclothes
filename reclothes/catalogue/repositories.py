from django.db.models import Avg, Count, F, OuterRef, Q, Subquery
from django.utils import timezone
from reclothes.repositories import BaseRepository

from catalogue.models import (Category, OneTimeUrl, Product, ProductImage,
                              ProductReview, Tag)


class ProductRepository(BaseRepository):

    def __init__(self):
        super().__init__(Product)

    def fetch_active(self, first=False, limit=None, **kwargs):
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
            self.model.objects
            .annotate(keys_diff=active_keys_count - F('keys_limit'))
            .filter(active_products)
            .order_by('-id')
        )
        if first:
            return qs.first()
        elif limit:
            return qs[:limit]
        return qs

    def fetch_single_detailed(self, **kwargs):
        """Return product with average rating and related category and type."""
        return (
            self.model.objects
            .select_related('category', 'product_type')
            .filter(**kwargs)
            .annotate(avg_rate=Avg('reviews__rating'))
            .first()
        )

    def fetch_newest_products(self, img_subquery, limit=None):
        """Return newest active products."""
        qs = (
            self.fetch_active()
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

    def fetch_hot_products(self, img_subquery, limit=None):
        """
        Get active products with most number of purchases.

        Number of purchases means count of order items.
        """
        qs = (
            self.fetch_active()
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

    def fetch_best_products(self, img_subquery, limit=None):
        """Get active products with best reviews rating ratio."""
        qs = (
            self.fetch_active()
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

    def fetch_by_ids_with_files_and_keys(self, ids):
        return (
            self.model.objects
            .prefetch_related('files', 'activation_keys')
            .filter(id__in=ids)
        )


class CategoryRepository(BaseRepository):

    def __init__(self):
        super().__init__(Category)


class TagRepository(BaseRepository):

    def __init__(self):
        super().__init__(Tag)


class ProductImageRepository(BaseRepository):

    def __init__(self):
        super().__init__(ProductImage)

    def prepare_feature_image_subquery(self, outer_ref='id'):
        """Return first feature image subquery."""
        return Subquery(
            self.model.objects
            .filter(product_id=OuterRef(outer_ref), is_feature=True)
            .values('image')[:1]
        )


class OneTimeUrlRepository(BaseRepository):

    def __init__(self):
        super().__init__(OneTimeUrl)


class ProductReviewRepository(BaseRepository):

    def __init__(self):
        super().__init__(ProductReview)
