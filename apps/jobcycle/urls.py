from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'jobcycle'

urlpatterns = [   
    # Basic empty templates just for testing purposes
    path(
        "requirements/",
        login_required(
            TemplateView.as_view(
                template_name="jobcycle/item_list.html",
                extra_context={"active_tab": "requirements"},
            )
        ),
        name="requirement_list",
    ),

    path(
        "quotations/",
        login_required(
            TemplateView.as_view(
                template_name="jobcycle/item_list.html",
                extra_context={"active_tab": "quotations"},
            )
        ),
        name="quotation_list",
    ),

    path(
        "jobs/",
        login_required(
            TemplateView.as_view(
                template_name="jobcycle/item_list.html",
                extra_context={"active_tab": "jobs"},
            )
        ),
        name="job_list",
    ),

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