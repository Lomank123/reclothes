from carts.consts import CART_ID_SESSION_KEY


class CartSessionManager:

    __slots__ = 'request',

    def __init__(self, request):
        self.request = request

    def load_cart_id_from_session(self):
        return self.request.session.get(CART_ID_SESSION_KEY, None)

    def set_cart_id_if_not_exists(self, cart_id, forced=False):
        if self.load_cart_id_from_session() and not forced:
            return
        self.request.session[CART_ID_SESSION_KEY] = cart_id
