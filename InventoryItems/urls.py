from django.urls import path, include 
from .views import * 

urlpatterns = [
    path('list/', DeviceListView, name="DeviceList"),
    path('details/', DeviceDetailsView, name="DeviceDetail"),
    path('transactions/', TransactionListView, name="TransactionList"),
    path('transaction/', TransactionDetailView, name="TransactionDetailView"),
    path('submit/', SubmitTransactionView, name="SubmitTransaction")
]