import django_filters

from .models import BaseItem, Requirement

class BaseItemFilter(django_filters.FilterSet):
    #amount = django_filters.RangeFilter()
    deadline = django_filters.DateFromToRangeFilter()
    created_at = django_filters.DateFromToRangeFilter()
    #date_year = django_filters.NumberFilter(field_name='date', lookup_expr='year')


    class Meta:
        model = None
        fields = {
            #'date': ['exact', 'gt', 'gte', 'lt', 'lte'],
            #'amount': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'title': ['icontains'],
            'customer': ['exact'],
            'owner': ['exact'],
            'status': ['exact'],
        }
        #fields = ['date', 'amount', 'description', 'source_acc', 'dest_acc']
        #order_by = ['-date']

class RequirementFilter(BaseItemFilter):
    class Meta:
        model = Requirement
        fields = {
            'title': ['icontains'],
            'customer': ['exact'],
            'owner': ['exact'],
            'status': ['exact'],
        }
        