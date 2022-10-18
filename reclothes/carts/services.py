from carts.models import Cart
from carts.utils import CartSessionManager


class CartToSessionService:
    """
    Set cart id to session after successful login.

    Depending on whether user has active cart, current session cart
    can be either deleted or attached.
    """

    def __init__(self, request):
        self.request = request
        self.session_manager = CartSessionManager(request)

    def _attach_or_delete_session_cart(self, session_cart, user_cart):
        """Return id of existing user cart or newly attached session one."""
        cart_id = session_cart.pk
        if user_cart is None:
            # Attach session cart to user
            session_cart.user = self.request.user
            session_cart.save()
        else:
            # Delete old cart
            session_cart.soft_delete()
            cart_id = user_cart.pk
        return cart_id

    def execute(self):
        session_cart_id = self.session_manager.load_cart_id_from_session()
        session_cart = Cart.active.filter(id=session_cart_id).first()
        user_cart = Cart.active.filter(user=self.request.user).first()
        cart_id = self._attach_or_delete_session_cart(session_cart, user_cart)
        self.session_manager.set_cart_id_if_not_exists(cart_id, forced=True)


class CartMiddlewareService:

    def __init__(self, request):
        self.request = request
        self.session_manager = CartSessionManager(request)

    def _check_or_create_cart(self, session_cart):
        forced = False
        if session_cart is None:
            forced = True
            user = self.request.user
            if user.is_authenticated:
                user_cart = Cart.active.filter(user=user).first()
                if user_cart is None:
                    new_user_cart = Cart.objects.create(user_id=user.pk)
                    cart = new_user_cart
                else:
                    cart = user_cart
            else:
                new_cart = Cart.objects.create()
                cart = new_cart
        else:
            cart = session_cart
        return cart, forced

    def execute(self):
        session_cart_id = self.session_manager.load_cart_id_from_session()
        session_cart = Cart.active.filter(id=session_cart_id).first()
        cart, forced = self._check_or_create_cart(session_cart)
        self.session_manager.set_cart_id_if_not_exists(cart.pk, forced=forced)
