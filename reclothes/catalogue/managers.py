from django.db.models import Count, F, Q, Manager
from django.utils import timezone


class ActiveProductManager(Manager):

    def get_queryset(self):
        """
        Return active products which either have 0 (no limit) or enough keys.
        """
        no_order = Q(activation_keys__order__isnull=True)
        not_expired = Q(activation_keys__expired_at__gte=timezone.now())
        active_keys_count = Count(
            'activation_keys', filter=no_order & not_expired)
        active_products = Q(is_active=True) & (
            Q(keys_limit=0) | Q(keys_diff__gte=0))

        return (
            super().get_queryset()
            .annotate(keys_diff=active_keys_count - F('keys_limit'))
            .filter(active_products)
            .order_by('-id')
        )


class ActiveCategoryManager(Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class ActiveKeyManager(Manager):

    def get_queryset(self):
        return super().get_queryset().active()
