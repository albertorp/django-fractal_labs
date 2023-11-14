
from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


from .models import BaseItem, Requirement, Quotation, Job

class BaseItemForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False)
    #terms = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False)
    #deadline = forms.DateField(widget=DatePickerInput, required=False)

    class Meta:
        model = BaseItem
        fields = ['customer', 'title', 'description', 'deadline']

    def clean_deadline(self):
        deadline = self.cleaned_data['deadline']
        today = timezone.now().date()
        if deadline:
            if deadline < today:
                raise forms.ValidationError(_('Date must be in the future'))
        return deadline
    
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)


class RequirementForm(BaseItemForm):
    class Meta:
        model = Requirement
        fields = ['customer', 'title', 'description', 'deadline', 'status', 'owner']
        

class QuotationForm(BaseItemForm):
    class Meta:
        model = Quotation
        fields = ['customer', 'title', 'description', 'deadline', 'price', 'currency', 'terms', 'validity', 'requirement', 'status', 'owner']

class JobForm(BaseItemForm):
    class Meta:
        model = Job
        fields = ['customer', 'title', 'description', 'deadline', 'price', 'currency', 'terms', 'quotation', 'status', 'invoiced', 'paid', 'owner']