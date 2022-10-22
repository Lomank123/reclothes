from rest_framework import serializers


class CardSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    expiry_date = serializers.DateField(
        format='%m/%y', input_formats=['%m/%y'], required=True)
    number = serializers.CharField(max_length=16, min_length=16, required=True)
    code = serializers.CharField(max_length=3, min_length=3, required=True)
