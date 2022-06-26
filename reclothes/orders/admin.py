from django.contrib import admin

from orders import models


# TODO: Maybe payment shouldn't be here
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "user", "address", "payment", "last_update", "creation_date", )


@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "cart_item", )


@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("name", "id", "is_available", )
    list_filter = ("is_available", )


@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "payment_type", "total_price", )
    list_filter = ("payment_type", )
