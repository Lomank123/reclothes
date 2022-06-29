from carts.models import Cart


class CartRepository:

    @staticmethod
    def create(*args, **kwargs):
        return Cart.objects.create(*args, **kwargs)

    @staticmethod
    def is_cart_exists_by_id(cart_id):
        return Cart.objects.filter(id=cart_id).exists()
