from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.managers import CustomUserManager


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=32,
        blank=True, null=True,
        verbose_name=_('Username'),
        validators=[UnicodeUsernameValidator()],
    )
    email = models.EmailField(
        unique=True,
        help_text=_('Required and unique.'),
        verbose_name=_("Email address"),
    )
    city = models.ForeignKey(
        to='orders.City',
        blank=True, null=True,
        on_delete=models.SET_NULL,
        related_name='users',
        verbose_name=_('City'),
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email} ({self.pk})'
