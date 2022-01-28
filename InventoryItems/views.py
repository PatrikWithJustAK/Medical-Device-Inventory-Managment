from django.shortcuts import render

# Create your views here.

def DeviceListView(req):
    return render(req,"device_list.html")


def DeviceDetailsView(req):
    return render(req,"device_detail.html")

def TransactionListView(req):
    return render(req,"transaction_list.html")

def TransactionDetailView(req):
    return render(req,'transaction_detail.html')

def SubmitTransactionView(req):
    return render(req,'submit_transaction.html')

    