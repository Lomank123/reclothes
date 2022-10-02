from datetime import timedelta

from catalogue.repositories import ProductRepository
from django.test import TestCase
from django.utils import timezone
from reclothes.tests import factory


class ProductRepositoryTestCase(TestCase):

    def setUp(self):
        self.product_type = factory.create_product_type(name="type1")

    def test_product_with_enough_keys_fetched(self):
        product = factory.create_product(self.product_type.pk)
        factory.create_activation_key(product.pk, key="1")

        result = ProductRepository.fetch_active()

        self.assertEqual(result.count(), 1)

    def test_unlimited_product_fetched(self):
        factory.create_product(self.product_type.pk, keys_limit=0)

        result = ProductRepository.fetch_active()

        self.assertEqual(result.count(), 1)

    def test_product_with_expired_key_not_fetched(self):
        product = factory.create_product(self.product_type.pk)
        expired_date = timezone.now() - timedelta(days=1)
        expired_key = factory.create_activation_key(product.pk, key="4")
        expired_key.expired_at = expired_date
        expired_key.save()

        result = ProductRepository.fetch_active()

        self.assertEqual(result.count(), 0)

    def test_inactive_product_not_fetched(self):
        factory.create_product(self.product_type.pk, is_active=False)

        result = ProductRepository.fetch_active()

        self.assertEqual(result.count(), 0)

    def test_product_with_not_enough_keys_not_fetched(self):
        factory.create_product(self.product_type.pk, keys_limit=2)

        result = ProductRepository.fetch_active()

        self.assertEqual(result.count(), 0)

    def test_product_with_used_key_not_fetched(self):
        user = factory.create_user("test1@gmail.com")
        order = factory.create_order(user=user)
        product = factory.create_product(self.product_type.pk)
        factory.create_activation_key(product.pk, key="2", order=order)

        result = ProductRepository.fetch_active()

        self.assertEqual(result.count(), 0)
