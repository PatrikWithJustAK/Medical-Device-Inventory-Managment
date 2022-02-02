import datetime
import uuid
from django.forms import ModelForm

from Profiles.models import Profile
from ServiceCenter.models import ServiceCenter
from .models import Transaction

class TransactionForm(ModelForm):
    class Meta:
        model=Transaction
        fields = "__all__"


class TransactionSubmitForm(ModelForm):

    class Meta:
        model = Transaction
        fields = "__all__"
        exclude = ('transaction_id', 'transaction_date', 'submitter', 'approver')


