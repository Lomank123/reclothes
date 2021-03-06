from accounts.models import CustomUser
from carts.models import Cart, CartItem
from catalogue.models import (Product, ProductAttribute, ProductAttributeValue,
                              ProductImage, ProductReview, ProductType)
from catalogue.services import HomeViewService, ProductDetailService
from django.test import TestCase
from orders.consts import CASH, IN_PROGRESS
from orders.models import Address, Order, OrderItem, Payment


def create_product_type(name):
    return ProductType.objects.create(name=name)


def create_product(type_id, title="test", quantity=10, regular_price=100.00):
    return Product.objects.create(
        product_type_id=type_id,
        title=title,
        quantity=quantity,
        regular_price=regular_price
    )


class CatalogueServicesTestCase(TestCase):

    @staticmethod
    def _create_user(username, password="123123123Aa"):
        return CustomUser.objects.create(username=username, password=password)

    @staticmethod
    def _create_product_attr(name, type_id):
        return ProductAttribute.objects.create(name=name, product_type_id=type_id)

    @staticmethod
    def _create_product_attr_value(product_id, attr_id, value="12"):
        return ProductAttributeValue.objects.create(product_id=product_id, attribute_id=attr_id, value=value)

    @staticmethod
    def _create_product_review(product_id, user_id, rating=5, text="test"):
        return ProductReview.objects.create(product_id=product_id, user_id=user_id, rating=rating, text=text)

    @staticmethod
    def _create_image(product_id, alt_text="img", is_feature=False):
        return ProductImage.objects.create(product_id=product_id, alt_text=alt_text, is_feature=is_feature)

    @staticmethod
    def _create_cart(user_id=None):
        return Cart.objects.create(user_id=user_id)

    @staticmethod
    def _create_cart_item(product_id, cart_id):
        return CartItem.objects.create(product_id=product_id, cart_id=cart_id)

    @staticmethod
    def _create_address(name):
        return Address.objects.create(name=name)

    @staticmethod
    def _create_payment(type=CASH, total_price=123):
        return Payment.objects.create(payment_type=type, total_price=total_price)

    @staticmethod
    def _create_order(user_id, address_id, payment_id, status=IN_PROGRESS):
        return Order.objects.create(user_id=user_id, address_id=address_id, payment_id=payment_id, status=status)

    @staticmethod
    def _create_order_item(order_id, cart_item_id):
        return OrderItem.objects.create(order_id=order_id, cart_item_id=cart_item_id)

    def _create_data(self):
        # Users
        user = self._create_user("test1")
        user2 = self._create_user("test2")
        # Products
        product_type = create_product_type("type1")
        attr1 = self._create_product_attr("attr1", type_id=product_type.id)
        attr2 = self._create_product_attr("attr2", type_id=product_type.id)
        product1 = create_product(type_id=product_type.id)
        product2 = create_product(type_id=product_type.id)
        self._create_product_attr_value(product_id=product1.id, attr_id=attr1.id)
        self._create_product_attr_value(product_id=product1.id, attr_id=attr2.id)
        # Reviews
        self._create_product_review(product_id=product1.id, user_id=user.id, rating=4)
        self._create_product_review(product_id=product1.id, user_id=user2.id, rating=1)
        self._create_product_review(product_id=product2.id, user_id=user.id, rating=5)
        self._create_product_review(product_id=product2.id, user_id=user2.id, rating=2)
        # Images
        self._create_image(product_id=product1.id, is_feature=True)
        self._create_image(product_id=product1.id)
        self._create_image(product_id=product2.id)
        # Carts
        cart1 = self._create_cart(user_id=user.id)
        cart2 = self._create_cart(user_id=user.id)
        # Cart items
        cart_item1 = self._create_cart_item(product_id=product1.id, cart_id=cart1.id)
        cart_item2 = self._create_cart_item(product_id=product2.id, cart_id=cart1.id)
        cart_item3 = self._create_cart_item(product_id=product1.id, cart_id=cart2.id)
        self._create_cart_item(product_id=product2.id, cart_id=cart2.id)
        # Orders
        address = self._create_address("addr1")
        payment1 = self._create_payment()
        payment2 = self._create_payment()
        order1 = self._create_order(user_id=user.id, address_id=address.id, payment_id=payment1.id)
        order2 = self._create_order(user_id=user.id, address_id=address.id, payment_id=payment2.id)
        # Order items
        self._create_order_item(order_id=order1.id, cart_item_id=cart_item1.id)
        self._create_order_item(order_id=order1.id, cart_item_id=cart_item2.id)
        self._create_order_item(order_id=order2.id, cart_item_id=cart_item3.id)

    def test_get_products_data(self):
        self._create_data()

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
        # hot_products
        self.assertEqual(response.data["hot_products"][0]["purchases"], 2)
        self.assertEqual(response.data["hot_products"][1]["purchases"], 1)
        # Image tests
        self.assertTrue("feature_image" in response.data["best_products"][0].keys())
        self.assertTrue("feature_image" in response.data["newest_products"][0].keys())
        self.assertTrue("feature_image" in response.data["hot_products"][0].keys())


class ProductDetailServiceTestCase(TestCase):

    def test_product_not_found(self):
        product_id = 123123

        response = ProductDetailService().execute(product_id)

        self.assertEqual(response.status_code, 404)

    def test_product_detail_service(self):
        product_type = create_product_type("type1")
        product = create_product(product_type.id)

        response = ProductDetailService().execute(product.id)

        self.assertEqual(response.status_code, 200)
        self.assertTrue("product" in response.data.keys())
        self.assertTrue("reviews" in response.data.keys())
        self.assertTrue("attrs" in response.data.keys())
        self.assertTrue("images" in response.data.keys())
