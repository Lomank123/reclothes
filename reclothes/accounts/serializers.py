from rest_framework import serializers

from accounts.models import Company, CustomUser


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('id', 'email')


class CustomUserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        exclude = (
            'password',
            'username',
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )
