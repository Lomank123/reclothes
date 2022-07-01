import logging

from carts import consts
from carts.repositories import CartRepository
from carts.utils import CartSessionManager


logger = logging.getLogger('django')


class CartMiddlewareService:

    __slots__ = 'session_manager',

    def __init__(self, request):
        self.session_manager = CartSessionManager(request)

    def _get_or_create_cart_id(self):
        """
        Return cart id if it's in current session. Otherwise create new cart
        and return it's id. Also return flag whether to update session value.
        """
        cart_id = self.session_manager.get_cart_id()
        forced = False
        exists = CartRepository.is_cart_exists_by_id(cart_id)
        if not exists:
            forced = True
            new_cart = CartRepository.create()
            logger.info(consts.NEW_CART_CREATED_MSG)
            # In case user cart is gone
            user = self.session_manager.request.user
            if user.is_authenticated:
                CartRepository.attach_user_to_cart_by_id(new_cart.id, user.id)
                logger.info(consts.NEW_CART_ATTACHED_MSG)
            cart_id = new_cart.id
        return cart_id, forced

    def execute(self):
        cart_id, forced = self._get_or_create_cart_id()
        self.session_manager.set_cart_id_if_not_exists(cart_id, forced=forced)
