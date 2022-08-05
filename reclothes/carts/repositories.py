from carts.models import Cart, CartItem


class CartRepository:

    @staticmethod
    def get_filtered_queryset(**kwargs):
        return Cart.objects.filter(**kwargs)

    @staticmethod
    def create(*args, **kwargs):
        return Cart.objects.create(*args, **kwargs)

    @staticmethod
    def get(**kwargs):
        """Return non-deleted and non-archived cart."""
        return Cart.objects.filter(
            is_archived=False, is_deleted=False, **kwargs).first()

    @staticmethod
    def exists(**kwargs):
        return Cart.objects.filter(**kwargs).exists()

    @staticmethod
    def attach_user_to_cart(user_id, **kwargs):
        cart = Cart.objects.get(**kwargs)
        cart.user_id = user_id
        cart.save()

    @staticmethod
    def delete(full_delete=False, **kwargs):
        """
        Mark cart as deleted.

        If full_delete is True then completely delete cart.
        """
        cart = Cart.objects.get(**kwargs)
        if full_delete:
            cart.delete()
        else:
            cart.is_deleted = True
            cart.save()


class CartItemRepository:

    @staticmethod
    def get_filtered_queryset(**kwargs):
        return CartItem.objects.filter(**kwargs)

    @staticmethod
    def empty():
        return CartItem.objects.none()

    @staticmethod
    def annotate(qs, **kwargs):
        return qs.annotate(**kwargs)
