from catalogue.models import CustomBaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class Cart(CustomBaseModel):
    user = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name=_("User"),
        related_name="carts",
    )
    is_deleted = models.BooleanField(default=False, verbose_name=_("Deleted"))
    is_archived = models.BooleanField(
        default=False, verbose_name=_("Archived"))

    def __str__(self):
        return f"Cart {self.pk}"

    class Meta:
        verbose_name_plural = _("Carts")
        verbose_name = _("Cart")
        ordering = ["-created_at"]


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        verbose_name=_("Cart"),
        related_name="cart_items",
    )
    product = models.ForeignKey(
        "catalogue.Product",
        on_delete=models.CASCADE,
        verbose_name=_("Product"),
        related_name="cart_items",
    )
    quantity = models.IntegerField(default=1, verbose_name=_("Quantity"))

    class Meta:
        verbose_name_plural = _("Cart items")
        verbose_name = _("Cart item")
        # Cart can have only unique cart items
        constraints = [
            models.UniqueConstraint(
                fields=['product_id', 'cart_id'],
                name='unique_cartitem_constraint',
            ),
        ]
