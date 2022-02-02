from django.utils import timezone
from django.shortcuts import render
from .models import Transaction, DeviceInstance
from InventoryItems.forms import TransactionForm, TransactionSubmitForm
from Profiles.models import Profile
from ServiceCenter.models import ServiceCenter


# Create your views here.

def DeviceListView(req):
    devices = DeviceInstance.objects.all()
    if req.method=="POST":
        searchparams=req.POST['search']
        print(searchparams)
        devices= DeviceInstance.objects.filter(serial_number__contains=searchparams)
        context= {"devices": devices}
        return render(req,"device_list.html", context)
    context= {"devices": devices}
    return render(req,"device_list.html", context)


def DeviceDetailsView(req, serial):
    sn=serial
    device = DeviceInstance.objects.get(serial_number=sn)
    context = {"device":device}
    return render(req,"device_detail.html", context)

def TransactionListView(req):
    return render(req,"transaction_list.html")

def TransactionDetailView(req, serial):
    profile = Profile.objects.get(user=req.user)
    sn= serial
    transactions = Transaction.objects.filter(serial_number=sn)
    context = {"transactions": transactions}

    return render(req,'transaction_detail.html', context)

def SubmitTransactionView(req, *args, **kwargs):
    serial = kwargs.get('serial')
    context = {}
    if req.method =="GET":
        if kwargs:
            serial = kwargs.get('serial')
            device = DeviceInstance.objects.get(serial_number=serial)
            location = device.service_center
            transaction_date = timezone.now
            submitter=Profile.objects.get(user=req.user)
            service_center = ServiceCenter.objects.get(name=submitter.home_center)
            form = TransactionSubmitForm(initial={'transaction_date':transaction_date,'serial_number':serial,'service_center':service_center, 'equipment_status':device.equipment_status, 'customer_id':device.customer_id, 'location_status':device.location_status, 'software_version':device.software_version})
            context = {"form":form,
            "transaction_date":transaction_date,
            "submitter":submitter,
            "location":location,
            "service_center":service_center,
            "device":device,
            "sn":serial
            }
            return render(req,'submit_transaction.html', context)
    user=req.user
    form = TransactionSubmitForm()
    submitter= Profile.objects.get(user=req.user)
    location = ServiceCenter.objects.get(name=submitter.get_center())
    approver = location.manager
    transaction_date=timezone.now()
    context = {"form": form}
    if req.method == "POST":
            form=TransactionSubmitForm(req.POST, timezone.now())
            submitter= Profile.objects.get(user =req.user)
            location = ServiceCenter.objects.get(name=submitter.get_center())
            if form.is_valid():
                t=form.save(commit=False)
                t.submitter=submitter
                t.location = location
                t.approver = approver
                t.transaction_date = timezone.now()
                t.save()

    return render(req,'submit_transaction.html', context)


def PendingApprovalView(req):
    profile = Profile.objects.get(user=req.user)
    transactions = Transaction.objects.filter(approver=profile, approved=False)
    context= {"transactions": transactions}
    if req.method=="POST":
        t=req.POST['transaction']
        transaction = Transaction.objects.get(transaction_id=t)
        sn = transaction.serial_number 
        device = DeviceInstance.objects.get(serial_number=sn)
        device.location_status = transaction.location_status
        device.equipment_status = transaction.equipment_status
        device.service_center = transaction.service_center
        device.software_version = transaction.software_version
        device.customer_id= transaction.customer_id
        transaction.approved = True
        transaction.save()
        device.save()
        
        return render(req, 'pending_transactions.html', context)

    return render(req, 'pending_transactions.html', context)

    