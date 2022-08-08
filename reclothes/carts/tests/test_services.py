from accounts.models import CustomUser
from carts.models import Cart, CartItem
from carts.services import CartMiddlewareService, CartService
from catalogue.models import Product, ProductType
from django.contrib import auth
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.backends.db import SessionStore
from django.test import RequestFactory, TestCase


def create_user(username=None, password="123123123Aa"):
    """
    Create and return user. If username is none then return AnonymousUser.
    """
    if username is None:
        return AnonymousUser()
    return CustomUser.objects.create(username=username, password=password)


def create_cart(user_id=None):
    return Cart.objects.create(user_id=user_id)


def create_session(user):
    """
    Create and return new session. User must be either User or AnonymousUser object.
    """
    session = SessionStore(None)
    session.clear()
    session.cycle_key()
    if user.is_authenticated:
        session[auth.SESSION_KEY] = user._meta.pk.value_to_string(user)
        session[auth.BACKEND_SESSION_KEY] = 'django.contrib.auth.backends.ModelBackend'
        session[auth.HASH_SESSION_KEY] = user.get_session_auth_hash()
    session.save()
    return session


def create_request(user=None, session=None):
    request = RequestFactory().request()
    request.user = user
    request.session = session
    return request


class CartMiddlewareServiceTestCase(TestCase):

    def test_anonymous_cart_create_and_set_to_session(self):
        user = create_user(username="test1")
        session = create_session(user)
        request = create_request(user, session)

        CartMiddlewareService(request).execute()

        self.assertTrue(request.session["cart_id"])
        self.assertEqual(Cart.objects.count(), 1)

    def test_cart_create_and_attach_to_user_and_set_to_session(self):
        user = create_user(username="test1")
        session = create_session(user)
        request = create_request(user, session)

        CartMiddlewareService(request).execute()

        self.assertEqual(Cart.objects.count(), 1)
        self.assertEqual(Cart.objects.filter(user=user).count(), 1)

    def test_user_cart_check_in_session(self):
        user = create_user(username="test1")
        session = create_session(user)
        cart = create_cart(user.pk)
        session["cart_id"] = cart.pk
        request = create_request(user, session)

        CartMiddlewareService(request).execute()

        self.assertEqual(Cart.objects.count(), 1)
        self.assertEqual(Cart.objects.filter(user=user).count(), 1)


class CartServiceTestCase(TestCase):

    @staticmethod
    def _create_cart_item(cart_id, product_id):
        return CartItem.objects.create(cart_id=cart_id, product_id=product_id)

    @staticmethod
    def _create_product_type(name):
        return ProductType.objects.create(name=name)

    @staticmethod
    def _create_product(type_id, title="test", quantity=10, regular_price=100.00):
        return Product.objects.create(
            product_type_id=type_id,
            title=title,
            quantity=quantity,
            regular_price=regular_price
        )

    @staticmethod
    def _delete_cart_by_id(cart_id):
        Cart.objects.get(id=cart_id).delete()

    def test_empty_cart_received(self):
        user = create_user()
        session = create_session(user)
        cart = create_cart()
        session["cart_id"] = cart.pk
        request = create_request(user, session)

        response = CartService(request).execute()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(len(response.data["cart_items"]), 0)

    def test_filled_cart_received(self):
        user = create_user()
        session = create_session(user)
        cart = create_cart()
        product_type = self._create_product_type("test1")
        product = self._create_product(type_id=product_type.pk)
        self._create_cart_item(cart.pk, product.pk)
        session["cart_id"] = cart.pk
        request = create_request(user, session)

        response = CartService(request).execute()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["cart_items"]), 1)
        self.assertTrue("image" in response.data["cart_items"][0])
        self.assertTrue("product_title" in response.data["cart_items"][0])

    def test_cart_not_found(self):
        user = create_user()
        session = create_session(user)
        cart = create_cart()
        session["cart_id"] = cart.pk
        request = create_request(user, session)
        self._delete_cart_by_id(cart.pk)

        response = CartService(request).execute()

        self.assertEqual(response.status_code, 404)
