from payment.models import Payment


class PaymentRepository:

    @staticmethod
    def fetch(first=False, limit=None, **kwargs):
        qs = Payment.objects.filter(**kwargs)
        if first:
            return qs.first()
        elif limit:
            return qs[:limit]
        return qs

    @staticmethod
    def create(**kwargs):
        return Payment.objects.create(**kwargs)
