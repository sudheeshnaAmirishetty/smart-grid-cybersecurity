from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='threat_index'),
    path('api/scenarios/', views.list_scenarios, name='threat_list'),
    path('api/scenarios/create/', views.create_scenario, name='threat_create'),
    path('api/scenarios/<int:scenario_id>/', views.scenario_detail, name='threat_detail'),
]
