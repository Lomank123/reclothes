from django.db.models import Avg, Count, F

from catalogue.models import Product


class ProductRepository:

    @staticmethod
    def get_newest_products(limit=None):
        """
        Return newest active products. Limit by specifying `limit` param.
        """
        qs = (
            Product.objects
            .filter(is_active=True)
            .annotate(type=F("product_type__name"))
            .values("id", "title", "description", "type", "regular_price", "product_type")
            .order_by("-creation_date")
        )
        products = qs
        if limit:
            products = qs[:limit]
        return products

    @staticmethod
    def get_hot_products(limit=None):
        """
        Return active products with most number of purchases. Limit by specifying `limit` param.
        Number of purchases means count of order items.
        """
        qs = (
            Product.objects
            .filter(is_active=True)
            .annotate(purchases=Count("cart_items__orderitem"), type=F("product_type__name"))
            .values("id", "title", "description", "regular_price", "type", "purchases")
            .order_by("-purchases")
        )
        products = qs
        if limit:
            products = qs[:limit]
        return products

    @staticmethod
    def get_best_products(limit=None):
        """
        Return active products with best reviews rating ratio. Limit by specifying `limit` param.
        """
        qs = (
            Product.objects
            .filter(is_active=True)
            .annotate(avg_rate=Avg("reviews__rating"), type=F("product_type__name"))
            .values("id", "title", "description", "regular_price", "type", "avg_rate")
            .order_by("-avg_rate")
        )
        products = qs
        if limit:
            products = qs[:limit]
        return products

    @staticmethod
    def get_by_id(product_id):
        return (
            Product.objects
            .select_related('category', 'product_type')
            .filter(id=product_id)
            .first()
        )

    @staticmethod
    def get_product_attrs(product_id):
        return (
            Product.objects
            .filter(id=product_id)
            .annotate(attr_name=F("attr_values__attribute__name"), attr_value=F("attr_values__value"))
            .values("attr_name", "attr_value")
        )


class CategoryRepository:
    pass


class TagRepository:
    pass


class ProductTypeRepository:
    pass
