import django_filters

from .models import BaseItem, Requirement, Quotation, Job, Invoice

class BaseItemFilter(django_filters.FilterSet):
    deadline = django_filters.DateFromToRangeFilter()
    created_at = django_filters.DateFromToRangeFilter()

    class Meta:
        model = None
        fields = {
            'title': ['icontains'],
            'customer': ['exact'],
            'owner': ['exact'],
            'status': ['exact'],
        }

class QuotationFilter(BaseItemFilter):
    class Meta:
        model = Quotation
        fields = {
            'title': ['icontains'],
            'customer': ['exact'],
            'owner': ['exact'],
            'status': ['exact'],
        }
        
class RequirementFilter(BaseItemFilter):
    class Meta:
        model = Requirement
        fields = {
            'title': ['icontains'],
            'customer': ['exact'],
            'owner': ['exact'],
            'status': ['exact'],
        }

class JobFilter(BaseItemFilter):
    class Meta:
        model = Job
        fields = {
            'title': ['icontains'],
            'customer': ['exact'],
            'owner': ['exact'],
            'status': ['exact'],
        }