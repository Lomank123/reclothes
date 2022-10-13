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

    def _fetch_session_cart(self):
        # We always have session cart id because of middleware
        cart_id = self.session_manager.load_cart_id_from_session()
        return CartRepository.fetch_active(first=True, id=cart_id)

    def _fetch_user_cart(self):
        user_id = self.session_manager.request.user.pk
        return CartRepository.fetch_active(first=True, user_id=user_id)

    def _attach_or_delete_session_cart(self, session_cart, user_cart):
        '''Return id of existing user cart or newly attached session one.'''
        cart_id = session_cart.pk
        if user_cart is None:
            CartRepository.attach_user_to_cart(
                session_cart, self.session_manager.request.user.pk)
            logger.info(USER_CART_NOT_FOUND_MSG)
        else:
            # Delete old cart
            CartRepository.delete(session_cart)
            logger.info(DELETE_OLD_CART_MSG)
            cart_id = user_cart.pk
        return cart_id

    def execute(self):
        session_cart = self._fetch_session_cart()
        user_cart = self._fetch_user_cart()
        cart_id = self._attach_or_delete_session_cart(session_cart, user_cart)
        self.session_manager.set_cart_id_if_not_exists(cart_id, forced=True)


class CustomUserViewSetService:

    def __init__(self, request):
        self.request = request

    def execute(self):
        return CustomUserRepository.fetch(id=self.request.user.pk)
