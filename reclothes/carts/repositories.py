from carts.models import Cart


class CartRepository:

    @staticmethod
    def create(*args, **kwargs):
        return Cart.objects.create(*args, **kwargs)

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
