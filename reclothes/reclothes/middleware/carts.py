from carts.services import CartMiddlewareService


class CartMiddleware(object):
    """
    Set cart id to session if it not exists.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Before the view (and later middleware) are called
        CartMiddlewareService(request).execute()
        response = self.get_response(request)
        return response
