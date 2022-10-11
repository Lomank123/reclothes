from rest_framework import permissions

from carts.models import Cart


class IsCartInSession(permissions.BasePermission):
    """
    Return True if cart id is in current session.

    Can be used only with Cart and CartItem objects.
    """

    def has_object_permission(self, request, view, obj):
        cart_id = request.session.get('cart_id', None)
        # If it is Cart object
        if isinstance(obj, Cart):
            return obj.pk == cart_id
        # CartItem object
        return obj.cart.pk == cart_id
