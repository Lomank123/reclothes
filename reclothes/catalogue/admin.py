from django.contrib import admin
from catalogue import models


class ProductAttributeInline(admin.TabularInline):
    model = models.ProductAttribute


class ProductImageInline(admin.TabularInline):
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
    prepopulated_fields = {'slug': ('title',), }
    inlines = [
        ProductAttributeValueInline,
        ProductImageInline,
    ]


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }


admin.site.register(models.ProductReview)
admin.site.register(models.Tag)
