from django.views.generic.base import TemplateView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from orders.services import DownloadFileService


class OrderView(TemplateView):
    template_name = 'orders/order.html'


class OrderSuccessView(TemplateView):
    template_name = 'orders/order_success.html'

    def get_context_data(self, **kwargs):
        # TODO: Check if order belongs to user
        context = super().get_context_data(**kwargs)
        order_id = self.request.GET.get('order_id', None)
        context.update({'order_id': order_id})
        return context


class MyOrdersView(TemplateView):
    template_name = 'orders/my_orders.html'


class DonwloadFileView(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        order_id = request.GET.get('order_id', None)
        return DownloadFileService(request).execute(order_id=order_id)
