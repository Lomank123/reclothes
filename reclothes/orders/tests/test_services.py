from accounts.models import CustomUser
from carts.tests.test_services import (create_cart, create_cart_item,
                                       create_product, create_product_type,
                                       create_request, create_user)
from django.test import TestCase
from orders.models import Address, City, Order, StatusTypes
from orders.services import OrderViewSetService
from payment.models import PaymentTypes


def create_city(name):
    return City.objects.create(name=name)


def create_address(name, city):
    return Address.objects.create(name=name, city=city)


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
        # City
        city = create_city('city1')
        create_address('addr1', city=city)

    # End-to-end test
    def test_no_data_provided(self):
        self._create_data()
        self.client.force_login(CustomUser.objects.first())

        response = self.client.post(
            self.path, data=dict(), content_type=self.content_type)

        self.assertEqual(response.status_code, 400)
        self.assertTrue('payment_type' in response.data['detail'].keys())
        self.assertTrue('address_id' in response.data['detail'].keys())

    # End-to-end test
    def test_no_card_credentials_provided(self):
        self._create_data()
        data = {
            'address_id': Address.objects.first().pk,
            'payment_type': PaymentTypes.CARD.value,
        }
        self.client.force_login(CustomUser.objects.first())

        response = self.client.post(
            self.path, data=data, content_type=self.content_type)

        self.assertEqual(response.status_code, 400)
        self.assertTrue('card' in response.data['detail'].keys())

    # End-to-end test
    def test_wrong_card_credentials_provided(self):
        self._create_data()
        data = {
            'address_id': Address.objects.first().pk,
            'payment_type': PaymentTypes.CARD.value,
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
    def test_order_with_cash_payment_created_successfully(self):
        self._create_data()
        data = {
            'address_id': Address.objects.first().pk,
            'payment_type': PaymentTypes.CASH.value,
        }
        self.client.force_login(CustomUser.objects.first())

        response = self.client.post(
            self.path, data=data, content_type=self.content_type)

        self.assertEqual(response.status_code, 200)

    # End-to-end test
    def test_order_with_card_payment_created_successfully(self):
        self._create_data()
        data = {
            'address_id': Address.objects.first().pk,
            'payment_type': PaymentTypes.CARD.value,
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
    def _create_order(user, address):
        return Order.objects.create(
            user=user,
            address=address,
            status=StatusTypes.IN_PROGRESS.value,
            total_price=123,
        )

    def test_non_admin_got_own_orders(self):
        user = create_user(email='test1@gmail.com')
        user2 = create_user(email='test2@gmail.com')
        city = create_city('city1')
        address = create_address('addr1', city=city)
        order = self._create_order(user=user, address=address)
        self._create_order(user=user2, address=address)
        request = create_request(user=user)

        qs = OrderViewSetService(request).execute()

        self.assertEqual(len(qs), 1)
        self.assertEqual(order, qs.first())

    def test_admin_got_all_orders(self):
        admin = create_user(email='admin1@gmail.com')
        admin.is_superuser = True
        admin.save()
        user2 = create_user(email='test2@gmail.com')
        city = create_city('city1')
        address = create_address('addr1', city=city)
        self._create_order(user=admin, address=address)
        self._create_order(user=user2, address=address)
        request = create_request(user=admin)

        qs = OrderViewSetService(request).execute()

        self.assertEqual(len(qs), 2)
