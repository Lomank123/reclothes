from accounts.services import CartToSessionService
from carts.models import Cart
from django.test import Client, RequestFactory, TestCase
from reclothes.tests import factory


class CartToSessionServiceTestCase(TestCase):

    @staticmethod
    def _create_request(user):
        client = Client()
        client.get("/")
        request = RequestFactory().request()
        request.user = user
        request.session = client.session
        return request

    def test_login_with_existing_cart_successful(self):
        # Arrange
        user = factory.create_user("test1@gmail.com")
        cart = factory.create_cart(user.pk)
        request = self._create_request(user)

        # Act
        CartToSessionService(request).execute()

        # Assert
        self.assertEqual(Cart.objects.count(), 2)
        self.assertEqual(Cart.objects.filter(is_deleted=True).count(), 1)
        self.assertTrue(request.session["cart_id"] == cart.pk)

    def test_login_without_valid_user_cart_successful(self):
        # Arrange
        user = factory.create_user("test1@gmail.com")
        factory.create_cart(user.pk, is_deleted=True)
        factory.create_cart(user.pk, is_archived=True)
        request = self._create_request(user)

        # Act
        CartToSessionService(request).execute()

        # Assert
        self.assertEqual(Cart.objects.filter(user=user).count(), 3)
        user_cart = Cart.objects.filter(
            user=user, is_archived=False, is_deleted=False)
        self.assertTrue(user_cart.exists())
        self.assertTrue(request.session["cart_id"] == user_cart.first().pk)
