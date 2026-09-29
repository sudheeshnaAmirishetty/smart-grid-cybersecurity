from django.contrib import admin
from .models import Device

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'status', 'last_heartbeat')
    search_fields = ('name', 'type', 'status')
