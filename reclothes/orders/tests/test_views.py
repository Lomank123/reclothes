from django.test import TestCase
from reclothes.tests import factory

from orders.views import OrderDetailView


class OrderDetailViewTestCase(TestCase):

    def test_user_is_not_owner(self):
        user = factory.create_user(email="test1@gmail.com")
        user2 = factory.create_user(email="test2@gmail.com")
        order = factory.create_order(user=user2)
        request_data = {'order_id': order.pk}
        request = factory.create_get_request(data=request_data)
        request.user = user

        response = OrderDetailView(request=request).get(request, pk=order.pk)

        self.assertEqual(response.status_code, 403)

    def test_user_is_owner(self):
        user = factory.create_user(email="test1@gmail.com")
        order = factory.create_order(user=user)
        request_data = {'order_id': order.pk}
        request = factory.create_get_request(data=request_data)
        request.user = user

        response = OrderDetailView(request=request).get(request, pk=order.pk)

        self.assertEqual(response.status_code, 200)
