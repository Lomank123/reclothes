from django.db.models import Avg, Count, F, Subquery, OuterRef

from catalogue.models import Product, ProductImage, Category, Tag


class ProductRepository:

    @staticmethod
    def fetch_qs(**kwargs):
        return Product.objects.filter(**kwargs)

    @staticmethod
    def get_active_with_category():
        return (
            Product.objects
            .select_related('category')
            .filter(is_active=True)
        )

    @staticmethod
    def get_detail(**kwargs):
        """Return product with average rating."""
        return (
            Product.objects
            .select_related('category', 'product_type')
            .filter(**kwargs)
            .annotate(avg_rate=Avg("reviews__rating"))
            .first()
        )

    @staticmethod
    def get_values_list(products, field_name, flat=True):
        """Return values list without nulls based on field name."""
        return products.filter(tags__isnull=False).values_list(
            field_name, flat=flat)

    @staticmethod
    def get_newest_products(image, limit=None):
        """
        Return newest active products.

        Limit by specifying `limit` param.
        """
        qs = (
            Product.objects
            .filter(is_active=True)
            .annotate(
                type=F("product_type__name"), feature_image=Subquery(image))
            .values(
                "id",
                "title",
                "description",
                "type",
                "regular_price",
                "product_type",
                "feature_image",
            )
            .order_by("-created_at")
        )
        products = qs
        if limit:
            products = qs[:limit]
        return products

    @staticmethod
    def get_hot_products(image, limit=None):
        """
        Get active products with most number of purchases.

        Limit by specifying `limit` param.
        Number of purchases means count of order items.
        """
        qs = (
            Product.objects
            .filter(is_active=True)
            .annotate(
                purchases=Count("cart_items__orderitem"),
                type=F("product_type__name"),
                feature_image=Subquery(image),
            )
            .values(
                "id",
                "title",
                "description",
                "regular_price",
                "type",
                "purchases",
                "feature_image",
            )
            .order_by("-purchases")
        )
        products = qs
        if limit:
            products = qs[:limit]
        return products

    @staticmethod
    def get_best_products(image, limit=None):
        """
        Get active products with best reviews rating ratio.

        Limit by specifying `limit` param.
        """
        qs = (
            Product.objects
            .filter(is_active=True)
            .annotate(
                avg_rate=Avg("reviews__rating"),
                type=F("product_type__name"),
                feature_image=Subquery(image),
            )
            .values(
                "id",
                "title",
                "description",
                "regular_price",
                "type",
                "avg_rate",
                "feature_image",
            )
            .order_by("-avg_rate")
        )
        products = qs
        if limit:
            products = qs[:limit]
        return products


class CategoryRepository:

    @staticmethod
    def fetch_qs(**kwargs):
        return Category.objects.filter(**kwargs)


class TagRepository:

    @staticmethod
    def get_by_ids(ids):
        return Tag.objects.filter(id__in=ids)

    @staticmethod
    def get_all():
        return Tag.objects.all()


class ProductImageRepository:

    @staticmethod
    def fetch_feature_image_by_product_id(
        product_id=None,
        subquery=False,
        outer_ref_value="id"
    ):
        """
        Return first feature image.

        Set subquery=True to return subquery.
        """
        ref_id = product_id
        if subquery:
            ref_id = OuterRef(outer_ref_value)
        elif product_id is None:
            raise AttributeError(
                "If subquery is False product_id must not be None.")
        return ProductImage.objects.filter(
            product_id=ref_id, is_feature=True).values('image')[:1]
