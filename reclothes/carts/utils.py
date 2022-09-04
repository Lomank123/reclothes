class CartSessionManager:

    __slots__ = 'request',

    def __init__(self, request):
        self.request = request

    def load_cart_id_from_session(self):
        return self.request.session.get("cart_id", None)

    def set_cart_id_if_not_exists(self, cart_id, forced=False):
        if self.load_cart_id_from_session() and not forced:
            return
        self.request.session["cart_id"] = cart_id
