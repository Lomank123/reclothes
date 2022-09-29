from django.views.generic.base import TemplateView, View
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.http.response import FileResponse, HttpResponseForbidden
from catalogue.models import ProductFile
from orders.models import Order

from orders.services import OrderFileService


class OrderView(TemplateView):
    template_name = 'orders/order.html'


class MyOrdersView(TemplateView):
    template_name = 'orders/my_orders.html'


class OrderSuccessView(TemplateView):
    template_name = 'orders/order_success.html'

    def _is_user_owner(self, request):
        order_id = request.GET.get('order_id', None)
        if order_id is None:
            return False
        order = Order.objects.filter(id=order_id).first()
        return order.user == request.user

    def get(self, request):
        if not self._is_user_owner(request):
            return HttpResponseForbidden()
        return super().get(request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.request.GET.get('order_id', None)
        context.update({'order_id': order_id})
        return context


class DowloadFileView(View):

    def _is_user_owner(self, request):
        order_id = request.GET.get('order_id', None)
        if order_id is None:
            return False
        order = Order.objects.filter(id=order_id).first()
        return order.user == request.user

    def get(self, request):
        if not self._is_user_owner(request):
            return HttpResponseForbidden()

        file_id = request.GET.get('file_id', None)
        product_file = ProductFile.objects.filter(id=file_id).first()
        return FileResponse(product_file.file, as_attachment=True)


class OrderFileView(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        order_id = request.GET.get('order_id', None)
        return OrderFileService(request).execute(order_id=order_id)
