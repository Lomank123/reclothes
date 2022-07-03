from django.test import TestCase
from catalogue.services import HomeViewService, ProductDetailService
from catalogue.models import Product, Category, ProductReview, ProductType, ProductImage, \
    ProductAttribute, ProductAttributeValue
from carts.models import Cart, CartItem
from orders.models import Order, OrderItem, Address, Payment
from accounts.models import CustomUser
from orders.consts import CASH, IN_PROGRESS


class CatalogueServicesTestCase(TestCase):

    def setUp(self):
        # Users
        self.user = CustomUser.objects.create(username="test1", password="123123123Aa")
        self.user2 = CustomUser.objects.create(username="test2", password="123123123Aa")
        # Products
        self.product_type = ProductType.objects.create(name="type1")
        self.attr1 = ProductAttribute.objects.create(name="attr1", product_type=self.product_type)
        self.attr2 = ProductAttribute.objects.create(name="attr2", product_type=self.product_type)
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
        self.product3 = Product.objects.create(
            product_type=self.product_type,
            category=self.category,
            title="title3",
            quantity=7,
            regular_price=32.44,
            is_active=False
        )
        self.attr_value1 = ProductAttributeValue.objects.create(product=self.product1, attribute=self.attr1, value="1")
        self.attr_value2 = ProductAttributeValue.objects.create(product=self.product1, attribute=self.attr2, value="2")
        self.review1 = ProductReview.objects.create(product=self.product1, user=self.user, text="t1", rating=4)
        self.review2 = ProductReview.objects.create(product=self.product1, user=self.user2, text="t2", rating=1)
        self.review3 = ProductReview.objects.create(product=self.product2, user=self.user, text="t3", rating=5)
        self.review4 = ProductReview.objects.create(product=self.product2, user=self.user2, text="t4", rating=2)
        self.image1 = ProductImage.objects.create(product=self.product1, alt_text="testimg1", is_feature=True)
        self.image2 = ProductImage.objects.create(product=self.product1, alt_text="testimg2", is_feature=False)
        self.image3 = ProductImage.objects.create(product=self.product2, alt_text="testimg3", is_feature=False)
        # Carts
        self.cart1 = Cart.objects.create(user=self.user)
        self.cart_item1 = CartItem.objects.create(cart=self.cart1, product=self.product1)
        self.cart_item2 = CartItem.objects.create(cart=self.cart1, product=self.product2)
        self.cart2 = Cart.objects.create(user=self.user)
        self.cart_item3 = CartItem.objects.create(cart=self.cart2, product=self.product1)
        self.cart_item4 = CartItem.objects.create(cart=self.cart2, product=self.product2)
        # Orders
        self.address = Address.objects.create(name="Address1")
        self.payment1 = Payment.objects.create(payment_type=CASH, total_price=1234)
        self.order1 = Order.objects.create(
            user=self.user,
            address=self.address,
            payment=self.payment1,
            status=IN_PROGRESS
        )
        self.order_item1 = OrderItem.objects.create(order=self.order1, cart_item=self.cart_item1)
        self.order_item2 = OrderItem.objects.create(order=self.order1, cart_item=self.cart_item2)
        self.payment2 = Payment.objects.create(payment_type=CASH, total_price=1234)
        self.order2 = Order.objects.create(
            user=self.user,
            address=self.address,
            payment=self.payment2,
            status=IN_PROGRESS
        )
        self.order_item3 = OrderItem.objects.create(order=self.order2, cart_item=self.cart_item3)

    def tearDown(self):
        self.attr_value1.delete()
        self.attr_value2.delete()
        self.attr1.delete()
        self.attr2.delete()
        self.review1.delete()
        self.review2.delete()
        self.review3.delete()
        self.review4.delete()
        self.product1.delete()
        self.product2.delete()
        self.product3.delete()
        self.user.delete()
        self.product_type.delete()
        self.category.delete()
        self.image1.delete()
        self.image2.delete()
        self.image3.delete()
        self.cart_item1.delete()
        self.cart_item2.delete()
        self.cart_item3.delete()
        self.cart_item4.delete()
        self.cart1.delete()
        self.cart2.delete()
        self.order_item1.delete()
        self.order_item2.delete()
        self.order_item3.delete()
        self.order1.delete()
        self.order2.delete()
        self.payment1.delete()
        self.payment2.delete()
        self.address.delete()

    def test_homeview_service(self):
        response = HomeViewService().execute()
        self.assertEqual(response.status_code, 200)
        self.assertTrue("best_products" in response.data.keys())
        self.assertTrue("hot_products" in response.data.keys())
        self.assertTrue("newest_products" in response.data.keys())
        self.assertEqual(len(response.data["best_products"]), 2)
        self.assertEqual(len(response.data["hot_products"]), 2)
        self.assertEqual(len(response.data["newest_products"]), 2)
        # best_products
        self.assertEqual(response.data["best_products"][0]["avg_rate"], 3.5)
        self.assertEqual(response.data["best_products"][1]["avg_rate"], 2.5)
        # Image tests
        self.assertTrue("feature_image" in response.data["best_products"][0].keys())
        self.assertTrue(response.data["best_products"][0]["feature_image"] is None)
        self.assertTrue(response.data["best_products"][1]["feature_image"] is not None)
        # hot_products
        self.assertEqual(response.data["hot_products"][0]["purchases"], 2)
        self.assertEqual(response.data["hot_products"][1]["purchases"], 1)
        self.assertTrue("feature_image" in response.data["hot_products"][0].keys())
        # newest_products
        self.assertEqual(response.data["newest_products"][0]["title"], "title2")
        self.assertEqual(response.data["newest_products"][1]["title"], "title1")
        self.assertTrue("feature_image" in response.data["newest_products"][0].keys())

    def test_product_detail_service(self):
        response = ProductDetailService().execute(123123)
        self.assertEqual(response.status_code, 404)
        # 2nd case
        response = ProductDetailService().execute(self.product1.id)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("product" in response.data.keys())
        self.assertTrue("reviews" in response.data.keys())
        self.assertEqual(len(response.data["reviews"]), 2)
        self.assertTrue("attrs" in response.data.keys())
        self.assertEqual(len(response.data["attrs"]), 2)
        self.assertTrue("images" in response.data.keys())
        self.assertEqual(len(response.data["images"]), 2)
