
from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


from .models import BaseItem, Requirement, Quotation, Job, Invoice, InvoiceItem

class BaseItemForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False)
    cancel_reason = forms.CharField(label=_('Cancellation Reason'), widget=forms.Textarea(attrs={'rows': 3}), required=False)
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
    rejection_reason = forms.CharField(label=_('Rejection Reason'), widget=forms.Textarea(attrs={'rows': 3}), required=False)
    return_reason = forms.CharField(label=_('Return Reason'), widget=forms.Textarea(attrs={'rows': 3}), required=False)

    class Meta:
        model = Requirement
        fields = ['customer', 'title', 'description', 'deadline', 'status', 'owner']
        

class QuotationForm(BaseItemForm):
    terms = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False)
    rejection_reason = forms.CharField(label=_('Rejection Reason'), widget=forms.Textarea(attrs={'rows': 3}), required=False)
    return_reason = forms.CharField(label=_('Return Reason'), widget=forms.Textarea(attrs={'rows': 3}), required=False)
    approval_comment = forms.CharField(label=_('Approval Comment'), widget=forms.Textarea(attrs={'rows': 3}), required=False)
    negotiate_comment = forms.CharField(label=_('Negotiate Comment'), widget=forms.Textarea(attrs={'rows': 3}), required=False)


    class Meta:
        model = Quotation
        fields = ['customer', 'title', 'description', 'deadline', 'price', 'currency', 'terms', 'validity', 'requirement', 'status', 'owner']

class JobForm(BaseItemForm):
    terms = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False)
    return_reason = forms.CharField(label=_('Return Reason'), widget=forms.Textarea(attrs={'rows': 3}), required=False)
    close_comment = forms.CharField(label=_('Closing Comment'), widget=forms.Textarea(attrs={'rows': 3}), required=False)

    class Meta:
        model = Job
        fields = ['customer', 'title', 'description', 'deadline', 'price', 'currency', 'terms', 'quotation', 'status', 'invoiced', 'paid', 'owner']


class InvoiceForm(BaseItemForm):
    class Meta:
        model = Invoice
        fields = ['customer', 'title', 'description', 'deadline', 'price', 'currency', 'tax_code', 'tax_pct', 'status', 'job', 'owner']


class WebRequirementForm(forms.ModelForm):
    """ 
    This for is a simplified version with more clear explanations for the web user that submits a
    requirement for the first time
    """
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False)
    #deadline = forms.DateField(widget=DatePickerInput, required=False)
    create_user = forms.BooleanField(initial=False, required=False)
    password1 = forms.CharField(widget=forms.PasswordInput, required=False)
    email = forms.EmailField()
    

    class Meta:
        model = Requirement
        fields = ['title', 'description', 'deadline']

    def clean_deadline(self):
        deadline = self.cleaned_data['deadline']
        today = timezone.now().date()
        if deadline:
            if deadline < today:
                raise forms.ValidationError(_('Date must be in the future'))
        return deadline

    def clean_password1(self):
        password = self.cleaned_data['password1']
        if self.cleaned_data['create_user'] and password=='':
            raise forms.ValidationError(_('You must input a password to create the user'))
        if self.cleaned_data['create_user']==False and password!='':
            raise forms.ValidationError(_('Please confirm that you want to create the user with the checkbox'))
        
        return password

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].label = _('How can we help?')
        self.fields['title'].help_text = _('Let us briefly know what you need')

        self.fields['description'].label = _('Can you give us more details?')
        self.fields['description'].help_text = ''

        self.fields['deadline'].label = _('When would you need a solution')
        self.fields['deadline'].help_text = _('Let us know, either here or in the box above an idea of your timelines')

        # self.fields['file'].label = _('Attach documents here')
        # self.fields['file'].help_text = _('You can upload here more info in a file or zip file if you have multiple files')

        self.fields['email'].label = _('How can we contact you?')
        self.fields['email'].help_text = _('Provide us with your main email address')

        self.fields['password1'].label = _('(Optional) Create a password')
        self.fields['password1'].help_text = _('If you want to create an account with us and be able to access your request, please set up a password')

        self.fields['create_user'].label = _('Create account?')
        self.fields['create_user'].help_text = _('Check this box to confirm that you want to create your user')


class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['title', 'description', 'quantity', 'price', 'tax_code', 'tax_pct']
        widgets = {
            'invoice': forms.HiddenInput(),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'tax_code': forms.Select(attrs={'class': 'form-control'}),
            'tax_pct': forms.NumberInput(attrs={'class': 'form-control'}),
        }