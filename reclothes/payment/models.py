from django.db import models
from django.utils.translation import gettext_lazy as _


class Transaction(models.Model):
    success = models.BooleanField(default=False, verbose_name=_('Success'))
    message = models.CharField(
        max_length=512, default='', verbose_name=_('Message'))
    transaction_id = models.CharField(
        max_length=512, unique=True, verbose_name=_('Transaction ID'))
    model = models.JSONField(null=True, blank=True, verbose_name=_('Model'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')

    def __str__(self):
        return f'Transaction ({self.pk})'
