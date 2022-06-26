from catalogue.models import CustomBaseModel
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from orders import consts


user_model = get_user_model()


class Address(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    is_available = models.BooleanField(default=True, verbose_name=_("Is available"))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-id"]
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")


# TODO: This should be created automatically with order
# Use signals for example
class Payment(models.Model):
    PAYMENT_CHOICES = [
        (consts.CASH, _("Cash")),
        (consts.CARD, _("Card")),
    ]
    payment_type = models.CharField(
        max_length=10,
        choices=PAYMENT_CHOICES,
        default=consts.CASH,
        verbose_name=_("Type")
    )
    total_price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name=_("Total price"))

    def __str__(self):
        return f"{self.payment_type} ({self.id})"

    class Meta:
        ordering = ["-id"]
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")


class Order(CustomBaseModel):
    STATUS_CHOICES = [
        (consts.IN_PROGRESS, _("In progress")),
        (consts.ACCEPTED, _("Accepted")),
        (consts.DECLINED, _("Declined")),
        (consts.DONE, _("Done")),
        (consts.REFUNDED, _("Refunded")),
    ]
    user = models.ForeignKey(user_model, on_delete=models.CASCADE, verbose_name=_("User"))
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING, verbose_name=_("Address"))
    payment = models.OneToOneField(Payment, on_delete=models.DO_NOTHING, verbose_name=_("Payment"))
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=consts.IN_PROGRESS,
        verbose_name=_("Status")
    )

    class Meta:
        ordering = ["-creation_date"]
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name=_("Order"))
    cart_item = models.OneToOneField("carts.CartItem", on_delete=models.CASCADE, verbose_name=_("Cart Item"))

    class Meta:
        ordering = ["-id"]
        verbose_name = _("Order item")
        verbose_name_plural = _("Order items")


# TODO: Implement transactions
class Transaction(models.Model):
    pass
