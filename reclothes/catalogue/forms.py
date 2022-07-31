from django import forms

from catalogue.models import Category, Product


class ProductModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProductModelForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(
            children__isnull=True
        )

    class Meta:
        model = Product
        fields = '__all__'
