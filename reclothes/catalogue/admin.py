from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from catalogue.forms import ProductModelForm
from catalogue.models import (Category, Product, ProductAttribute,
                              ProductAttributeValue, ProductImage,
                              ProductReview, ProductType, Tag, ProductFile, ActivationKey)


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute


class ProductImageInline(admin.TabularInline):
    readonly_fields = ('created_at', 'updated_at')
    model = ProductImage


class ProductFileInline(admin.TabularInline):
    readonly_fields = ('created_at', 'updated_at')
    model = ProductFile


class ActivationKeyInline(admin.TabularInline):
    model = ActivationKey


class ProductAttributeValueInline(admin.TabularInline):
    model = ProductAttributeValue


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'is_active')
    list_filter = ('is_active', )
    search_fields = ('id', 'name')
    inlines = (ProductAttributeInline, )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductModelForm
    list_display = (
        'title',
        'id',
        'regular_price',
        'product_type',
        'category',
        'quantity',
        'company',
        'is_active',
        'is_limited',
    )
    list_filter = ('is_active', )
    search_fields = ('id', 'title')
    inlines = (
        ProductAttributeValueInline,
        ProductImageInline,
        ProductFileInline,
        ActivationKeyInline,
    )

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            self.readonly_fields = ('created_at', 'updated_at')
        else:
            self.readonly_fields = ('company', 'created_at', 'updated_at')
        return super().get_readonly_fields(request, obj)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.company is None:
            return qs.none()
        return qs.filter(company=request.user.company)

    def save_model(self, request, obj, form, change):
        obj.company = request.user.company
        super().save_model(request, obj, form, change)


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ('name', 'parent', 'slug', 'is_active')
    list_filter = ('is_active', )
    search_fields = ('id', 'name')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('id', )


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id', 'user', 'product', 'rating')
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('id', 'text')
