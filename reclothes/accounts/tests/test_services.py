from django.test import TestCase, RequestFactory, Client
from accounts.services import LoginViewService
from accounts.models import CustomUser
from carts.models import Cart


class LoginViewServiceTestCase(TestCase):

    def setUp(self):
        self.user1 = CustomUser.objects.create(username="test1", password="123123123Aa")
        self.user2 = CustomUser.objects.create(username="test2", password="123123123Aa")
        self.cart1 = Cart.objects.create(user=self.user1)
        self.cart2 = Cart.objects.create(user=self.user2, is_deleted=True)
        self.cart3 = Cart.objects.create(user=self.user2, is_archived=True)

    def tearDown(self):
        self.user1.delete()
        self.user2.delete()
        self.cart1.delete()
        self.cart2.delete()
        self.cart3.delete()

    def test_execute_form_login(self):
        self.assertEqual(Cart.objects.count(), 3)
        # 1st case with existing user cart
        client1 = Client()
        client1.get("/")
        request = RequestFactory().request()
        request.user = self.user1
        request.session = client1.session
        LoginViewService(request).execute_form_login()
        self.assertTrue(request.session["cart_id"] == self.cart1.id)
        self.assertEqual(Cart.objects.count(), 4)
        # 2nd case without valid user cart
        client2 = Client()
        client2.get("/")
        request.user = self.user2
        request.session = client2.session
        LoginViewService(request).execute_form_login()
        self.assertFalse(request.session["cart_id"] == self.cart1.id)
        self.assertEqual(Cart.objects.count(), 5)
        self.assertTrue(Cart.objects.filter(user=self.user2, is_archived=False, is_deleted=False).exists())
        self.assertEqual(Cart.objects.filter(user=self.user2).count(), 3)
