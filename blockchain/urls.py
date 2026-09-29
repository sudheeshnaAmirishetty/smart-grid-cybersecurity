from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='blockchain_index'),
    path('audit/', views.audit_dashboard, name='blockchain_audit_page'),
    path('api/transactions/', views.list_transactions, name='blockchain_list'),
    path('api/transactions/create/', views.create_transaction, name='blockchain_create'),
    path('api/transactions/audit/', views.audit_log, name='blockchain_audit'),
    path('api/transactions/<str:tx_id>/', views.transaction_detail, name='blockchain_detail'),
]
