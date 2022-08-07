from accounts.models import CustomUser


class CustomUserRepository:

    @staticmethod
    def fetch_all_users():
        return CustomUser.objects.all()
