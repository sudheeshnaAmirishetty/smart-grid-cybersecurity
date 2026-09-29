from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='cybersecurity_index'),
    path('api/threats/', views.list_threats, name='cybersecurity_list'),
    path('api/threats/create/', views.create_threat, name='cybersecurity_create'),
    path('api/threats/<int:threat_id>/', views.threat_detail, name='cybersecurity_detail'),
    path('api/cia-classify/', views.cia_classification, name='cia_classification'),
]
