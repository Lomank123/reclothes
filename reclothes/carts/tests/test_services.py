from datetime import timedelta

from accounts.models import CustomUser
from carts.consts import RECENT_CART_ITEMS_LIMIT
from carts.models import Cart, CartItem
from carts.services import (CartItemService, CartMiddlewareService,
                            CartService, ChangeQuantityService)
from catalogue.models import ActivationKey, Product, ProductType
from django.contrib import auth
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.backends.db import SessionStore
from django.test import RequestFactory, TestCase
from django.utils import timezone
from rest_framework.request import Request


def create_user(email=None, password='123123123Aa'):
    if email is None:
        return AnonymousUser()
    return CustomUser.objects.create(email=email, password=password)


def create_cart(user_id=None):
    return Cart.objects.create(user_id=user_id)


def create_cart_item(cart_id, product_id):
    return CartItem.objects.create(
        cart_id=cart_id, product_id=product_id)


def create_product_type(name):
    return ProductType.objects.create(name=name)


def create_product(type_id, title='test', regular_price=100.00, **kwargs):
    return Product.objects.create(
        product_type_id=type_id,
        title=title,
        regular_price=regular_price,
        **kwargs,
    )


def create_activation_key(product_id, key, **kwargs):
    expiry_date = timezone.now() + timedelta(days=1)
    return ActivationKey.objects.create(
        product_id=product_id, key=key, expired_at=expiry_date, **kwargs)


def create_session(user):
    '''
    Create and return new session.

    User must be either User or AnonymousUser object.
    '''
    session = SessionStore(None)
    session.clear()
    session.cycle_key()
    if user.is_authenticated:
        session[auth.SESSION_KEY] = user._meta.pk.value_to_string(user)
        session[auth.BACKEND_SESSION_KEY] = (
            'django.contrib.auth.backends.ModelBackend')
        session[auth.HASH_SESSION_KEY] = user.get_session_auth_hash()
    session.save()
    return session


def create_request(user=None, session=None):
    request = RequestFactory().request()
    request.user = user
    request.session = session
    return request


def create_post_request(path='/', data=dict()):
    return RequestFactory().post(path=path, data=data)


class CartMiddlewareServiceTestCase(TestCase):

    def test_anonymous_cart_create_and_set_to_session(self):
        user = create_user(email='test1@gmail.com')
        session = create_session(user)
        request = create_request(user, session)

        CartMiddlewareService(request).execute()

        self.assertTrue(request.session['cart_id'])
        self.assertEqual(Cart.objects.count(), 1)

    def test_cart_create_and_attach_to_user_and_set_to_session(self):
        user = create_user(email='test1@gmail.com')
        session = create_session(user)
        request = create_request(user, session)

        CartMiddlewareService(request).execute()

        self.assertEqual(Cart.objects.count(), 1)
        self.assertEqual(Cart.objects.filter(user=user).count(), 1)

    def test_user_cart_check_in_session(self):
        user = create_user(email='test1@gmail.com')
        session = create_session(user)
        cart = create_cart(user.pk)
        session['cart_id'] = cart.pk
        request = create_request(user, session)

        CartMiddlewareService(request).execute()

        self.assertEqual(Cart.objects.count(), 1)
        self.assertEqual(Cart.objects.filter(user=user).count(), 1)


class CartServiceTestCase(TestCase):

    @staticmethod
    def _delete_cart_by_id(cart_id):
        Cart.objects.get(id=cart_id).delete()

    def test_cart_retrieved(self):
        user = create_user()
        session = create_session(user)
        cart = create_cart()
        session['cart_id'] = cart.pk
        request = create_request(user, session)

        response = CartService(request).execute()
        data = response.data['data']

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data.get('id', False))

    def test_cart_not_found(self):
        user = create_user()
        session = create_session(user)
        cart = create_cart()
        session['cart_id'] = cart.pk
        request = create_request(user, session)
        self._delete_cart_by_id(cart.pk)

        response = CartService(request).execute()

        self.assertEqual(response.status_code, 400)
        self.assertTrue('detail' in response.data.keys())


class CartItemServiceTestCase(TestCase):

    @staticmethod
    def _create_rest_request():
        return Request(request=RequestFactory().request())

    def test_empty_cart_received(self):
        cart = create_cart()
        request = self._create_rest_request()

        response = CartItemService(request).execute(cart_id=cart.pk)
        data = response.data['data']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['cart_items']), 0)

    def test_paginated_cart_items_received(self):
        cart = create_cart()
        product_type = create_product_type('test1')
        product = create_product(type_id=product_type.pk)
        create_cart_item(cart.pk, product.pk)
        request = self._create_rest_request()

        response = CartItemService(request).execute(
            cart_id=cart.pk, paginate=True)
        data = response.data['data']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['cart_items']['results']), 1)
        self.assertTrue('image' in data['cart_items']['results'][0])
        self.assertTrue('product_title' in data['cart_items']['results'][0])

    def test_limited_cart_items_received(self):
        cart = create_cart()
        product_type = create_product_type('test1')
        product = create_product(type_id=product_type.pk)
        product2 = create_product(type_id=product_type.pk)
        product3 = create_product(type_id=product_type.pk)
        product4 = create_product(type_id=product_type.pk)
        product5 = create_product(type_id=product_type.pk)
        create_cart_item(cart.pk, product.pk)
        create_cart_item(cart.pk, product2.pk)
        create_cart_item(cart.pk, product3.pk)
        create_cart_item(cart.pk, product4.pk)
        create_cart_item(cart.pk, product5.pk)
        request = self._create_rest_request()

        response = CartItemService(request).execute(
            cart_id=cart.pk, limit=RECENT_CART_ITEMS_LIMIT)
        data = response.data['data']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['cart_items']), RECENT_CART_ITEMS_LIMIT)


class ChangeQuantityServiceTestCase(TestCase):

    def test_cart_item_quantity_changed(self):
        # Arrange
        product_type = create_product_type(name="type1")
        product = create_product(product_type.pk)
        create_activation_key(product.pk, key="1")
        create_activation_key(product.pk, key="2")
        cart = create_cart()
        cart_item = create_cart_item(cart.pk, product.pk)

        post_data = {
            'value': cart_item.quantity + 1,
            'cart_item_id': cart_item.pk,
            'product_id': product.pk,
        }
        request = create_post_request(data=post_data)

        # Act
        response = ChangeQuantityService(request).execute()

        # Assert
        data = response.data['data']
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data.get('value', False))
        self.assertEqual(data['value'], 2)
        self.assertEqual(CartItem.objects.get(id=cart_item.pk).quantity, 2)

    def test_new_quantity_too_little(self):
        # Arrange
        product_type = create_product_type(name="type1")
        product = create_product(product_type.pk)
        cart = create_cart()
        cart_item = create_cart_item(cart.pk, product.pk)

        post_data = {
            'value': cart_item.quantity - 1,
            'cart_item_id': cart_item.pk,
            'product_id': product.pk,
        }
        request = create_post_request(data=post_data)

        # Act
        response = ChangeQuantityService(request).execute()

        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertTrue('detail' in response.data.keys())
        self.assertEqual(CartItem.objects.get(id=cart_item.pk).quantity, 1)

    def test_new_quantity_more_than_max_possible(self):
        # Arrange
        product_type = create_product_type(name="type1")
        product = create_product(type_id=product_type.pk)
        create_activation_key(product.pk, key="1")

        cart = create_cart()
        cart_item = create_cart_item(cart.pk, product.pk)

        post_data = {
            'value': cart_item.quantity + 1,
            'cart_item_id': cart_item.pk,
            'product_id': product.pk,
        }
        request = create_post_request(data=post_data)

        # Act
        response = ChangeQuantityService(request).execute()

        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertTrue('detail' in response.data.keys())
        self.assertEqual(CartItem.objects.get(id=cart_item.pk).quantity, 1)
