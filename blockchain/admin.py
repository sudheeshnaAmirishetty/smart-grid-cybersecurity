from django.contrib import admin
from .models import TransactionRecord

@admin.register(TransactionRecord)
class TransactionRecordAdmin(admin.ModelAdmin):
    list_display = ('tx_id', 'sender', 'receiver', 'amount', 'timestamp')
    search_fields = ('tx_id', 'sender', 'receiver')
