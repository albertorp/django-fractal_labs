
from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


from .models import FileAttachment

class FileAttachmentForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False)
    

    class Meta:
        model = FileAttachment
        fields = ['title', 'description', 'type', 'file', 'owner', 'submitted_by']

    
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)