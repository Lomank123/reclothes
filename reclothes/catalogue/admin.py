from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from catalogue import models
from catalogue.forms import ProductModelForm


class ProductAttributeInline(admin.TabularInline):
    model = models.ProductAttribute


class ProductImageInline(admin.TabularInline):
    readonly_fields = ['creation_date', 'last_update']
    model = models.ProductImage


class ProductAttributeValueInline(admin.TabularInline):
    model = models.ProductAttributeValue


@admin.register(models.ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [
        ProductAttributeInline,
    ]


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductModelForm
    readonly_fields = ['creation_date', 'last_update']
    inlines = [
        ProductAttributeValueInline,
        ProductImageInline,
    ]


@admin.register(models.Category)
class CategoryAdmin(MPTTModelAdmin):
    prepopulated_fields = {'slug': ('name',), }


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    readonly_fields = ['creation_date', 'last_update']


@admin.register(models.ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    readonly_fields = ['creation_date', 'last_update']
