from django.test import TestCase, RequestFactory, Client
from accounts.services import LoginViewService
from accounts.models import CustomUser
from carts.models import Cart


class LoginViewServiceTestCase(TestCase):

    @staticmethod
    def _create_user(username, password="123123123Aa"):
        return CustomUser.objects.create(username=username, password=password)

    @staticmethod
    def _create_cart(user_id, **kwargs):
        return Cart.objects.create(user_id=user_id, **kwargs)

    def test_login_with_existing_cart_successful(self):
        # Arrange
        user = self._create_user("test1")
        cart = self._create_cart(user.pk)
        self.assertEqual(Cart.objects.count(), 1)
        client = Client()
        client.get("/")
        request = RequestFactory().request()
        request.user = user
        request.session = client.session

        # Act
        LoginViewService(request).execute()

        # Assert
        self.assertEqual(Cart.objects.count(), 2)
        self.assertEqual(Cart.objects.filter(is_deleted=True).count(), 1)
        self.assertTrue(request.session["cart_id"] == cart.pk)

    def test_login_without_valid_user_cart_successful(self):
        # Arrange
        user = self._create_user("test1")
        self._create_cart(user.pk, is_deleted=True)
        self._create_cart(user.pk, is_archived=True)
        client = Client()
        client.get("/")
        request = RequestFactory().request()
        request.user = user
        request.session = client.session

        # Act
        LoginViewService(request).execute()

        # Assert
        self.assertEqual(Cart.objects.filter(user=user).count(), 3)
        user_cart = Cart.objects.filter(
            user=user, is_archived=False, is_deleted=False)
        self.assertTrue(user_cart.exists())
        self.assertTrue(request.session["cart_id"] == user_cart.first().pk)
