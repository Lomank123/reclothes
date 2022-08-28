from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    city = models.ForeignKey(
        to='orders.City',
        blank=True, null=True,
        on_delete=models.SET_NULL,
        related_name='users',
        verbose_name=_('City'),
    )

    def __str__(self):
        return f'{self.username} ({self.pk})'
