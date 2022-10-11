from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView, View

from orders.models import Order
from orders.services import DownloadFileService


class OrderView(TemplateView):
    template_name = 'orders/order.html'


class MyOrdersView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/my_orders.html'


class OrderDetailView(TemplateView):
    template_name = 'orders/order_detail.html'

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        is_owner = order.user == request.user
        if not is_owner:
            return HttpResponseForbidden()
        return super().get(request, order_id=pk)


class DownloadFileView(View):

    def get(self, request, url_token):
        return DownloadFileService(url_token).execute()
