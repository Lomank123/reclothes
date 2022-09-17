from django.contrib import admin

from orders.models import City, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    list_display = ('__str__', 'id', 'cart_item')
    model = OrderItem


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'is_available')
    list_filter = ('is_available', )
    search_fields = ('id', 'name')


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
