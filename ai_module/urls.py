from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='ai_index'),
    path('api/anomalies/', views.list_anomalies, name='ai_list'),
    path('api/anomalies/analyze/', views.analyze_data, name='ai_analyze'),
    path('api/anomalies/<int:anom_id>/', views.anomaly_detail, name='ai_detail'),
]
