from django.db.models import Count, F, Avg
from catalogue.models import Product, Category, Tag


class ProductRepository:

    @staticmethod
    def get_newest_products(num=10):
        """
        Return newest products limited by `num` param (10 by default).
        """
        return list(
            Product.objects
            .annotate(type=F("product_type__name"))
            .values("id", "title", "description", "type", "regular_price", "product_type")
            .order_by("-creation_date")[:num]
        )

    @staticmethod
    def get_hot_products(num=10):
        """
        Return `num` products with most number of purchases (10 by default).
        Number of purchases means count of order items.
        """
        return list(
            Product.objects
            .annotate(
                purchases=Count("cart_items__orderitem"),
                type=F("product_type__name")
            )
            .values("id", "title", "description", "regular_price", "type", "purchases")
            .order_by("-purchases")[:num]
        )

    @staticmethod
    def get_best_products(num=10):
        """
        Return `num` products with best reviews rating ratio (10 by default).
        """
        return list(
            Product.objects
            .annotate(
                avg_rate=Avg("reviews__rating"),
                type=F("product_type__name")
            )
            .values("id", "title", "description", "regular_price", "type", "avg_rate")
            .order_by("-avg_rate")[:num]
        )


class CategoryRepository:
    pass


class TagRepository:
    pass
