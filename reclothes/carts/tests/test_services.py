from accounts.models import CustomUser
from carts.models import Cart, CartItem
from carts.services import CartService
from catalogue.models import Product, ProductType
from django.test import Client, RequestFactory, TestCase


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


class CartServiceTestCase(TestCase):

    def setUp(self):
        self.user1 = CustomUser.objects.create(username="test1", password="123123123Aa")
        self.user2 = CustomUser.objects.create(username="test2", password="123123123Aa")
        self.cart1 = Cart.objects.create(user=self.user1)
        self.product_type = ProductType.objects.create(name="type1")
        self.product1 = Product.objects.create(
            product_type=self.product_type,
            title="title1",
            quantity=10,
            regular_price=100.00
        )

    def tearDown(self):
        self.user1.delete()
        self.user2.delete()
        self.cart1.delete()
        self.product1.delete()
        self.product_type.delete()

    def test_execute_ok(self):
        client = Client()
        client.get("/")
        request = RequestFactory().request()
        request.session = client.session
        # empty cart
        response = CartService(request).execute()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["cart"]["cart_items_count"], 0)
        self.assertEqual(len(response.data["cart_items"]), 0)
        # filled cart
        cart = Cart.objects.get(id=request.session.get("cart_id"))
        CartItem.objects.create(cart_id=cart.id, product=self.product1)
        response = CartService(request).execute()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["cart"]["cart_items_count"], 1)
        self.assertEqual(len(response.data["cart_items"]), 1)
        self.assertTrue("image" in response.data["cart_items"][0])
        self.assertTrue("product_title" in response.data["cart_items"][0])

    def test_execute_not_found(self):
        client = Client()
        client.get("/")
        request = RequestFactory().request()
        request.session = client.session
        Cart.objects.get(id=request.session.get("cart_id")).delete()
        response = CartService(request).execute()
        self.assertEqual(response.status_code, 404)
