import logging

from carts.utils import CartSessionManager
from carts.repositories import CartRepository
from carts import consts


logger = logging.getLogger('django')


class CartMiddlewareService:

    __slots__ = 'session_manager', 'request',

    def __init__(self, request):
        self.session_manager = CartSessionManager(request)
        self.request = request

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
            cart_id = new_cart.id
            logger.info(consts.NEW_CART_CREATED_MSG)
        return cart_id, forced

    def execute(self):
        cart_id, forced = self._get_or_create_cart_id()
        self.session_manager.set_cart_id_if_not_exists(cart_id, forced=forced)
