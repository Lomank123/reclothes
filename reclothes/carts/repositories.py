from reclothes.repositories import BaseRepository

from carts.models import Cart


class CartRepository(BaseRepository):

    def __init__(self):
        super().__init__(Cart)

    def fetch_active(self, first=False, limit=None, **kwargs):
        """Return non-deleted and non-archived cart qs."""
        return super().fetch(
            first=first, limit=limit,
            is_archived=False,
            is_deleted=False,
            **kwargs,
        )

    @staticmethod
    def delete(cart, full_delete=False):
        """
        Mark cart as deleted.

        If full_delete is True then completely delete cart.
        """
        if full_delete:
            cart.delete()
        else:
            cart.is_deleted = True
            cart.save()
