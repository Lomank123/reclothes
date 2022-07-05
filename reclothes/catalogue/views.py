from django.views.generic.base import TemplateView


class HomeView(TemplateView):
    template_name = 'catalogue/home.html'


class ProductDetailView(TemplateView):
    template_name = 'catalogue/product-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product_id"] = kwargs.get("pk")
        return context


class CatalogueView(TemplateView):
    template_name = 'catalogue/catalogue.html'
