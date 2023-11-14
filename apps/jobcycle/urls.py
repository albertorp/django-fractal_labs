from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'jobcycle'

urlpatterns = [   
    path("requirements/", views.RequirementListView.as_view(), name="requirement_list"),
    path("requirements/<int:pk>", views.RequirementUpdateView.as_view(), name="requirement_update"),
    path('requirements/create', views.RequirementCreateView.as_view(), name='requirement_create'),
    

    path("quotations/", views.QuotationListView.as_view(), name="quotation_list"),
    path("quotations/<int:pk>", views.QuotationUpdateView.as_view(), name="quotation_update"),
    path('quotations/create', views.QuotationCreateView.as_view(), name='quotation_create'),
   

    path( "jobs/", views.JobListView.as_view(), name="job_list"),
    path("jobs/<int:pk>", views.JobUpdateView.as_view(), name="job_update"),
    path('jobs/create', views.JobCreateView.as_view(), name='job_create'),

    path(
        "invoices/",
        login_required(
            TemplateView.as_view(
                template_name="jobcycle/item_list.html",
                extra_context={"active_tab": "invoices"},
            )
        ),
        name="invoice_list",
    ),


   
      
]