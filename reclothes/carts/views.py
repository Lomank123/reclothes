from django.views.generic.base import TemplateView


class CartView(TemplateView):
    template_name = 'carts/cart.html'
