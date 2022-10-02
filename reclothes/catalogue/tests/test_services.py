from catalogue.models import Category
from catalogue.services import (CatalogueService, CategoryService,
                                HomeViewService, ProductDetailService)
from catalogue.viewsets import ProductViewSet
from django.test import TestCase
from reclothes.tests import factory


class HomePageTestCase(TestCase):

    def _create_data(self):
        # Users
        user = factory.create_user(email='test1@gmail.com')
        user2 = factory.create_user(email='test2@gmail.com')
        # Products
        product_type = factory.create_product_type('type1')
        attr1 = factory.create_product_attr('attr1', type_id=product_type.pk)
        attr2 = factory.create_product_attr('attr2', type_id=product_type.pk)
        product1 = factory.create_product(type_id=product_type.pk)
        product2 = factory.create_product(type_id=product_type.pk)
        factory.create_activation_key(product_id=product1.pk, key="1")
        factory.create_activation_key(product_id=product2.pk, key="2")
        factory.create_product_attr_value(
            product_id=product1.pk, attr_id=attr1.pk)
        factory.create_product_attr_value(
            product_id=product1.pk, attr_id=attr2.pk)
        # Reviews
        factory.create_product_review(
            product_id=product1.pk, user_id=user.pk, rating=4)
        factory.create_product_review(
            product_id=product1.pk, user_id=user2.pk, rating=1)
        factory.create_product_review(
            product_id=product2.pk, user_id=user.pk, rating=5)
        factory.create_product_review(
            product_id=product2.pk, user_id=user2.pk, rating=2)
        # Images
        factory.create_image(product_id=product1.pk, is_feature=True)
        factory.create_image(product_id=product1.pk)
        factory.create_image(product_id=product2.pk)
        # Carts
        cart1 = factory.create_cart(user_id=user.pk)
        cart2 = factory.create_cart(user_id=user.pk)
        # Cart items
        cart_item1 = factory.create_cart_item(
            product_id=product1.pk, cart_id=cart1.pk)
        cart_item2 = factory.create_cart_item(
            product_id=product2.pk, cart_id=cart1.pk)
        cart_item3 = factory.create_cart_item(
            product_id=product1.pk, cart_id=cart2.pk)
        factory.create_cart_item(product_id=product2.pk, cart_id=cart2.pk)
        # Orders
        order1 = factory.create_order(user=user)
        order2 = factory.create_order(user=user)
        # Order items
        factory.create_order_item(
            order_id=order1.pk, cart_item_id=cart_item1.pk)
        factory.create_order_item(
            order_id=order1.pk, cart_item_id=cart_item2.pk)
        factory.create_order_item(
            order_id=order2.pk, cart_item_id=cart_item3.pk)

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
        product_type = factory.create_product_type('type1')
        product = factory.create_product(product_type.pk)

        response = ProductDetailService().execute(product.pk)
        data = response.data['data']

        self.assertEqual(response.status_code, 200)
        self.assertTrue('reviews_with_users' in data.keys())
        self.assertTrue('attrs_with_values' in data.keys())
        self.assertTrue('ordered_images' in data.keys())


class CategoryServiceTestCase(TestCase):

    def test_root_categories_received(self):
        root_category = factory.create_category(name='root1', slug='root1')
        factory.create_category(name='root2', slug='root2')
        factory.create_category(parent=root_category, name='s1', slug='s1')

        response = CategoryService().execute()
        data = response.data['data']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Category.objects.count(), 3)
        self.assertEqual(len(data['items']), 2)

    def test_sub_categories_received(self):
        root_category = factory.create_category(name='root1', slug='root1')
        factory.create_category(name='root2', slug='root2')
        sub_category = factory.create_category(
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
    def _create_viewset(request):
        viewset = ProductViewSet(request=request)
        viewset.format_kwarg = None
        return viewset

    def test_products_with_tags_received(self):
        # Test data
        product_type = factory.create_product_type(name='type1')
        product1 = factory.create_product(type_id=product_type.pk, title='test1')
        product2 = factory.create_product(type_id=product_type.pk, title='test2')
        factory.create_activation_key(product_id=product1.pk, key="1")
        factory.create_activation_key(product_id=product2.pk, key="2")
        tag1 = factory.create_tag(name='tag1')
        tag2 = factory.create_tag(name='tag2')
        tag3 = factory.create_tag(name='tag3')
        product1.tags.add(tag1)
        product1.tags.add(tag2)
        product2.tags.add(tag3)
        # Viewset
        request = factory.create_rest_request()
        viewset = self._create_viewset(request)

        response = CatalogueService(viewset).execute(paginate=True)
        data = response.data['data']

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data.get('products', False))
        self.assertTrue(data.get('popular_tags', False))
        self.assertTrue(data['products'].get('results', False))
        self.assertEqual(len(data['products']['results']), 2)
        self.assertEqual(len(data['popular_tags']), 3)
