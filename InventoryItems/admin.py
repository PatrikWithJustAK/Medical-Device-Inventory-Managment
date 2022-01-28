from django.contrib import admin
from .models import InventoryEquipmentType, Transaction, DeviceInstance

# Register your models here.
admin.site.register(InventoryEquipmentType)
admin.site.register(DeviceInstance)
admin.site.register(Transaction)
