from django_filters import rest_framework as filters

from catalogue.models import Product


class CatalogueFilter(filters.FilterSet):
    price_from = filters.NumberFilter(
        field_name="regular_price",
        lookup_expr="gte"
    )
    price_to = filters.NumberFilter(
        field_name="regular_price",
        lookup_expr="lte"
    )

    class Meta:
        model = Product
        fields = [
            'tags',
            'category_id',
            'is_active',
            'product_type_id',
            'price_from',
            'price_to',
        ]
