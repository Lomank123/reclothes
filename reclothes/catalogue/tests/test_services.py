from django.test import TestCase
from catalogue.services import HomeViewService
from catalogue.models import Product, Category, ProductReview, ProductType
from carts.models import Cart, CartItem
from orders.models import Order, OrderItem, Address, Payment
from accounts.models import CustomUser
from orders.consts import CASH, IN_PROGRESS


class HomeViewServiceTestCase(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(username="test1", password="123123123Aa")
        self.user2 = CustomUser.objects.create(username="test2", password="123123123Aa")
        self.product_type = ProductType.objects.create(name="type1")
        self.category = Category.objects.create(name="category1")
        self.product1 = Product.objects.create(
            product_type=self.product_type,
            category=self.category,
            title="title1",
            quantity=10,
            regular_price=100.00
        )
        self.product2 = Product.objects.create(
            product_type=self.product_type,
            category=self.category,
            title="title2",
            quantity=7,
            regular_price=32.44
        )
        self.review1 = ProductReview.objects.create(product=self.product1, user=self.user, text="testreview1", rating=4)
        self.review2 = ProductReview.objects.create(product=self.product1, user=self.user2, text="testreview2", rating=1)
        self.review3 = ProductReview.objects.create(product=self.product2, user=self.user, text="testreview3", rating=5)
        self.review4 = ProductReview.objects.create(product=self.product2, user=self.user2, text="testreview4", rating=2)

    def tearDown(self):
        self.review1.delete()
        self.review2.delete()
        self.review3.delete()
        self.review4.delete()
        self.product1.delete()
        self.product2.delete()
        self.user.delete()
        self.product_type.delete()
        self.category.delete()

    def test_get_home_products(self):
        # Prerequisites
        cart1 = Cart.objects.create(user=self.user)
        cart_item1 = CartItem.objects.create(cart=cart1, product=self.product1)
        cart_item2 = CartItem.objects.create(cart=cart1, product=self.product2)
        cart2 = Cart.objects.create(user=self.user)
        cart_item3 = CartItem.objects.create(cart=cart2, product=self.product1)
        CartItem.objects.create(cart=cart2, product=self.product2)
        address = Address.objects.create(name="Address1")
        payment1 = Payment.objects.create(payment_type=CASH, total_price=1234)
        order1 = Order.objects.create(user=self.user, address=address, payment=payment1, status=IN_PROGRESS)
        OrderItem.objects.create(order=order1, cart_item=cart_item1)
        OrderItem.objects.create(order=order1, cart_item=cart_item2)
        payment2 = Payment.objects.create(payment_type=CASH, total_price=1234)
        order2 = Order.objects.create(user=self.user, address=address, payment=payment2, status=IN_PROGRESS)
        OrderItem.objects.create(order=order2, cart_item=cart_item3)
        # Test
        response = HomeViewService().execute()
        self.assertEqual(response.status_code, 200)
        self.assertTrue("best_products" in response.data.keys())
        self.assertTrue("hot_products" in response.data.keys())
        self.assertTrue("newest_products" in response.data.keys())
        # best_products
        self.assertEqual(response.data["best_products"][0]["avg_rate"], 3.5)
        self.assertEqual(response.data["best_products"][1]["avg_rate"], 2.5)
        # hot_products
        self.assertEqual(response.data["hot_products"][0]["count"], 2)
        self.assertEqual(response.data["hot_products"][1]["count"], 1)
        # newest_products
        self.assertEqual(response.data["newest_products"][0]["title"], "title2")
        self.assertEqual(response.data["newest_products"][1]["title"], "title1")
