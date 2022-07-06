import logging

from carts.repositories import CartRepository
from carts.utils import CartSessionManager

from accounts import consts


logger = logging.getLogger('django')


class LoginViewService:

    __slots__ = 'session_manager',

    def __init__(self, request):
        self.session_manager = CartSessionManager(request)

    def _get_user_cart_id(self):
        """
        Get user cart which is not deleted or archived.
        If there's none, attach current cart to them.
        Otherwise return user cart id and delete recently created one.
        """
        user_id = self.session_manager.request.user.id
        user_cart = CartRepository.get_current_by_user_id(user_id)
        # We always have cart id because of middleware
        cart_id = self.session_manager.get_cart_id()
        if user_cart is None:
            CartRepository.attach_user_to_cart_by_id(cart_id, user_id)
            logger.info(consts.USER_CART_NOT_FOUND_MSG)
        else:
            # Delete old cart
            CartRepository.delete_by_id(cart_id)
            logger.info(consts.DELETE_OLD_CART_MSG)
            cart_id = user_cart.id
        return cart_id

    def execute(self):
        cart_id = self._get_user_cart_id()
        self.session_manager.set_cart_id_if_not_exists(cart_id, forced=True)
