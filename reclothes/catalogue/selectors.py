from django.db.models import OuterRef, Subquery

from catalogue.models import ProductImage


class ImageSubquerySelector:
    """Return ProductImage subquery with feature image."""

    @staticmethod
    def build_subquery(outer_ref='id'):
        return Subquery(
            ProductImage.objects
            .filter(product_id=OuterRef(outer_ref), is_feature=True)
            .values('image')[:1]
        )
