from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from accounts.models import CustomUser
from accounts.serializers import CustomUserSerializer


class CustomUserViewSet(ModelViewSet):
    serializer_class = CustomUserSerializer
    permission_classes = (AllowAny, )

    def get_queryset(self):
        qs = CustomUser.objects.all()
        return qs
