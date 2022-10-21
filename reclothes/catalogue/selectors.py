import collections

from django.db.models import OuterRef, Subquery

from catalogue.consts import MOST_POPULAR_TAGS_LIMIT
from catalogue.models import ProductImage, Tag


class ImageSubquerySelector:
    """Return ProductImage subquery with feature image."""

    @staticmethod
    def build_subquery(outer_ref='id'):
        return Subquery(
            ProductImage.objects
            .filter(product_id=OuterRef(outer_ref), is_feature=True)
            .values('image')[:1]
        )


class PopularTagSelector:
    """Return popular tags based on products queryset."""

    @staticmethod
    def select(products, limit=MOST_POPULAR_TAGS_LIMIT):
        tags_ids = products.filter(tags__isnull=False).values_list(
            'tags__id', flat=True)
        counter = collections.Counter(tags_ids)
        popular_ids = [key for key, _ in counter.most_common(limit)]
        return Tag.objects.filter(id__in=popular_ids)
