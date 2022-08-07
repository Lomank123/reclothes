from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from accounts.serializers import CustomUserSerializer
from accounts.services import CustomUserViewSetService


class CustomUserViewSet(ModelViewSet):
    serializer_class = CustomUserSerializer
    permission_classes = (AllowAny, )

    def get_queryset(self):
        return CustomUserViewSetService.execute()
