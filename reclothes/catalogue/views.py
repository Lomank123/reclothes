from django.views.generic.base import TemplateView


class HomeView(TemplateView):
    template_name = 'catalogue/home.html'


class ProductDetailView(TemplateView):
    template_name = 'catalogue/product-detail.html'

    def get(self, request, pk, **kwargs):
        return super().get(request, product_id=pk, **kwargs)


class CatalogueView(TemplateView):
    template_name = 'catalogue/catalogue.html'


class CategoriesView(TemplateView):
    template_name = 'catalogue/categories.html'
