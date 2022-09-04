from django.db.models import Count

from carts.models import Cart, CartItem


class CartRepository:

    @staticmethod
    def create(*args, **kwargs):
        return Cart.objects.create(*args, **kwargs)

    @staticmethod
    def fetch_active(single=False, limit=None, **kwargs):
        """
        Return non-deleted and non-archived cart qs with items count.

        Specify single param to return first object from qs.
        """
        qs = (
            Cart.objects
            .filter(is_archived=False, is_deleted=False, **kwargs)
            .annotate(items_count=Count('cart_items__id'))
        )
        if limit:
            return qs[:limit]
        if single:
            return qs.first()
        return qs

    @staticmethod
    def attach_user_to_cart(cart, user_id):
        cart.user_id = user_id
        cart.save()

    @staticmethod
    def delete(cart, full_delete=False):
        """
        Mark cart as deleted.

        If full_delete is True then completely delete cart.
        """
        if full_delete:
            cart.delete()
        else:
            cart.is_deleted = True
            cart.save()


class CartItemRepository:

    @staticmethod
    def fetch(single=False, limit=None, **kwargs):
        qs = CartItem.objects.filter(**kwargs).order_by('-id')
        if limit:
            return qs[:limit]
        elif single:
            return qs.first()
        return qs

    @staticmethod
    def empty():
        return CartItem.objects.none()

    @staticmethod
    def annotate(qs, **kwargs):
        return qs.annotate(**kwargs)

    @staticmethod
    def change_quantity(item, value):
        item.quantity = value
        item.save()
