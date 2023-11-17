from django.contrib import messages
from django.forms.models import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, UpdateView, CreateView, DetailView

from .utils import get_buttons_invoice

from apps.customers.models import Customer
from .models import BaseItem, Job, Invoice, InvoiceItem
from .forms import InvoiceForm, InvoiceItemForm
from .views import BaseItemListView, BaseItemDetailView, BaseItemCreateView, BaseItemUpdateView


class InvoiceListView(BaseItemListView):
    model = Invoice
    title = _('List of Invoices')
    active_tab = 'invoices'
    template_name = 'jobcycle/invoices/invoice_list.html'



class InvoiceDetailView(BaseItemDetailView):
    model = Invoice
    title = _('Invoice Details')
    item_type = 'invoice'
    active_tab = 'invoices'



  

class InvoiceUpdateView(BaseItemUpdateView):
    model = Invoice
    form_class = InvoiceForm
    success_url = reverse_lazy('jobcycle:invoice_list')
    title = _('Invoice Update')
    item_type = 'invoice'
    active_tab = 'invoices'
    template_name = 'jobcycle/invoices/invoice_update.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['buttons'] = get_buttons_invoice(self.object.status)
        return ctx
    
    def form_valid(self, form):
        if 'save' in self.request.POST:
            messages.success(self.request, _('Invoice saved'))

        return super().form_valid(form)




class InvoiceCreateView(BaseItemCreateView):
    model = Invoice
    form_class = InvoiceForm
    success_url = reverse_lazy('jobcycle:invoice_list')
    title = _('Create Invoice')
    item_type = 'invoice'
    active_tab = 'invoices'




def _add_edit_invoiceitem_htmx(request, invoiceitem=None, invoice=None):
    if request.method == "POST":
        
        form = InvoiceItemForm(request.POST, instance=invoiceitem)
        if form.is_valid():
            invoiceitem = form.save(commit=False)
            # Additional processing
            invoiceitem.invoice = invoice
            invoiceitem.save()

            # TODO Calculate subtotals for the parent invoice and update it
            #return render(request,"jobcycle/invoices/invoiceitem_list_row.html",{"item": invoiceitem,})
            return HttpResponseRedirect(reverse("jobcycle:invoice_update", args=[invoiceitem.invoice.id]))
    else:
        # initial_data = {
        #     'tax_pct': 0.00,
        #     'title': 'titulo automatico',
        #     #'field2': 42,  # Initial Value for Field 2
        #     # Add more initial values as needed
        # }
        form = InvoiceItemForm(instance=invoiceitem)

    return render(
        request,
        "jobcycle/invoices/invoiceitem_list_row_form.html",
        {
            "invoiceitem": invoiceitem,
            "invoice": invoice,
            "form": form,
        },
    )


def add_invoiceitem_row_htmx(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    return _add_edit_invoiceitem_htmx(request, invoice=invoice)


def edit_invoiceitem_row_htmx(request, invoice_id, pk):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    invoiceitem = get_object_or_404(InvoiceItem, pk=pk)
    return _add_edit_invoiceitem_htmx(request, invoiceitem=invoiceitem, invoice=invoice)

