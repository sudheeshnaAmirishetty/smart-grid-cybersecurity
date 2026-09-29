from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('infrastructure/', include('infrastructure.urls')),
    path('iot/', include('iot_integration.urls')),
    path('cybersecurity/', include('cybersecurity.urls')),
    path('ai/', include('ai_module.urls')),
    path('blockchain/', include('blockchain.urls')),
    path('sdn/', include('sdn.urls')),
    path('threat/', include('threat_simulation.urls')),
    path('', include('monitoring.urls')),
]
