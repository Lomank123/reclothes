from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from accounts.serializers import (CustomUserDetailSerializer,
                                  CustomUserSerializer)
from accounts.services import CustomUserViewSetService


class CustomUserViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, )

    def get_permissions(self):
        if self.action == 'destroy':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CustomUserDetailSerializer
        return CustomUserSerializer

    def get_queryset(self):
        # By default it returns only current user
        return CustomUserViewSetService(self.request).execute()
