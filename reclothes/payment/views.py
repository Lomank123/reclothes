from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from payment.serializers import CardSerializer


class CardAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        """Validate card credentials."""
        serializer = CardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = {'detail': 'Card credentials are valid.'}
        return Response(data=data, status=status.HTTP_200_OK)
