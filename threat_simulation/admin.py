from django.contrib import admin
from .models import SimulationScenario

@admin.register(SimulationScenario)
class SimulationScenarioAdmin(admin.ModelAdmin):
    list_display = ('name', 'attack_type', 'is_active', 'score', 'started_at')
    list_filter = ('attack_type', 'is_active')
    search_fields = ('name',)
