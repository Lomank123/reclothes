class CartSessionManager:

    __slots__ = 'request',

    def __init__(self, request):
        self.request = request

    def get_cart_id(self):
        return self.request.session.get("cart_id", None)

    def set_cart_id_if_not_exists(self, cart_id, forced=False):
        if self.get_cart_id() and not forced:
            return
        self.request.session["cart_id"] = cart_id
