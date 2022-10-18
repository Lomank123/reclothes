from django.shortcuts import get_object_or_404

from carts.models import Cart
from carts.utils import CartSessionManager


class CurrentCartSelector:
    """Return cart which id is in current session."""

    __slots__ = 'session_manager',

    def __init__(self, request):
        self.session_manager = CartSessionManager(request)

    def select(self):
        cart_id = self.session_manager.load_cart_id_from_session()
        return get_object_or_404(Cart.active, id=cart_id)
