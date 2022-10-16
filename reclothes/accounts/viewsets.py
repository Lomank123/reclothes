from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from accounts.models import CustomUser
from accounts.serializers import (CustomUserDetailSerializer,
                                  CustomUserSerializer)


class CustomUserViewSet(ModelViewSet):

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
        # Limit to only current user
        return CustomUser.objects.filter(id=self.request.user.pk)
