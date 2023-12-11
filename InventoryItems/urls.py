from django.urls import path, include 
from .views import DeviceDetailsView, DeviceListView, TransactionDetailView, TransactionListView, PendingApprovalView, SubmitTransactionView

urlpatterns = [
    path('', DeviceListView, name="base"),
    path('list/', DeviceListView, name="DeviceList"),
    path('details/', DeviceDetailsView, name="DeviceDetail"),
    path('details/<str:serial>/', DeviceDetailsView, name="DeviceDetail"),
    path('transactions/', TransactionListView, name="TransactionList"),
    path('transaction/<str:serial>/', TransactionDetailView, name="TransactionDetailView"),
    path('submit/', SubmitTransactionView, name="SubmitTransaction"),
    path('submit/<str:serial>/', SubmitTransactionView, name="SubmitTransaction"),
    path('approve/', PendingApprovalView, name ="PendingApproval")
]