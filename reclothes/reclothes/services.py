from rest_framework import status
from rest_framework.response import Response


class AbstractAPIService:

    def _get_response_data(self):
        pass

    def _get_response(self):
        pass


class APIService(AbstractAPIService):

    @staticmethod
    def _get_response(data: dict) -> Response:
        response = Response(data=data, status=status.HTTP_200_OK)
        if len(data) == 0:
            response.status_code = status.HTTP_404_NOT_FOUND
        return response
