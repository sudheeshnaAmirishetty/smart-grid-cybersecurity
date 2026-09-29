from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='monitoring_index'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('register/', views.register, name='register'),
    path('<str:key>/', views.module_detail, name='module_detail'),
]
