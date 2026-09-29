from django.contrib import admin
from .models import ThreatRecord

@admin.register(ThreatRecord)
class ThreatRecordAdmin(admin.ModelAdmin):
    list_display = ('name', 'confidentiality', 'integrity', 'availability', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name',)
