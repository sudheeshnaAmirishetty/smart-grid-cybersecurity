from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='sdn_index'),
    path('api/rules/', views.list_rules, name='sdn_list'),
    path('api/rules/create/', views.create_rule, name='sdn_create'),
    path('api/rules/<int:rule_id>/', views.rule_detail, name='sdn_detail'),
]
