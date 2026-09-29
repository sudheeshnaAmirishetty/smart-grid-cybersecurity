from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='iot_index'),
    path('upload/', views.upload_dataset, name='iot_upload'),
    path('api/messages/', views.list_messages, name='iot_list'),
    path('api/messages/create/', views.create_message, name='iot_create'),
    path('api/messages/detect/', views.detect_threat, name='iot_detect'),
    path('api/messages/<int:message_id>/', views.message_detail, name='iot_detail'),
    path('api/messages/sample/', views.sample_message, name='iot_sample'),
]
