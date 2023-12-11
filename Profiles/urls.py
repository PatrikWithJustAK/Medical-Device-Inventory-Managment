from django.urls import path, include 
from InventoryItems.views import PendingApprovalView
urlpatterns = [
        path('', PendingApprovalView, name ="PendingApproval")
]
