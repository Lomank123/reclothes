from django.contrib import admin

from payment.models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'transaction_id', 'success', 'message')
    search_fields = ('id', 'message')
    list_filter = ('success', )
