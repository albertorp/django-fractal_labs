from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'customers'

urlpatterns = [   
    path('', views.CustomerListView.as_view(), name='customer_list'),
    path('<int:pk>/', views.CustomerUpdateView.as_view(), name='customer_update'),
    path('create/', views.CustomerCreateView.as_view(), name='customer_create'),
    # path('<int:pk>/excel_export', views.ExcelExportView.as_view(), name='excel_export'),
      
]