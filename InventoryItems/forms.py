import datetime
import uuid
from django.forms import ModelForm
from .models import Transaction


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = "__all__"
        exclude = ('transaction_id', 'transaction_date')
    def form_valid(self, form):
        form.instance.transaction_date = datetime.datetime.now() #set the author to the profile of the user who submitted the blogpost
        form.instance.transaction_id = uuid.uuid4
        return super().form_valid(form)
