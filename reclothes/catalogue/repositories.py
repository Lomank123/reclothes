from django.db.models import Avg, Count, F, Subquery, OuterRef

from catalogue.models import Product, ProductImage, Category, Tag


class ProductRepository:

    @staticmethod
    def get_active():
        return Product.objects.filter(is_active=True)

    @staticmethod
    def get_active_with_category():
        return (
            Product.objects
            .select_related('category')
            .filter(is_active=True)
        )

    @staticmethod
    def get_by_id(product_id):
        """
        Return product with selected related and annotated average rating.
        """
        return (
            Product.objects
            .select_related('category', 'product_type')
            .filter(id=product_id)
            .annotate(avg_rate=Avg("reviews__rating"))
            .first()
        )

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
            .values(
                "id",
                "title",
                "description",
                "type",
                "regular_price",
                "product_type",
                "feature_image"
            )
            .order_by("-creation_date")
        )
        products = qs
        if limit:
            products = qs[:limit]
        return products

    @staticmethod
    def get_hot_products(image, limit=None):
        """
        Return active products with most number of purchases.
        Limit by specifying `limit` param.
        Number of purchases means count of order items.
        """
        qs = (
            Product.objects
            .filter(is_active=True)
            .annotate(
                purchases=Count("cart_items__orderitem"),
                type=F("product_type__name")
            )
            .annotate(feature_image=Subquery(image))
            .values(
                "id",
                "title",
                "description",
                "regular_price",
                "type",
                "purchases",
                "feature_image"
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
        Return active products with best reviews rating ratio.
        Limit by specifying `limit` param.
        """
        qs = (
            Product.objects
            .filter(is_active=True)
            .annotate(
                avg_rate=Avg("reviews__rating"),
                type=F("product_type__name")
            )
            .annotate(feature_image=Subquery(image))
            .values(
                "id",
                "title",
                "description",
                "regular_price",
                "type",
                "avg_rate",
                "feature_image"
            )
            .order_by("-avg_rate")
        )
        products = qs
        if limit:
            products = qs[:limit]
        return products

    @staticmethod
    def get_values_with_attrs(product):
        """
        Return queryset of attrs with values by product.
        """
        return product.attr_values.select_related('attribute')

    @staticmethod
    def get_reviews_with_user(product):
        """
        Return queryset of reviews with user info by product ordered by date.
        """
        return (
            product.reviews
            .select_related('user')
            .order_by('-creation_date')
        )

    @staticmethod
    def get_images(product):
        """
        Return product images ordered by is_feature.
        """
        return product.images.order_by('-is_feature')


class CategoryRepository:

    @staticmethod
    def get_active():
        return Category.objects.filter(is_active=True)

    @staticmethod
    def get_by_id(id):
        return Category.objects.filter(id=id).first()

    @staticmethod
    def get_roots():
        return Category.objects.filter(parent__isnull=True)


class TagRepository:

    @staticmethod
    def get_all():
        return Tag.objects.all()


class ProductTypeRepository:
    pass


class ProductImageRepository:

    @staticmethod
    def get_feature_image_by_product_id(
        product_id=None,
        subquery=False,
        outer_ref_value="id"
    ):
        """
        Return first feature image. Set subquery=True to return subquery.
        """
        ref_id = product_id
        if subquery:
            ref_id = OuterRef(outer_ref_value)
        elif product_id is None:
            raise AttributeError(
                "If subquery is False product_id must not be None."
            )
        return (
            ProductImage.objects
            .filter(product_id=ref_id, is_feature=True)
            .values('image')[:1]
        )


class ProductAttributeValueRepository:
    pass
