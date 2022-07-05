from django.db.models import Subquery, F, Count

from carts.models import Cart


class CartRepository:

    @staticmethod
    def create(*args, **kwargs):
        return Cart.objects.create(*args, **kwargs)

    @staticmethod
    def get_by_id(cart_id):
        """
        Return non-deleted and non-archived cart by its id.
        """
        return (
            Cart.objects
            .filter(id=cart_id, is_archived=False, is_deleted=False)
            .annotate(cart_items_count=Count('cart_items'))
            .first()
        )

    @staticmethod
    def is_cart_exists_by_id(cart_id):
        return Cart.objects.filter(id=cart_id).exists()

    @staticmethod
    def get_current_by_user_id(user_id):
        """
        Return current not deleted or archived cart by user id.
        """
        return Cart.objects.filter(user_id=user_id, is_deleted=False, is_archived=False).first()

    @staticmethod
    def attach_user_to_cart_by_id(cart_id, user_id):
        cart = Cart.objects.get(id=cart_id)
        cart.user_id = user_id
        cart.save()

    @staticmethod
    def delete_by_id(cart_id, full_delete=False):
        """
        Mark cart as deleted or if full_delete is True then completely delete cart object.
        """
        cart = Cart.objects.get(id=cart_id)
        if full_delete:
            cart.delete()
        else:
            cart.is_deleted = True
            cart.save()

    @staticmethod
    def get_cart_items(cart):
        """
        Return cart items by cart object.
        """
        return cart.cart_items.all()


class CartItemRepository:

    @staticmethod
    def attach_feature_image(qs, img_subquery):
        """
        Annotate image to cart item queryset.
        """
        return qs.annotate(image=Subquery(img_subquery))

    @staticmethod
    def attach_product_info(qs):
        """
        Annotate product info to cart item queryset.
        """
        return qs.annotate(product_title=F('product__title'))
