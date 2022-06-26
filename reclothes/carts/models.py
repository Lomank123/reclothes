from catalogue.models import CustomBaseModel
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


user_model = get_user_model()


class Cart(CustomBaseModel):
    user = models.ForeignKey(
        user_model,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("User"),
        related_name="carts"
    )
    is_deleted = models.BooleanField(default=False, verbose_name=_("Deleted"))
    is_archived = models.BooleanField(default=False, verbose_name=_("Archived"))

    def __str__(self):
        return f"{self.user.username}'s cart {self.id}"

    class Meta:
        verbose_name_plural = _("Carts")
        verbose_name = _("Cart")
        ordering = ["-creation_date"]


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        verbose_name=_("Cart"),
        related_name="cart_items"
    )
    product = models.ForeignKey(
        "catalogue.Product",
        on_delete=models.CASCADE,
        verbose_name=_("Product"),
        related_name="cart_items"
    )
    quantity = models.IntegerField(default=1, verbose_name=_("Quantity"))

    class Meta:
        verbose_name_plural = _("Cart items")
        verbose_name = _("Cart item")
        ordering = ["-id"]
