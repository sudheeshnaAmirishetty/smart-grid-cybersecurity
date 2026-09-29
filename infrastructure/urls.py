from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='infrastructure_index'),
    path('api/devices/', views.list_devices, name='infrastructure_list'),
    path('api/devices/create/', views.create_device, name='infrastructure_create'),
    path('api/devices/<int:device_id>/', views.device_detail, name='infrastructure_detail'),
]
