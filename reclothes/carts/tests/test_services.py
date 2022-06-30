from django.test import TestCase, RequestFactory, Client
from accounts.models import CustomUser
from carts.models import Cart


class CartMiddlewareServiceTestCase(TestCase):

    def setUp(self):
        self.user1 = CustomUser.objects.create(username="test1", password="123123123Aa")
        self.user2 = CustomUser.objects.create(username="test2", password="123123123Aa")
        self.cart1 = Cart.objects.create(user=self.user1)

    def tearDown(self):
        self.user1.delete()
        self.user2.delete()
        self.cart1.delete()

    def test_execute(self):
        self.assertEqual(Cart.objects.count(), 1)
        # 1st case without authenticated user
        client1 = Client()
        client1.get("/")
        request = RequestFactory().request()
        # request.user = self.user1
        request.session = client1.session
        self.assertTrue(request.session["cart_id"])
        self.assertEqual(Cart.objects.count(), 2)
        Cart.objects.filter(user=None).first().delete()
        client1.get("/")
        self.assertEqual(Cart.objects.count(), 2)
        # 2nd case with user
        client2 = Client()
        client2.force_login(self.user2)
        client2.get("/")
        self.assertEqual(Cart.objects.count(), 3)
        self.assertEqual(Cart.objects.filter(user=self.user2).count(), 1)
