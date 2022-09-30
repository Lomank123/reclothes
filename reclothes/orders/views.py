from django.http.response import HttpResponseForbidden
from django.views.generic.base import TemplateView, View
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from orders.permissions import is_order_owner
from orders.services import DownloadFileService, OrderFileService


class OrderView(TemplateView):
    template_name = 'orders/order.html'


class MyOrdersView(TemplateView):
    template_name = 'orders/my_orders.html'


class OrderSuccessView(TemplateView):
    template_name = 'orders/order_success.html'

    def get(self, request):
        order_id = request.GET.get('order_id', None)
        is_owner = is_order_owner(request, order_id)
        if not is_owner:
            return HttpResponseForbidden()
        return super().get(request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.request.GET.get('order_id', None)
        context.update({'order_id': order_id})
        return context


class DownloadFileView(View):

    def get(self, request):
        return DownloadFileService(request).execute()


class OrderFileView(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        return OrderFileService(request).execute()
