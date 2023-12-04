from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import TemplateView

from . import views, views_invoices

app_name = 'jobcycle'

urlpatterns = [   
    path("requirements/", views.RequirementListView.as_view(), name="requirement_list"),
    path("requirements/<int:pk>", views.RequirementUpdateView.as_view(), name="requirement_update"),
    path('requirements/create', views.RequirementCreateView.as_view(), name='requirement_create'),
    path("requirements/<int:pk>/detail", views.RequirementDetailView.as_view(), name="requirement_detail"),

    path('contactus/', views.WebRequirementCreateView.as_view(), name='contactus'),
    path(
        'thanks/', 
        TemplateView.as_view(template_name = 'jobcycle/thanks.html'), 
        name='thanks'
        ),
    

    path("quotations/", views.QuotationListView.as_view(), name="quotation_list"),
    path("quotations/<int:pk>", views.QuotationUpdateView.as_view(), name="quotation_update"),
    path('quotations/create', views.QuotationCreateView.as_view(), name='quotation_create'),
    path("quotations/<int:pk>/detail", views.QuotationDetailView.as_view(), name="quotation_detail"),
   

    path("jobs/", views.JobListView.as_view(), name="job_list"),
    path("jobs/<int:pk>", views.JobUpdateView.as_view(), name="job_update"),
    path('jobs/create', views.JobCreateView.as_view(), name='job_create'),
    path("jobs/<int:pk>/detail", views.JobDetailView.as_view(), name="job_detail"),


    path("invoices/", views_invoices.InvoiceListView.as_view(), name="invoice_list"),
    path("invoices/<int:pk>", views_invoices.InvoiceUpdateView.as_view(), name="invoice_update"),
    path('invoices/create', views_invoices.InvoiceCreateView.as_view(), name='invoice_create'),
    path("invoices/<int:pk>/detail", views_invoices.InvoiceDetailView.as_view(), name="invoice_detail"),

    
    path("invoices/<int:pk>/add_line_item", views_invoices.add_invoiceitem_row_htmx, name="add_line_item"),
    path("invoices/<int:invoice_id>/edit_line_item/<int:pk>", views_invoices.edit_invoiceitem_row_htmx, name="edit_line_item"),
    path("invoices/<int:pk>/add_line_item/cancel", views_invoices.cancel_add_invoiceitem_row_htmx, name="cancel_add_line_item"),
    path("invoices/<int:invoice_id>/edit_line_item/<int:pk>/cancel", views_invoices.cancel_edit_invoiceitem_row_htmx, name="cancel_edit_line_item"),
    
    path("excel_export/", views.excel_export, name="excel_export"),

]