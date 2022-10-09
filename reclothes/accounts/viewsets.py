from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from accounts.serializers import (CustomUserDetailSerializer,
                                  CustomUserSerializer)
from accounts.services import CustomUserViewSetService


class CustomUserViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, )

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CustomUserDetailSerializer
        return CustomUserSerializer

    def get_queryset(self):
        return CustomUserViewSetService(self.request).execute()
