from accounts.models import CustomUser
from carts.tests.test_services import (create_cart, create_cart_item,
                                       create_product, create_product_type,
                                       create_request, create_user)
from django.test import TestCase
from orders.models import Order, StatusTypes
from orders.services import OrderViewSetService


class CreateOrderServiceTestCase(TestCase):
    path = '/api/order/'
    content_type = 'application/json'

    def _create_data(self):
        # User
        user = create_user(email='test1@gmail.com')
        # Product
        product_type = create_product_type('type1')
        product = create_product(type_id=product_type.pk)
        # Cart
        cart = create_cart(user_id=user.pk)
        create_cart_item(product_id=product.pk, cart_id=cart.pk)

    # End-to-end test
    def test_no_data_provided(self):
        self._create_data()
        self.client.force_login(CustomUser.objects.first())

        response = self.client.post(
            self.path, data=dict(), content_type=self.content_type)

        self.assertEqual(response.status_code, 400)

    # End-to-end test
    def test_no_card_credentials_provided(self):
        self._create_data()
        self.client.force_login(CustomUser.objects.first())

        response = self.client.post(
            self.path, data=dict(), content_type=self.content_type)

        self.assertEqual(response.status_code, 400)
        self.assertTrue('card' in response.data['detail'].keys())

    # End-to-end test
    def test_wrong_card_credentials_provided(self):
        self._create_data()
        data = {
            'card': {
                'name': 'qwe',
                'number': '123213',
                'code': '12',
                'expiry_date': '15-22',
            },
        }
        self.client.force_login(CustomUser.objects.first())

        response = self.client.post(
            self.path, data=data, content_type=self.content_type)

        self.assertEqual(response.status_code, 400)
        card_errors = response.data['detail']['card']
        self.assertTrue('number' in card_errors.keys())
        self.assertTrue('expiry_date' in card_errors.keys())
        self.assertTrue('code' in card_errors.keys())

    # End-to-end test
    def test_order_created_successfully(self):
        self._create_data()
        data = {
            'card': {
                'name': 'Card Holder',
                'number': '1231231231231231',
                'code': '123',
                'expiry_date': '4/22',
            },
        }
        self.client.force_login(CustomUser.objects.first())

        response = self.client.post(
            self.path, data=data, content_type=self.content_type)

        self.assertEqual(response.status_code, 200)


class OrderViewSetServiceTestCase(TestCase):

    @staticmethod
    def _create_order(user):
        return Order.objects.create(
            user=user,
            status=StatusTypes.IN_PROGRESS.value,
            total_price=123,
        )

    def test_non_admin_got_own_orders(self):
        user = create_user(email='test1@gmail.com')
        user2 = create_user(email='test2@gmail.com')
        order = self._create_order(user=user)
        self._create_order(user=user2)
        request = create_request(user=user)

        qs = OrderViewSetService(request).execute()

        self.assertEqual(len(qs), 1)
        self.assertEqual(order, qs.first())

    def test_admin_got_all_orders(self):
        admin = create_user(email='admin1@gmail.com')
        admin.is_superuser = True
        admin.save()
        user2 = create_user(email='test2@gmail.com')
        self._create_order(user=admin)
        self._create_order(user=user2)
        request = create_request(user=admin)

        qs = OrderViewSetService(request).execute()

        self.assertEqual(len(qs), 2)
