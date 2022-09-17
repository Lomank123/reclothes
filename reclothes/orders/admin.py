from django.contrib import admin

from orders.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    list_display = ('__str__', 'id', 'cart_item')
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'id',
        'status',
        'user',
        'updated_at',
        'created_at',
    )
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('id', )
    inlines = (OrderItemInline, )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id', 'order', 'cart_item')
    search_fields = ('id', )
