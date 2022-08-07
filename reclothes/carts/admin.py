from django.contrib import admin

from carts import models


@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'is_deleted', 'is_archived', 'updated_at', 'created_at', )


@admin.register(models.CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity', )
