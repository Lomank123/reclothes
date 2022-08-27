from django.views.generic.base import TemplateView


class OrderView(TemplateView):
    template_name = 'orders/order.html'
