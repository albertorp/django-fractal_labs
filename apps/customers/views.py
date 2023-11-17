from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, UpdateView, CreateView

from .models import Customer
from .forms import CustomerForm
# Create your views here.


class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer  
    template_name = 'customers/customer_list.html' 
    context_object_name = 'customer_list' 
    list_display = ('id', 'email', 'user', 'tax_id_number', 'stripe_customer_id', 'created_at')
    title = _('Customers')
    active_tab = 'customers'

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['active_tab'] = self.active_tab
        context['model_name'] = self.model.__name__
        context['fields'] = self.list_display
        return context
    


class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    template_name = 'customers/customer_update.html'
    form_class = CustomerForm
    success_url = reverse_lazy('customers:customer_list')
    title = _('Customer Update')
    active_tab = 'customers'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = self.title
        ctx['active_tab'] = self.active_tab
        return ctx

    def get_form_kwargs(self):
        """ Used to pass the logged in user to the form in order to enable/disable fields """
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    

    def form_valid(self, form):
        if 'save' in self.request.POST:
            messages.success(self.request, _('Customer saved'))

        if 'cancel' in self.request.POST:
            messages.info(self.request, _('Operation cancelled'))
            return HttpResponseRedirect(self.get_success_url())


        return super().form_valid(form)


class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer 
    template_name = 'customers/customer_update.html'
    form_class = CustomerForm
    success_url = reverse_lazy('customers:customer_list')
    title = _('Customer Create')
    active_tab = 'customers'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = self.title
        ctx['active_tab'] = self.active_tab
        return ctx

    def get_form_kwargs(self):
        """ Used to pass the logged in user to the form in order to enable/disable fields """
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs