import uuid

from accounts.models import CustomUser
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from orders.services import (DownloadFileService, OrderFileService,
                             OrderViewSetService)
from reclothes.tests import factory
from catalogue.models import OneTimeUrl
from django.utils import timezone
from datetime import timedelta


class CreateOrderServiceTestCase(TestCase):
    path = '/api/order/'
    content_type = 'application/json'

    def _create_data(self):
        # User
        user = factory.create_user(email='test1@gmail.com')
        # Product
        product_type = factory.create_product_type('type1')
        product = factory.create_product(type_id=product_type.pk)
        # Cart
        cart = factory.create_cart(user_id=user.pk)
        factory.create_cart_item(product_id=product.pk, cart_id=cart.pk)

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

    def test_non_admin_got_own_orders(self):
        user = factory.create_user(email='test1@gmail.com')
        user2 = factory.create_user(email='test2@gmail.com')
        order = factory.create_order(user=user)
        factory.create_order(user=user2)
        request = factory.create_request(user=user)

        qs = OrderViewSetService(request).execute()

        self.assertEqual(len(qs), 1)
        self.assertEqual(order, qs.first())


class OrderFileServiceTestCase(TestCase):

    def test_order_not_found(self):
        request = factory.create_request()

        response = OrderFileService(request, order_id=421).execute()

        self.assertEqual(response.status_code, 404)

    def test_user_is_not_order_owner(self):
        user = factory.create_user(email="test1@gmail.com")
        order = factory.create_order(user=user)
        request_data = {'order_id': order.pk}
        request = factory.create_get_request(data=request_data)
        request.user = None

        response = OrderFileService(request, order_id=order.pk).execute()

        self.assertEqual(response.status_code, 403)

    def test_order_files_retrieved(self):
        user = factory.create_user(email="test1@gmail.com")
        order = factory.create_order(user=user)
        request_data = {'order_id': order.pk}
        request = factory.create_get_request(data=request_data)
        request.user = user

        response = OrderFileService(request, order_id=order.pk).execute()

        self.assertEqual(response.status_code, 200)


# TODO: Implement this
class DownloadFileServiceTestCase(TestCase):

    def test_token_invalid(self):
        invalid_token = "123"

        response = DownloadFileService(url_token=invalid_token).execute()

        self.assertEqual(response.status_code, 400)

    def test_url_not_found(self):
        while True:
            test_uuid4 = uuid.uuid4().hex
            if not OneTimeUrl.objects.filter(url_token=test_uuid4).exists():
                break

        response = DownloadFileService(url_token=test_uuid4).execute()

        self.assertEqual(response.status_code, 404)

    def test_url_has_been_already_used(self):
        product_type = factory.create_product_type(name="type1")
        product = factory.create_product(type_id=product_type.pk)
        test_file = SimpleUploadedFile(
            "test.txt", b"test_content", content_type='text/plain')
        product_file = factory.create_product_file(
            product=product, file=test_file)
        expiry_date = timezone.now() + timedelta(days=1)
        url = factory.create_one_time_url(
            file=product_file, expired_at=expiry_date, is_used=True)

        response = DownloadFileService(url_token=url.url_token.hex).execute()

        self.assertEqual(response.status_code, 400)

    def test_file_retrieved(self):
        product_type = factory.create_product_type(name="type1")
        product = factory.create_product(type_id=product_type.pk)
        test_file = SimpleUploadedFile(
            "test.txt", b"test_content", content_type='text/plain')
        product_file = factory.create_product_file(
            product=product, file=test_file)
        expiry_date = timezone.now() + timedelta(days=1)
        url = factory.create_one_time_url(
            file=product_file, expired_at=expiry_date)

        response = DownloadFileService(url_token=url.url_token.hex).execute()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(OneTimeUrl.objects.count(), 0)
