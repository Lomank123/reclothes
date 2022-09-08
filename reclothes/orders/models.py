from catalogue.models import CustomBaseModel
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class StatusTypes(models.TextChoices):
    DECLINED = 'Declined'
    ACCEPTED = 'Accepted'
    DONE = 'Done'
    IN_PROGRESS = 'In progress'
    REFUNDED = 'Refunded'


class City(models.Model):
    name = models.CharField(
        max_length=255, verbose_name=_('Name'), unique=True)
    is_available = models.BooleanField(
        default=True, verbose_name=_('Available'))

    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _('Cities')

    def __str__(self):
        return f'{self.name} ({self.pk})'


class Address(models.Model):
    city = models.ForeignKey(
        to=City,
        on_delete=models.PROTECT,
        related_name='addresses',
        verbose_name=_('City'),
    )
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
    total_price = models.DecimalField(
        validators=[MinValueValidator(0.01)],
        verbose_name=_("Total price"),
        help_text=_("Maximum 9999999999.99"),
        max_digits=12,
        decimal_places=2,
        default=0,
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
