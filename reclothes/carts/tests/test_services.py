from carts.consts import RECENT_CART_ITEMS_LIMIT
from carts.models import Cart, CartItem
from carts.services import (CartItemService, CartMiddlewareService,
                            CartService, ChangeQuantityService)
from django.test import TestCase
from reclothes.tests import factory


class CartMiddlewareServiceTestCase(TestCase):

    def test_anonymous_cart_create_and_set_to_session(self):
        user = factory.create_user(email='test1@gmail.com')
        session = factory.create_session(user)
        request = factory.create_request(user, session)

        CartMiddlewareService(request).execute()

        self.assertTrue(request.session['cart_id'])
        self.assertEqual(Cart.objects.count(), 1)

    def test_cart_create_and_attach_to_user_and_set_to_session(self):
        user = factory.create_user(email='test1@gmail.com')
        session = factory.create_session(user)
        request = factory.create_request(user, session)

        CartMiddlewareService(request).execute()

        self.assertEqual(Cart.objects.count(), 1)
        self.assertEqual(Cart.objects.filter(user=user).count(), 1)

    def test_user_cart_check_in_session(self):
        user = factory.create_user(email='test1@gmail.com')
        session = factory.create_session(user)
        cart = factory.create_cart(user.pk)
        session['cart_id'] = cart.pk
        request = factory.create_request(user, session)

        CartMiddlewareService(request).execute()

        self.assertEqual(Cart.objects.count(), 1)
        self.assertEqual(Cart.objects.filter(user=user).count(), 1)


class CartServiceTestCase(TestCase):

    @staticmethod
    def _delete_cart_by_id(cart_id):
        Cart.objects.get(id=cart_id).delete()

    def test_cart_retrieved(self):
        user = factory.create_user()
        session = factory.create_session(user)
        cart = factory.create_cart()
        session['cart_id'] = cart.pk
        request = factory.create_request(user, session)

        response = CartService(request).execute()
        data = response.data['data']

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data.get('id', False))

    def test_cart_not_found(self):
        user = factory.create_user()
        session = factory.create_session(user)
        cart = factory.create_cart()
        session['cart_id'] = cart.pk
        request = factory.create_request(user, session)
        self._delete_cart_by_id(cart.pk)

        response = CartService(request).execute()

        self.assertEqual(response.status_code, 400)
        self.assertTrue('detail' in response.data.keys())


class CartItemServiceTestCase(TestCase):

    def test_empty_cart_received(self):
        cart = factory.create_cart()
        request = factory.create_rest_request()

        response = CartItemService(request).execute(cart_id=cart.pk)
        data = response.data['data']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['cart_items']), 0)

    def test_paginated_cart_items_received(self):
        cart = factory.create_cart()
        product_type = factory.create_product_type('test1')
        product = factory.create_product(type_id=product_type.pk)
        factory.create_cart_item(cart.pk, product.pk)
        request = factory.create_rest_request()

        response = CartItemService(request).execute(
            cart_id=cart.pk, paginate=True)
        data = response.data['data']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['cart_items']['results']), 1)
        self.assertTrue('image' in data['cart_items']['results'][0])
        self.assertTrue('product_title' in data['cart_items']['results'][0])

    def test_limited_cart_items_received(self):
        cart = factory.create_cart()
        product_type = factory.create_product_type('test1')
        product = factory.create_product(type_id=product_type.pk)
        product2 = factory.create_product(type_id=product_type.pk)
        product3 = factory.create_product(type_id=product_type.pk)
        product4 = factory.create_product(type_id=product_type.pk)
        product5 = factory.create_product(type_id=product_type.pk)
        factory.create_cart_item(cart.pk, product.pk)
        factory.create_cart_item(cart.pk, product2.pk)
        factory.create_cart_item(cart.pk, product3.pk)
        factory.create_cart_item(cart.pk, product4.pk)
        factory.create_cart_item(cart.pk, product5.pk)
        request = factory.create_rest_request()

        response = CartItemService(request).execute(
            cart_id=cart.pk, limit=RECENT_CART_ITEMS_LIMIT)
        data = response.data['data']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['cart_items']), RECENT_CART_ITEMS_LIMIT)


class ChangeQuantityServiceTestCase(TestCase):

    def test_cart_item_quantity_changed(self):
        # Arrange
        product_type = factory.create_product_type(name="type1")
        product = factory.create_product(product_type.pk)
        factory.create_activation_key(product.pk, key="1")
        factory.create_activation_key(product.pk, key="2")
        cart = factory.create_cart()
        cart_item = factory.create_cart_item(cart.pk, product.pk)

        post_data = {
            'value': cart_item.quantity + 1,
            'cart_item_id': cart_item.pk,
            'product_id': product.pk,
        }
        request = factory.create_post_request(data=post_data)

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
        product_type = factory.create_product_type(name="type1")
        product = factory.create_product(product_type.pk)
        cart = factory.create_cart()
        cart_item = factory.create_cart_item(cart.pk, product.pk)

        post_data = {
            'value': cart_item.quantity - 1,
            'cart_item_id': cart_item.pk,
            'product_id': product.pk,
        }
        request = factory.create_post_request(data=post_data)

        # Act
        response = ChangeQuantityService(request).execute()

        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertTrue('detail' in response.data.keys())
        self.assertEqual(CartItem.objects.get(id=cart_item.pk).quantity, 1)

    def test_new_quantity_more_than_max_possible(self):
        # Arrange
        product_type = factory.create_product_type(name="type1")
        product = factory.create_product(type_id=product_type.pk)
        factory.create_activation_key(product.pk, key="1")

        cart = factory.create_cart()
        cart_item = factory.create_cart_item(cart.pk, product.pk)

        post_data = {
            'value': cart_item.quantity + 1,
            'cart_item_id': cart_item.pk,
            'product_id': product.pk,
        }
        request = factory.create_post_request(data=post_data)

        # Act
        response = ChangeQuantityService(request).execute()

        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertTrue('detail' in response.data.keys())
        self.assertEqual(CartItem.objects.get(id=cart_item.pk).quantity, 1)
