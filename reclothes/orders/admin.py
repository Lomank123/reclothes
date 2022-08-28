from django.contrib import admin

from orders.models import Address, City, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    list_display = ('__str__', 'id', 'cart_item')
    model = OrderItem


class AddressInline(admin.TabularInline):
    list_display = ('name', 'id', 'city', 'is_available')
    model = Address


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'is_available')
    list_filter = ('is_available', )
    search_fields = ('id', 'name')
    inlines = (AddressInline, )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'city', 'is_available')
    list_filter = ('is_available', )
    search_fields = ('id', )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'id',
        'status',
        'user',
        'address',
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
