import logging

from carts.repositories import CartRepository
from carts.utils import CartSessionManager

from accounts.consts import USER_CART_NOT_FOUND_MSG, DELETE_OLD_CART_MSG
from accounts.repositories import CustomUserRepository


logger = logging.getLogger('django')


class LoginViewService:

    __slots__ = 'session_manager',

    def __init__(self, request):
        self.session_manager = CartSessionManager(request)

    def _get_user_cart_id(self):
        '''
        Get user cart which is not deleted or archived.
        If there's none, attach current cart to them.
        Otherwise return user cart id and delete recently created one.
        '''
        user_id = self.session_manager.request.user.pk
        user_cart = CartRepository.get(user_id=user_id)
        # We always have cart id because of middleware
        cart_id = self.session_manager.get_cart_id()
        cart = CartRepository.get(id=cart_id)
        if user_cart is None:
            CartRepository.attach_user_to_cart(cart, user_id)
            logger.info(USER_CART_NOT_FOUND_MSG)
        else:
            # Delete old cart
            CartRepository.delete(cart)
            logger.info(DELETE_OLD_CART_MSG)
            cart_id = user_cart.pk
        return cart_id

    def execute(self):
        cart_id = self._get_user_cart_id()
        self.session_manager.set_cart_id_if_not_exists(cart_id, forced=True)


class CustomUserViewSetService:

    def execute(self):
        return CustomUserRepository.fetch_all_users()
