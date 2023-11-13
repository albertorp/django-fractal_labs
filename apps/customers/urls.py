from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'customers'

urlpatterns = [   
    path(
        "",
        login_required(
            TemplateView.as_view(
                template_name="customers/customer_list.html",
                extra_context={"active_tab": "customers"},
            )
        ),
        name="customer_list",
    ),
    # path('', views.CustomerListView.as_view(), name='customer_list'),
    # path('<int:pk>/', views.CustomerUpdateView.as_view(), name='customer_detail'),
    # path('create/', views.CustomerCreateView.as_view(), name='customer_create'),
    # path('<int:pk>/excel_export', views.ExcelExportView.as_view(), name='excel_export'),
      
]