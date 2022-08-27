from catalogue.models import CustomBaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class PaymentTypes(models.TextChoices):
    CASH = _('Cash')
    CARD = _('Card')


class StatusTypes(models.TextChoices):
    DECLINED = _('Declined')
    ACCEPTED = _('Accepted')
    DONE = _('Done')
    IN_PROGRESS = _('In progress')
    REFUNDED = _('Refunded')


class Address(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Address'))
    is_available = models.BooleanField(
        default=True, verbose_name=_('Available'))

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')

    def __str__(self):
        return self.name


class Order(CustomBaseModel):
    user = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.CASCADE,
        verbose_name=_('User'),
        blank=True, null=True,
        related_name='orders',
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.DO_NOTHING,
        verbose_name=_('Address'),
        related_name='orders',
    )
    status = models.CharField(
        max_length=255,
        choices=StatusTypes.choices,
        default=StatusTypes.IN_PROGRESS,
        verbose_name=_('Order status'),
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return f'Order ({self.pk})'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name=_('Order'),
        related_name='order_items',
    )
    cart_item = models.OneToOneField(
        'carts.CartItem',
        on_delete=models.CASCADE,
        verbose_name=_('Cart Item'),
    )

    class Meta:
        verbose_name = _('Order item')
        verbose_name_plural = _('Order items')

    def __str__(self):
        return f'Order item ({self.pk})'


# TODO: Move to payment app
class Payment(models.Model):
    type = models.CharField(
        max_length=10,
        choices=PaymentTypes.choices,
        default=PaymentTypes.CASH,
        verbose_name=_('Payment Type'),
    )
    total_price = models.DecimalField(
        max_digits=7, decimal_places=2, verbose_name=_('Total price'))
    order = models.OneToOneField(
        Order, on_delete=models.RESTRICT, verbose_name=_('Order'))

    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')

    def __str__(self):
        return f'Payment ({self.pk}) to order ({self.order.pk})'
