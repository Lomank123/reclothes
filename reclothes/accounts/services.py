import logging

from carts.repositories import CartRepository
from carts.utils import CartSessionManager

from accounts.consts import DELETE_OLD_CART_MSG, USER_CART_NOT_FOUND_MSG

logger = logging.getLogger('django')


class LoginViewService:

    def __init__(self, request):
        self.session_manager = CartSessionManager(request)
        self.repository = CartRepository()

    def _attach_or_delete_session_cart(self, session_cart, user_cart):
        """Return id of existing user cart or newly attached session one."""
        cart_id = session_cart.pk
        if user_cart is None:
            session_cart.user = self.session_manager.request.user
            session_cart.save()
            logger.info(USER_CART_NOT_FOUND_MSG)
        else:
            # Delete old cart
            self.repository.delete(session_cart)
            logger.info(DELETE_OLD_CART_MSG)
            cart_id = user_cart.pk
        return cart_id

    def execute(self):
        session_cart_id = self.session_manager.load_cart_id_from_session()
        session_cart = self.repository.fetch_active(
            first=True, id=session_cart_id)
        user_id = self.session_manager.request.user.pk
        user_cart = self.repository.fetch_active(first=True, user_id=user_id)
        cart_id = self._attach_or_delete_session_cart(session_cart, user_cart)
        self.session_manager.set_cart_id_if_not_exists(cart_id, forced=True)
