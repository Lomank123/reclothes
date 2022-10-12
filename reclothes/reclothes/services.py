from rest_framework import status
from rest_framework.response import Response


class AbstractAPIService:

    def _build_response_data(self):
        '''Construct response data and return it as dict.'''

    def _build_response(self):
        '''Construct Response and return it.'''

    def execute(self):
        '''Entrypoint of every service.'''


class APIService(AbstractAPIService):
    '''Base implementation of service. Use it when create new services.'''

    def __init__(self):
        self.errors = dict()

    def _build_response_data(self, **kwargs) -> dict:
        if self.errors:
            return {'detail': self.errors}
        return {'data': kwargs}

    def _build_response(self, data=dict(), status_code=status.HTTP_200_OK):
        response = Response(data=data, status=status_code)
        if self.errors:
            response.status_code = status.HTTP_400_BAD_REQUEST
        return response

    def execute(self, **kwargs) -> Response:
        data = self._build_response_data(**kwargs)
        return self._build_response(data)
