from datetime import datetime
import uuid
from django.db import models
from django.forms import CharField, DateTimeField


# Medical Device InventoryManagement can be used for many different types of equipment
# For example, this could be a wheelchair, CPAP equipment, or a ventilator 
# We need to know the manufacturer and model for each EquipmentType

EquipmentTypeChoices = (
    ("Vent", "Ventilator"),
    ("CPAP", "CPAP Device"),
    ("O2", "Oxygen Device"),
    ("Other", "Other Equipment"),
)

EquipmentStatusChoices = (
    ("A", "Active"),
    ("I", "Inactive"),
    ("R", "Retired"),
)

LocationStatusChoices = (
    ("SC", "At Service Center"),
    ("CU", "With the customer"),
    ("RC", "Sent to Repair Center"),
    ("RT", "Retired Unit"),
)

# This is the base class for a specific TYPE of equipment
class InventoryEquipmentType(models.Model):
    type = models.CharField("Type of Equipment", max_length=8, choices=EquipmentTypeChoices)
    manufacturer = models.CharField("What manufacturer makes this equipment?", max_length=50)
    model_number =models.CharField("Model Number for this equipment", max_length=50)
    def __str__(self):
        return str(self.model_number)

# DeviceInstance is the class for a specific INSTANCE of equipment
# Due to FDA regulations, many types of medical equipment MUST be serviced periodically
# Some types of equipment need to be serviced monthly, quarterly, or annually
# The purpose of this application is to document a history of all service calls for each DeviceInstance 
# This provides documentation of the client's compliance with FDA regulations
# In this use-case, every medical device is required to have a unique Serial Number
# We will also monitor the customer who is using the equipment (This could be plugged into an existing customer DB via foreignkey)
# location_status is used to describe the physical location of the equipment. It is either at the Service Center, With a patient, sent for repair, or MIA
# equipment_status is used to describe the functionality of the equipment. It is either Active (billing), Inactive (not billing), or Retired (not billing, no longer in use)
# Some types of equipment (Ventilators, Oxygen Concentrators, Life-sustaining devices) require a software check periodically to comply with FDA regulations

class DeviceInstance(models.Model):
    equipment_type = models.ForeignKey("InventoryItems.InventoryEquipmentType", verbose_name="Which Type of Equipment is this?", on_delete=models.CASCADE)
    serial_number = models.CharField("The Serial Number Of this Device", max_length=50)
    service_center = models.ForeignKey("ServiceCenter.ServiceCenter", verbose_name="Which service center is servicing this equipment?", on_delete=models.CASCADE)
    customer_id = models.CharField("ID of the customer using this equipment", max_length=50, null=True, default="")
    location_status = models.CharField("The current location of this equipment", choices = LocationStatusChoices, max_length=5, default="SC")
    equipment_status = models.CharField("Is this equipment actively billing?", choices = EquipmentStatusChoices, default="A", max_length=1)
    software_version = models.CharField("The current version of software on this equipment", max_length=20, default="", null=True)

    def __str__(self):
        return str(self.serial_number)

    def getSerial(self):
        return self.serial_number

# Transaction is the class to describe a single service check done on a single DeviceInstance
# This transaction shares a one-to-one relationship with a DeviceInstance, but a DeviceInstance will have many Transactions, so we access the Transactions via ForeignKey
# To maintain regulatory compliance, the DeviceInstance objects should never be edited directly by a non-clinical employee
# Typically each service_center will have one or more clincians who do these service checks
# The clinician should submit a "Transaction" that details every service check. 
# If any of the DeviceInstance data has changed (software updates, equipment picked up, transferred to another service center), then the data from the transaction will be sent to the service center manager
# Only the service center manager should have access to update DeviceInstance objects
# Regular clinicians can only send Transactions to the service center manager for approval
# This minimizes regulatory risk by ensuring that any data in the inventory management system has been checked by at least 2 employees: the employee who did the check, and the service center manager who confirms the data is accurate
# If a Transaction is not accurate, the service center manager can decline a Transaction, which will submit it back to the servicing employee to be reviewed and resubmitted
# Once a Transaction has been approved, the associated DeviceInstance will be updated with information from the most recent Transaction

class Transaction(models.Model):
    transaction_id = models.UUIDField("Unique ID of this transaction", default=uuid.uuid4)
    service_center = models.ForeignKey("ServiceCenter.ServiceCenter", verbose_name="Which service center is servicing this equipment?", on_delete=models.CASCADE)
    customer_id = models.CharField("ID of the customer using this equipment", max_length=50, null=True, default="")
    location_status = models.CharField("The current location of this equipment", choices = LocationStatusChoices, max_length=5)
    equipment_status = models.CharField("Is this equipment actively billing?", choices = EquipmentStatusChoices, max_length=1)
    software_version = models.CharField("The current version of software on this equipment", max_length=20, default="", null=True)
    serial_number = models.CharField("The Serial Number Of this Device", max_length=50, null=True)
    notes = models.TextField("Notes from this service visit", null=True)
    service_check_date =models.DateField("Date check was done MM/DD/YYYY", auto_now=False, auto_now_add=False)
    transaction_date = models.DateTimeField("When Transaction was submitted MM/DD/YY", auto_now=False, auto_now_add=False)
    submitter = models.ForeignKey("Profiles.Profile", verbose_name="The individual who submitted the transaction", on_delete=models.CASCADE, related_name="Submitter")
    approver = models.ForeignKey("Profiles.Profile", verbose_name="The individual who approves the transaction", on_delete=models.CASCADE)
    approved = models.BooleanField("Was this transaction approved by a manager?", default=False)
    def __str__(self):
        return str(self.serial_number) +  " - " + str(self.transaction_date)

    def get_transaction_id(self):
        return self.transaction_id



