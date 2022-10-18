from django.db import models

from catalogue.selectors import ImageSubquerySelector


class CartItemQuerySet(models.QuerySet):

    def annotate_product_with_image(self):
        """Annotate feature image and product fields."""
        if not self.exists():
            return self

        img_subquery = ImageSubquerySelector.build_subquery(
            outer_ref='product_id')
        data = {
            'product_title': models.F('product__title'),
            'product_is_limited': models.F('product__keys_limit'),
            'image': img_subquery,
        }
        return self.annotate(**data)

    def available(self, request):
        """Return available items based on whether user is authenticated."""
        user = request.user
        if user.is_authenticated:
            return self.filter(cart__user=user)
        # Anonymous users can access only their current cart
        current_cart_id = request.session.get('cart_id', None)
        return self.filter(id=current_cart_id)
