from django.contrib import admin
from .models import IoTMessage, IoTDatasetUpload

@admin.register(IoTMessage)
class IoTMessageAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'protocol', 'received_at')
    list_filter = ('protocol',)
    search_fields = ('device_id',)


@admin.register(IoTDatasetUpload)
class IoTDatasetUploadAdmin(admin.ModelAdmin):
    list_display = ('name', 'uploaded_at', 'total_records', 'anomalies_detected')
    readonly_fields = ('summary',)
    search_fields = ('name',)
