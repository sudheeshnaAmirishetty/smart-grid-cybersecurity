from django.contrib import admin
from .models import FlowRule

@admin.register(FlowRule)
class FlowRuleAdmin(admin.ModelAdmin):
    list_display = ('src', 'dst', 'protocol', 'action', 'updated_at')
    list_filter = ('protocol', 'action')
    search_fields = ('src', 'dst')
