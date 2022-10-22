from catalogue.models import CustomBaseModel
from django.db import models
from django.db.models import F, Sum
from django.utils.translation import gettext_lazy as _

from carts.managers import ActiveCartManager
from carts.querysets import CartItemQuerySet


class Cart(CustomBaseModel):
    user = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name=_('User'),
        related_name='carts',
    )
    is_deleted = models.BooleanField(default=False, verbose_name=_('Deleted'))
    is_archived = models.BooleanField(
        default=False, verbose_name=_('Archived'))

    objects = models.Manager()
    active = ActiveCartManager()

    class Meta:
        ordering = ['-id']
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')

    def __str__(self):
        return f'Cart {self.pk}'

    @property
    def items_count(self):
        return self.cart_items.count()

    @property
    def total_price(self):
        result = self.cart_items.aggregate(
            total=Sum(F('product__regular_price') * F('quantity')))
        return result['total']

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def archive(self):
        self.is_archived = True
        self.save()


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        verbose_name=_('Cart'),
        related_name='cart_items',
    )
    product = models.ForeignKey(
        'catalogue.Product',
        on_delete=models.CASCADE,
        verbose_name=_('Product'),
        related_name='cart_items',
    )
    quantity = models.IntegerField(default=1, verbose_name=_('Quantity'))

    objects = CartItemQuerySet.as_manager()

    class Meta:
        ordering = ['-id']
        verbose_name = _('Cart item')
        verbose_name_plural = _('Cart items')
        constraints = [
            models.UniqueConstraint(
                fields=['product_id', 'cart_id'],
                name='unique_cartitem_constraint',
            ),
        ]

    def __str__(self):
        return f'Item ({self.pk}) to Cart ({self.cart.pk})'

    @property
    def total_price(self):
        return self.product.regular_price * self.quantity

    @property
    def keys_count(self):
        """Required keys count."""
        return self.product.keys_limit * self.quantity
