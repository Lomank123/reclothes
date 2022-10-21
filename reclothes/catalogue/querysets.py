from django.db import models


class ProductQuerySet(models.QuerySet):

    def detailed(self):
        return (
            self.select_related('category', 'product_type')
            .annotate(avg_rate=models.Avg('reviews__rating'))
        )

    def best(self):
        """Products with best reviews rating ratio."""
        return (
            self.annotate(
                avg_rate=models.Avg('reviews__rating'),
                type=models.F('product_type__name'),
            )
            .order_by('-avg_rate')
        )

    def hot(self, limit=None):
        """
        Products with most number of purchases.

        Number of purchases means count of order items.
        """
        return (
            self.annotate(
                purchases=models.Count('cart_items__orderitem'),
                type=models.F('product_type__name'),
            )
            .order_by('-purchases')
        )

    def newest(self, limit=None):
        return (
            self.annotate(type=models.F('product_type__name'))
            .order_by('-created_at')
        )
