from django.contrib import admin
from .models import AnomalyRecord

@admin.register(AnomalyRecord)
class AnomalyRecordAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'score', 'is_anomaly', 'created_at')
    list_filter = ('is_anomaly',)
    search_fields = ('device_id',)
