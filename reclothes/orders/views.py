from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView, View

from orders.services import DownloadFileService


class OrderView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/order.html'


class MyOrdersView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/my_orders.html'


class OrderDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/order_detail.html'

    def get(self, request, pk):
        return super().get(request, order_id=pk)


class DownloadFileView(View):

    def get(self, request, url_token):
        return DownloadFileService(url_token).execute()
