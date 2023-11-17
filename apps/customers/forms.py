
from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


from .models import Customer

class CustomerForm(forms.ModelForm):
    billing_address = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False)
    

    class Meta:
        model = Customer
        fields = ['email', 'user', 'tax_id_number', 'stripe_customer_id', 'billing_address']

    
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

