from django.db import models
from django.utils.translation import gettext_lazy as _


class PaymentTypes(models.TextChoices):
    CASH = 'Cash'
    CARD = 'Card'


class Payment(models.Model):
    type = models.CharField(
        max_length=10,
        choices=PaymentTypes.choices,
        default=PaymentTypes.CASH,
        verbose_name=_('Payment Type'),
    )
    total_price = models.DecimalField(
        max_digits=7, decimal_places=2,
        verbose_name=_('Total price'),
        help_text=_('Maximum 99999.99'),
    )
    order = models.OneToOneField(
        'orders.Order', on_delete=models.RESTRICT, verbose_name=_('Order'))

    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')

    def __str__(self):
        return f'Payment ({self.pk}) to order ({self.order.pk})'
