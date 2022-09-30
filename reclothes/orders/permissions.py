from orders.repositories import OrderRepository


def is_order_owner(request, order_id=None):
    if order_id is None:
        return False
    order = OrderRepository.fetch(first=True, id=order_id)
    return order.user == request.user
