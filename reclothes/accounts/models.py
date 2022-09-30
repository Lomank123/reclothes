from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.managers import CustomUserManager


class Company(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    address = models.CharField(max_length=255, verbose_name=_('Address'))
    contact_person = models.ForeignKey(
        to='accounts.CustomUser',
        on_delete=models.PROTECT,
        related_name='companies',
        verbose_name=_('Contact person'),
    )

    class Meta:
        ordering = ['-id']
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')

    def __str__(self):
        return f'{self.name} ({self.pk})'


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
    company = models.ForeignKey(
        to=Company,
        on_delete=models.PROTECT,
        null=True, blank=True,
        related_name='users',
        verbose_name=_('Company'),
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['-id']
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return f'{self.email} ({self.pk})'
