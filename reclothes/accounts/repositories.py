from accounts.models import CustomUser


class CustomUserRepository:

    @staticmethod
    def fetch(first=False, limit=None, **kwargs):
        qs = CustomUser.objects.filter(**kwargs)
        if first:
            return qs.first()
        elif limit:
            return qs[:limit]
        return qs
