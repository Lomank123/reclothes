from django.contrib import admin

from carts.models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    list_display = ('__str__', 'id', 'product', 'quantity')
    model = CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'id',
        'user',
        'is_deleted',
        'is_archived',
        'updated_at',
        'created_at',
    )
    list_filter = ('is_deleted', 'is_archived')
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('id', )
    inlines = (CartItemInline, )


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id', 'cart', 'product', 'quantity')
    search_fields = ('id', )
