from carts.exceptions import BadRequest
from carts.models import Cart
from carts.utils import CartSessionManager
from catalogue.models import ActivationKey
from django.db import transaction
from django.shortcuts import get_object_or_404

from orders.consts import NOT_ENOUGH_KEYS_MSG
from orders.models import Order, OrderItem


class CreateOrderService:

    __slots__ = 'request', 'session_manager'

    def __init__(self, request):
        self.request = request
        self.session_manager = CartSessionManager(request)

    def _create_order_items(self, cart, order):
        cart_items = cart.cart_items.select_related('product')
        for item in cart_items:
            limit = item.keys_count
            keys = item.product.active_keys.values_list(
                'pk', flat=True)[:limit]

            if len(keys) < limit:
                raise BadRequest(detail=NOT_ENOUGH_KEYS_MSG)

            # Mount keys to order
            ActivationKey.objects.filter(pk__in=keys).update(order=order)
            # Create OrderItem
            OrderItem.objects.create(order=order, cart_item=item)

    @transaction.atomic
    def execute(self):
        cart_id = self.session_manager.load_cart_id_from_session()
        cart = get_object_or_404(Cart, id=cart_id)

        # Order with keys and items
        order = Order.objects.create(
            user=cart.user, total_price=cart.total_price)
        self._create_order_items(cart, order)

        cart.archive()
        new_cart = Cart.objects.create(user=self.request.user)
        self.session_manager.set_cart_id_if_not_exists(
            cart_id=new_cart.pk, forced=True)

        return order
