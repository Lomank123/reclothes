from orders.serializers import CitySerializer
from rest_framework import serializers

from accounts.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    city = CitySerializer(required=False)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'city')
