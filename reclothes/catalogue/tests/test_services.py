from accounts.models import CustomUser
from carts.models import Cart, CartItem
from catalogue.models import (Category, Product, ProductAttribute,
                              ProductAttributeValue, ProductImage,
                              ProductReview, ProductType, Tag)
from catalogue.services import (CatalogueService, CategoryService,
                                HomeViewService, ProductDetailService)
from catalogue.viewsets import ProductViewSet
from django.test import RequestFactory, TestCase
from orders.models import (Address, Order, OrderItem, Payment, PaymentTypes,
                           StatusTypes)
from rest_framework.request import Request


def create_product_type(name):
    return ProductType.objects.create(name=name)


def create_product(type_id, title='test', quantity=10, regular_price=100.00):
    return Product.objects.create(
        product_type_id=type_id,
        title=title,
        quantity=quantity,
        regular_price=regular_price
    )


class CatalogueServicesTestCase(TestCase):

    @staticmethod
    def _create_user(username, password='123123123Aa'):
        return CustomUser.objects.create(username=username, password=password)

    @staticmethod
    def _create_product_attr(name, type_id):
        return ProductAttribute.objects.create(
            name=name, product_type_id=type_id)

    @staticmethod
    def _create_product_attr_value(product_id, attr_id, value='12'):
        return ProductAttributeValue.objects.create(
            product_id=product_id, attribute_id=attr_id, value=value)

    @staticmethod
    def _create_product_review(product_id, user_id, rating=5, text='test'):
        return ProductReview.objects.create(
            product_id=product_id, user_id=user_id, rating=rating, text=text)

    @staticmethod
    def _create_image(product_id, alt_text='img', is_feature=False):
        return ProductImage.objects.create(
            product_id=product_id, alt_text=alt_text, is_feature=is_feature)

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
    def _create_payment(order_id, type=PaymentTypes.CASH, total_price=123):
        return Payment.objects.create(
            order_id=order_id, type=type, total_price=total_price)

    @staticmethod
    def _create_order(
        user_id,
        address_id,
        status=StatusTypes.IN_PROGRESS,
    ):
        return Order.objects.create(
            user_id=user_id,
            address_id=address_id,
            status=status
        )

    @staticmethod
    def _create_order_item(order_id, cart_item_id):
        return OrderItem.objects.create(
            order_id=order_id, cart_item_id=cart_item_id)

    def _create_data(self):
        # Users
        user = self._create_user('test1')
        user2 = self._create_user('test2')
        # Products
        product_type = create_product_type('type1')
        attr1 = self._create_product_attr('attr1', type_id=product_type.pk)
        attr2 = self._create_product_attr('attr2', type_id=product_type.pk)
        product1 = create_product(type_id=product_type.pk)
        product2 = create_product(type_id=product_type.pk)
        self._create_product_attr_value(
            product_id=product1.pk, attr_id=attr1.pk)
        self._create_product_attr_value(
            product_id=product1.pk, attr_id=attr2.pk)
        # Reviews
        self._create_product_review(
            product_id=product1.pk, user_id=user.pk, rating=4)
        self._create_product_review(
            product_id=product1.pk, user_id=user2.pk, rating=1)
        self._create_product_review(
            product_id=product2.pk, user_id=user.pk, rating=5)
        self._create_product_review(
            product_id=product2.pk, user_id=user2.pk, rating=2)
        # Images
        self._create_image(product_id=product1.pk, is_feature=True)
        self._create_image(product_id=product1.pk)
        self._create_image(product_id=product2.pk)
        # Carts
        cart1 = self._create_cart(user_id=user.pk)
        cart2 = self._create_cart(user_id=user.pk)
        # Cart items
        cart_item1 = self._create_cart_item(
            product_id=product1.pk, cart_id=cart1.pk)
        cart_item2 = self._create_cart_item(
            product_id=product2.pk, cart_id=cart1.pk)
        cart_item3 = self._create_cart_item(
            product_id=product1.pk, cart_id=cart2.pk)
        self._create_cart_item(product_id=product2.pk, cart_id=cart2.pk)
        # Orders
        address = self._create_address('addr1')
        order1 = self._create_order(user_id=user.pk, address_id=address.pk)
        order2 = self._create_order(user_id=user.pk, address_id=address.pk)
        self._create_payment(order1.pk)
        self._create_payment(order2.pk)
        # Order items
        self._create_order_item(order_id=order1.pk, cart_item_id=cart_item1.pk)
        self._create_order_item(order_id=order1.pk, cart_item_id=cart_item2.pk)
        self._create_order_item(order_id=order2.pk, cart_item_id=cart_item3.pk)

    def test_home_page_products_data_received(self):
        self._create_data()

        response = HomeViewService().execute()
        data = response.data['data']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['best_products']), 2)
        self.assertEqual(len(data['hot_products']), 2)
        self.assertEqual(len(data['newest_products']), 2)
        # best_products
        self.assertEqual(data['best_products'][0]['avg_rate'], 3.5)
        self.assertEqual(data['best_products'][1]['avg_rate'], 2.5)
        # hot_products
        self.assertEqual(data['hot_products'][0]['purchases'], 2)
        self.assertEqual(data['hot_products'][1]['purchases'], 1)
        # Image tests
        self.assertTrue('feature_image' in data['best_products'][0].keys())
        self.assertTrue('feature_image' in data['newest_products'][0].keys())
        self.assertTrue('feature_image' in data['hot_products'][0].keys())


class ProductDetailServiceTestCase(TestCase):

    def test_product_not_found(self):
        product_id = 123123

        response = ProductDetailService().execute(product_id)

        self.assertEqual(response.status_code, 400)
        self.assertTrue('detail' in response.data.keys())

    def test_product_detail_received(self):
        product_type = create_product_type('type1')
        product = create_product(product_type.pk)

        response = ProductDetailService().execute(product.pk)
        data = response.data['data']

        self.assertEqual(response.status_code, 200)
        self.assertTrue('reviews_with_users' in data.keys())
        self.assertTrue('attrs_with_values' in data.keys())
        self.assertTrue('ordered_images' in data.keys())


class CategoryServiceTestCase(TestCase):

    @staticmethod
    def _create_category(**kwargs):
        return Category.objects.create(**kwargs)

    def test_root_categories_received(self):
        root_category = self._create_category(name='root1', slug='root1')
        self._create_category(name='root2', slug='root2')
        self._create_category(parent=root_category, name='s1', slug='s1')

        response = CategoryService().execute()
        data = response.data['data']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Category.objects.count(), 3)
        self.assertEqual(len(data['items']), 2)

    def test_sub_categories_received(self):
        root_category = self._create_category(name='root1', slug='root1')
        self._create_category(name='root2', slug='root2')
        sub_category = self._create_category(
            parent=root_category, name='s1', slug='s1')

        response = CategoryService().execute(root_category.pk)
        data = response.data['data']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Category.objects.count(), 3)
        self.assertEqual(len(data['items']), 1)
        self.assertEqual(
            data['items'][0]['category_tree'][0]['id'], sub_category.pk)


class CatalogueServiceTestCase(TestCase):

    @staticmethod
    def _create_request():
        return Request(request=RequestFactory().request())

    @staticmethod
    def _create_viewset(request):
        viewset = ProductViewSet(request=request)
        viewset.format_kwarg = None
        return viewset

    @staticmethod
    def _create_tag(**kwargs):
        return Tag.objects.create(**kwargs)

    def test_products_with_tags_received(self):
        # Test data
        product_type = create_product_type(name='type1')
        product1 = create_product(type_id=product_type.pk, title='test1')
        product2 = create_product(type_id=product_type.pk, title='test2')
        tag1 = self._create_tag(name='tag1')
        tag2 = self._create_tag(name='tag2')
        tag3 = self._create_tag(name='tag3')
        product1.tags.add(tag1)
        product1.tags.add(tag2)
        product2.tags.add(tag3)
        # Viewset
        request = self._create_request()
        viewset = self._create_viewset(request)

        response = CatalogueService(viewset).execute(paginate=True)
        data = response.data['data']

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data.get('products', False))
        self.assertTrue(data.get('popular_tags', False))
        self.assertTrue(data['products'].get('results', False))
        self.assertEqual(len(data['products']['results']), 2)
        self.assertEqual(len(data['popular_tags']), 3)
