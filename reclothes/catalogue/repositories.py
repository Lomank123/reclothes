from django.db.models import Avg, Count, F, Subquery, OuterRef

from catalogue.models import Product, ProductImage


class ProductRepository:

    @staticmethod
    def get_newest_products(image, limit=None):
        """
        Return newest active products. Limit by specifying `limit` param.
        """
        qs = (
            Product.objects
            .filter(is_active=True)
            .annotate(type=F("product_type__name"))
            .annotate(feature_image=Subquery(image))
            .values("id", "title", "description", "type", "regular_price", "product_type", "feature_image")
            .order_by("-creation_date")
        )
        products = qs
        if limit:
            products = qs[:limit]
        return products

    @staticmethod
    def get_hot_products(image, limit=None):
        """
        Return active products with most number of purchases. Limit by specifying `limit` param.
        Number of purchases means count of order items.
        """
        qs = (
            Product.objects
            .filter(is_active=True)
            .annotate(purchases=Count("cart_items__orderitem"), type=F("product_type__name"))
            .annotate(feature_image=Subquery(image))
            .values("id", "title", "description", "regular_price", "type", "purchases", "feature_image")
            .order_by("-purchases")
        )
        products = qs
        if limit:
            products = qs[:limit]
        return products

    @staticmethod
    def get_best_products(image, limit=None):
        """
        Return active products with best reviews rating ratio. Limit by specifying `limit` param.
        """
        qs = (
            Product.objects
            .filter(is_active=True)
            .annotate(avg_rate=Avg("reviews__rating"), type=F("product_type__name"))
            .annotate(feature_image=Subquery(image))
            .values("id", "title", "description", "regular_price", "type", "avg_rate", "feature_image")
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
            .annotate(avg_rate=Avg("reviews__rating"))
            .first()
        )


class CategoryRepository:
    pass


class TagRepository:
    pass


class ProductTypeRepository:
    pass


class ProductImageRepository:

    @staticmethod
    def get_feature_image_by_product_id(product_id=None, subquery=False):
        """
        Return first feature image. Set subquery=True to return subquery.
        """
        ref_id = product_id
        if subquery:
            ref_id = OuterRef('id')
        elif product_id is None:
            raise AttributeError("If subquery is False product_id must not be None.")
        return (
            ProductImage.objects
            .filter(product_id=ref_id, is_feature=True)
            .values('image')[:1]
        )
