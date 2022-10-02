from accounts.models import CustomUser
from carts.tests.test_services import (create_activation_key, create_product,
                                       create_product_type)
from django.test import TestCase
from orders.models import Order, StatusTypes
from django.utils import timezone
from datetime import timedelta
from catalogue.repositories import ProductRepository


def create_order(user_id, status=StatusTypes.IN_PROGRESS):
    return Order.objects.create(user_id=user_id, status=status)


def create_user(email, password="123123123Aa"):
    return CustomUser.objects.create(email=email, password=password)


class ProductRepositoryTestCase(TestCase):

    def setUp(self):
        self.product_type = create_product_type(name="type1")

    def test_product_with_enough_keys_fetched(self):
        product = create_product(self.product_type.pk)
        create_activation_key(product.pk, key="1")

        result = ProductRepository.fetch_active()

        self.assertEqual(result.count(), 1)

    def test_unlimited_product_fetched(self):
        create_product(self.product_type.pk, keys_limit=0)

        result = ProductRepository.fetch_active()

        self.assertEqual(result.count(), 1)

    def test_product_with_expired_key_not_fetched(self):
        product = create_product(self.product_type.pk)
        expired_date = timezone.now() - timedelta(days=1)
        expired_key = create_activation_key(product.pk, key="4")
        expired_key.expired_at = expired_date
        expired_key.save()

        result = ProductRepository.fetch_active()

        self.assertEqual(result.count(), 0)

    def test_inactive_product_not_fetched(self):
        create_product(self.product_type.pk, is_active=False)

        result = ProductRepository.fetch_active()

        self.assertEqual(result.count(), 0)

    def test_product_with_not_enough_keys_not_fetched(self):
        create_product(self.product_type.pk, keys_limit=2)

        result = ProductRepository.fetch_active()

        self.assertEqual(result.count(), 0)

    def test_product_with_used_key_not_fetched(self):
        user = create_user("test1@gmail.com")
        order = create_order(user_id=user.pk)
        product = create_product(self.product_type.pk)
        create_activation_key(product.pk, key="2", order=order)

        result = ProductRepository.fetch_active()

        self.assertEqual(result.count(), 0)
