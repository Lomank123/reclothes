from django.views.generic.base import TemplateView


class OrderView(TemplateView):
    template_name = 'orders/order.html'


class OrderSuccessView(TemplateView):
    template_name = 'orders/order_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.request.GET.get('order_id', None)
        context.update({'order_id': order_id})
        return context


class MyOrdersView(TemplateView):
    template_name = 'orders/my_orders.html'
