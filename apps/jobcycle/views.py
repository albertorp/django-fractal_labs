from django.apps import apps
from django.db.models.fields.related import ForeignKey
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.forms.models import BaseModelForm, model_to_dict
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, UpdateView, CreateView, DetailView

from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress
from allauth.account.utils import send_email_confirmation

from openpyxl import Workbook

from .utils import get_buttons_requirement, get_buttons_quotation, get_buttons_job, get_buttons_webrequirement

from apps.customers.models import Customer
from apps.comments.models import Comment

from .models import BaseItem, Requirement, Quotation, Job
from .forms import RequirementForm, QuotationForm, JobForm, WebRequirementForm
from .filters import RequirementFilter, QuotationFilter, JobFilter



class WebRequirementCreateView(CreateView):
    model = Requirement
    form_class = WebRequirementForm
    template_name = 'jobcycle/contactus.html'
    success_url = reverse_lazy('jobcycle:thanks') #jobcycle:thanks
    title = _('Contact Us')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = self.title
        ctx['buttons'] = get_buttons_webrequirement()
        return ctx
    

    def form_valid(self, form):

        # Check to see if the email corresponds to an existing customer
        try:
            # If it does, save it under that user
            customer = Customer.objects.get(email=form.cleaned_data['email'])
        except: 
            # We get a new customer
            customer = Customer()
            customer.email = form.cleaned_data['email']
            customer.save()
        


        # Check to see if we need to create a nuew user
        if form.cleaned_data['create_user']:
            # If the visitor wants to create a user, we create a new user in the system and assign the requirement to the new user
            try:
                user = get_adapter().new_user(self.request)
                get_adapter().save_user(self.request, user, form)
                # Mark the email address as unverified
                email_address = EmailAddress.objects.create(
                    user=user,
                    email=form.cleaned_data['email'],
                    verified=False
                )
                email_address.set_as_primary()
                # Send the verification email
                send_email_confirmation(self.request, user)
                user.save()
                customer.user = user
                customer.save()
            except:
                # The user already exists, so we omit the creation
                messages.error(self.request, _('The user already exists'))

            
            

        form.instance.customer = customer
        return super().form_valid(form)



class BaseItemListView(LoginRequiredMixin, ListView):
    model = BaseItem  
    template_name = 'jobcycle/item_list.html' 
    context_object_name = 'items' 
    list_display = ('id', 'customer', 'title', 'created_at', 'status', 'deadline', 'owner')
    paginate_by = 10
    #ordering = ['-date_created']  # Optionally, specify how you want to order the items
    
    def get_queryset(self):
        """
        If the user is not staff, filter to only show items belonging to the
        current user's customer.
        
        """
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            return qs.filter(customer=self.request.user.customer)
        return(qs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['active_tab'] = self.active_tab
        context['model_name'] = self.model.__name__
        context['fields'] = self.list_display

        if hasattr(self, 'filterset'):
            context['form_filter'] = self.filterset.form

        if not self.request.GET:
            context['extra_param'] = '?page='
        else:
            context['extra_param'] = '&page='

        return context
    


class RequirementListView(BaseItemListView):
    model = Requirement
    title = _('List of Requirements')
    active_tab = 'requirements'

    def get_queryset(self):
        qs = super().get_queryset()
        if 'all' in self.request.GET:
            # If 'all' is in the request.GET, reset self.filterset and return all values in qs
            self.filterset = RequirementFilter(None, queryset=qs)
            return qs
        else:
            # If 'all' is not in request.GET, apply filters using RequirementFilter
            self.filterset = RequirementFilter(self.request.GET, queryset=qs)
            return self.filterset.qs


    


class QuotationListView(BaseItemListView):
    model = Quotation
    title = _('List of Quotations')
    active_tab = 'quotations'

    def get_queryset(self):
        qs = super().get_queryset()
        if 'all' in self.request.GET:
            # If 'all' is in the request.GET, reset self.filterset and return all values in qs
            self.filterset = QuotationFilter(None, queryset=qs)
            return qs
        else:
            # If 'all' is not in request.GET, apply filters using QuotationFilter
            self.filterset = QuotationFilter(self.request.GET, queryset=qs)
            return self.filterset.qs

class JobListView(BaseItemListView):
    model = Job
    title = _('List of Jobs')
    active_tab = 'jobs'

    def get_queryset(self):
        qs = super().get_queryset()
        if 'all' in self.request.GET:
            # If 'all' is in the request.GET, reset self.filterset and return all values in qs
            self.filterset = JobFilter(None, queryset=qs)
            return qs
        else:
            # If 'all' is not in request.GET, apply filters using JobFilter
            self.filterset = JobFilter(self.request.GET, queryset=qs)
            return self.filterset.qs


class BaseItemDetailView(LoginRequiredMixin, DetailView):
    model = None # Must be defined in derived class
    template_name = 'jobcycle/item_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = self.title
        ctx['item_type'] = self.item_type
        ctx['active_tab'] = self.active_tab

        instance = self.object
        instance_dict = {instance._meta.get_field(key).verbose_name if hasattr(instance._meta.get_field(key), 'verbose_name') else key: getattr(instance, key) for key in model_to_dict(instance).keys()}
        ctx['object_dict'] = instance_dict

        return ctx


class RequirementDetailView(BaseItemDetailView):
    model = Requirement
    title = _('Requirement Details')
    item_type = 'requirement'
    active_tab = 'requirements'


class QuotationDetailView(BaseItemDetailView):
    model = Quotation
    title = _('Quotation Details')
    item_type = 'quotation'
    active_tab = 'quotations'


class JobDetailView(BaseItemDetailView):
    model = Job
    title = _('Job Details')
    item_type = 'job'
    active_tab = 'jobs'


class BaseItemUpdateView(LoginRequiredMixin, UpdateView):
    model = None # Must be defined in derived class
    template_name = 'jobcycle/item_update.html'
    additional_form_fields_template = None

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = self.title
        ctx['item_type'] = self.item_type
        ctx['active_tab'] = self.active_tab
        ctx['comments'] = self.object.comments.all()
        ctx['comment_count'] = self.object.comments.count()
        ctx['attachments'] = self.object.attachments.all()
        ctx['attachment_count'] = self.object.attachments.count()
        ctx['additional_form_fields_template'] = self.additional_form_fields_template
        return ctx

    def get_form_kwargs(self):
        """ Used to pass the logged in user to the form in order to enable/disable fields """
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    
    def form_invalid(self, form):
        messages.error(self.request, _('Please check errors and try again'))
        return super().form_invalid(form)

    

class RequirementUpdateView(BaseItemUpdateView):
    model = Requirement
    form_class = RequirementForm
    success_url = reverse_lazy('jobcycle:requirement_list')
    title = _('Requirement Update')
    item_type = 'requirement'
    active_tab = 'requirements'
    additional_form_fields_template = None

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['buttons'] = get_buttons_requirement(self.object.status)
        return ctx
    
    def form_valid(self, form):
        if 'save' in self.request.POST:
            messages.success(self.request, _('Requirement saved'))

        if 'analyse' in self.request.POST:
            form.instance.status = Requirement.Status.ANALYSIS
            #form.instance.rw = Requirement.ReadWrite.WRITE_STAFF
            # Prepare a standard "We are reviewing your requirement" email
            # Send email
            messages.success(self.request, _('Requirement sent for Analysis'))

        if 'quote' in self.request.POST:
            form.instance.status = Requirement.Status.TO_QUOTE
            #form.instance.rw = Requirement.ReadWrite.READ_ONLY
            
            # Create a Quotation Object
            quotation = Quotation()

            # Copy as much data from the requirement to the quotation as possible
            req = self.get_object()
            quotation.title = req.title
            quotation.description = req.description
            quotation.customer = req.customer
            quotation.deadline = req.deadline
            quotation.status = Quotation.Status.DRAFT
            quotation.owner = req.owner
            quotation.requirement = req

            # Save the Quotation object
            quotation.save()
            
            # # Copy all RequirementAttachment objects as QuotationAttachment objects
            # for req_attachment in req.requirementattachment_set.all():
            #     quotation_attachment = QuotationAttachment(
            #         item=quotation,
            #         title=req_attachment.title,
            #         description=req_attachment.description,
            #         submitted_by=req_attachment.submitted_by,
            #     )
            #     import os
            #     filename = os.path.basename(req_attachment.file.name)
            #     quotation_attachment.file.save(filename, req_attachment.file, save=False)
            #     quotation_attachment.save()
            
            # Create a new Comment associated with the Requirement and the complementary for the new quotation
            req = self.get_object()
            comment_text = _('Requirement closed and new Quotation created with ID: ') + str(quotation.id)
            comment = Comment.objects.create(
                user=self.request.user, 
                text=comment_text,
                content_type=ContentType.objects.get_for_model(req),
                object_id=req.pk
            )
            quotation_comment = _('Quotation created from Requirement with ID: ') + str(req.id)
            comment = Comment.objects.create(
                user=self.request.user, 
                text=quotation_comment,
                content_type=ContentType.objects.get_for_model(quotation),
                object_id=quotation.pk
            )

            messages.success(self.request, comment_text)
        
        if 'return' in self.request.POST:
            form.instance.status = Requirement.Status.RETURNED
            # Prepare a standard "Returned" email with additional information
            # Send email

            # Create a new Comment associated with the Requirement
            req = self.get_object()
            comment_text = _('Requirement was returned to the customer with this message: ') + form.cleaned_data['return_reason']  
            comment = Comment.objects.create(
                user=self.request.user, 
                text=comment_text,
                content_type=ContentType.objects.get_for_model(req),
                object_id=req.pk
            )

            messages.warning(self.request, _('Requirement Returned to the Customer'))

        if 'reject' in self.request.POST:
            form.instance.status = Requirement.Status.REJECTED
            #form.instance.rw = Requirement.ReadWrite.READ_ONLY
            # Prepare a standard "No Bid" email
            # Send email

            # Create a new Comment associated with the Requirement
            req = self.get_object()
            comment_text = _('Requirement was rejected with this reason: ') + form.cleaned_data['rejection_reason']  
            comment = Comment.objects.create(
                user=self.request.user, 
                text=comment_text,
                content_type=ContentType.objects.get_for_model(req),
                object_id=req.pk
            )

            messages.warning(self.request, _('Requirement Rejected'))

        return super().form_valid(form)

class QuotationUpdateView(BaseItemUpdateView):
    model = Quotation
    form_class = QuotationForm
    success_url = reverse_lazy('jobcycle:quotation_list')
    title = _('Quotation Details/Update')
    item_type = 'quotation'
    active_tab = 'quotations'
    additional_form_fields_template = "jobcycle/quotations/additional_form_fields_quotations.html"

    def form_valid(self, form):
        if 'save' in self.request.POST:
            messages.success(self.request, _('Quotation saved'))

        if 'send' in self.request.POST:
            # The quotation is ready to be sent to the customer
            
            # Check that the price has a positive value
            # TODO Refactor this to a "validate_quote" method (validate price, currency, terms...)
            price = form.cleaned_data['price']
            if price is None or price < 0:
                form.add_error('price', _('Price must be greater than or equal to 0.'))
                messages.error(self.request, _('Please check errors and try again'))
                return self.form_invalid(form)
            form.instance.status = Quotation.Status.SENT
            #form.instance.rw = Quotation.ReadWrite.READ_ONLY
            # Prepare a standard "Your quotation is ready" email
            # Send email
            messages.success(self.request, _('Quotation sent to the customer'))

        if 'approved' in self.request.POST:

            # TODO when the customer hits 'Approved', there should be a confirmation screen
            # to make sure and record that they know the terms and conditions
            
            form.instance.status = Quotation.Status.APPROVED
            #form.instance.rw = Quotation.ReadWrite.READ_ONLY
            # Create a Job Object
            job = Job()

            # Copy as much data from the quotation to the job as possible
            quotation = self.get_object()
            job.title = quotation.title
            job.description = quotation.description
            job.customer = quotation.customer
            job.deadline = quotation.deadline
            job.status = Job.Status.DRAFT
            job.price = quotation.price
            job.currency = quotation.currency
            job.terms = quotation.terms
            job.quotation = quotation
            #job.rw = Job.ReadWrite.WRITE_STAFF

            # Save the Job object
            job.save()

            
            # Copy all QuotationAttachment objects as JobAttachment objects
            # for q_attachment in quotation.quotationattachment_set.all():
            #     job_attachment = JobAttachment(
            #         item=job,
            #         title=q_attachment.title,
            #         description=q_attachment.description,
            #         submitted_by=q_attachment.submitted_by,
            #     )
            #     import os
            #     filename = os.path.basename(q_attachment.file.name)
            #     job_attachment.file.save(filename, q_attachment.file, save=False)
            #     job_attachment.save()


            messages.success(self.request, _('Quotation approved and Job created'))

        if 'rejected' in self.request.POST:
            
            # TODO Make sure there are Rejection comments

            form.instance.status = Quotation.Status.REJECTED
            #form.instance.rw = Quotation.ReadWrite.READ_ONLY
            # Log the rejection cause
            messages.info(self.request, _('Quotation Rejected'))

        if 'negotiate' in self.request.POST:
            form.instance.status = Quotation.Status.NEGOTIATE
            #form.instance.rw = Quotation.ReadWrite.READ_ONLY
            messages.info(self.request, _('Quotation is under negotiation'))

        if 'cancel' in self.request.POST:
            form.instance.status = Quotation.Status.CANCELLED
            #form.instance.rw = Quotation.ReadWrite.READ_ONLY
            # Log the cancellation cause
            messages.warning(self.request, _('Quotation Cancelled'))

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['buttons'] = get_buttons_quotation(self.object.status)
        return ctx

class JobUpdateView(BaseItemUpdateView):
    model = Job
    form_class = JobForm
    success_url = reverse_lazy('jobcycle:job_list')
    title = _('Job Details/Update')
    item_type = 'job'
    active_tab = 'jobs'
    additional_form_fields_template = "jobcycle/jobs/additional_form_fields_jobs.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['buttons'] = get_buttons_job(self.object.status)
        return ctx


    def form_valid(self, form):
        if 'save' in self.request.POST:            
            messages.success(self.request, _('Job saved'))

        if 'assign' in self.request.POST:
            form.instance.status = Job.Status.NOT_STARTED
            #form.instance.rw = Job.ReadWrite.WRITE_STAFF
            messages.success(self.request, _('Job has been planned and can now be started'))

        if 'start' in self.request.POST:
            form.instance.status = Job.Status.IN_PROGRESS
            #form.instance.rw = Job.ReadWrite.WRITE_STAFF
            messages.success(self.request, _('Job has been started'))

        if 'review' in self.request.POST:
            form.instance.status = Job.Status.IN_REVIEW
            #form.instance.rw = Job.ReadWrite.WRITE_STAFF
            messages.success(self.request, _('Job has been sent for review'))

        if 'deliver' in self.request.POST:
            form.instance.status = Job.Status.DELIVERED
            #form.instance.rw = Job.ReadWrite.READ_ONLY
            messages.success(self.request, _('Job has been sent to the customer and we are waiting for approval'))


        if 'return' in self.request.POST:
            if self.object.status == Job.Status.IN_REVIEW:
                # The work has been returned for corrections by the reviewer
                form.instance.status = Job.Status.IN_PROGRESS 
                messages.success(self.request, _('Job has been returned for corrections'))
            else:
                # Make sure that the return button can only be sent as for these 2 status
                # If we get here, the work has been returned by the customer
                form.instance.status = Job.Status.REWORK
                messages.success(self.request, _('Job has been returned for REWORK by the customer'))
            
            
        # if 'invoice' in self.request.POST:
        #     form.instance.status = Job.Status.INVOICED
        #     form.instance.rw = Job.ReadWrite.READ_ONLY
        #     messages.success(self.request, _('Invoice for the Job has been prepared and sent to the customer'))

        # if 'paid' in self.request.POST:
        #     form.instance.status = Job.Status.PAID
        #     form.instance.rw = Job.ReadWrite.READ_ONLY
        #     messages.success(self.request, _('Invoice for this Job has been paid'))

        if 'close' in self.request.POST:
            form.instance.status = Job.Status.CLOSED
            messages.success(self.request, _('Job has been closed'))

        
        if 'cancel' in self.request.POST:
            form.instance.status = Job.Status.CANCELLED
            # Log the cancellation cause
            messages.warning(self.request, _('Job Cancelled'))

        return super().form_valid(form)

class BaseItemCreateView(LoginRequiredMixin, CreateView):
    model = None # Must be defined in derived class
    template_name = 'jobcycle/item_update.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = self.title
        ctx['item_type'] = self.item_type
        ctx['active_tab'] = self.active_tab
        ctx['create'] = True
        return ctx

    def get_form_kwargs(self):
        """ Used to pass the logged in user to the form in order to enable/disable fields """
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class RequirementCreateView(BaseItemCreateView):
    model = Requirement
    form_class = RequirementForm
    success_url = reverse_lazy('jobcycle:requirement_list')
    title = _('Create Requirement')
    item_type = 'requirement'
    active_tab = 'requirements'

class QuotationCreateView(BaseItemCreateView):
    model = Quotation
    form_class = QuotationForm
    success_url = reverse_lazy('jobcycle:quotation_list')
    title = _('Create Quotation')
    item_type = 'quotation'
    active_tab = 'quotations'

class JobCreateView(BaseItemCreateView):
    model = Job
    form_class = JobForm
    success_url = reverse_lazy('jobcycle:job_list')
    title = _('Create Job')
    item_type = 'job'
    active_tab = 'jobs'



def excel_export(request):
    """
    This method exports the tables from our apps into an excel file. This allows for a very simple backup for
    our users

    TODO: Change the models to be exported so that they can be defined in the settings file. These list should be updated 
    when new models are added

    """
    now_str = timezone.now().strftime('%Y-%m-%d %H%M')
    file_name = 'Data ' + ' - ' + now_str + '.xlsx'

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'

    # Prepare the Excel file
    workbook = Workbook()
    # By default, OpenPyXL creates a new workbook with one sheet named "Sheet". 
    # To remove this sheet, you can simply delete it after creating the workbook, 
    # before adding any other sheets.
    default_sheet = workbook.get_sheet_by_name('Sheet')
    workbook.remove_sheet(default_sheet)

    
    models = [
        'customers.Customer',
        'jobcycle.Requirement',
        'jobcycle.Quotation',
        'jobcycle.Job',
        'jobcycle.Invoice',
        'comments.Comment',
        'users.CustomUser'
        ]
    
    for model_path in models:

        # Get the model and queryset
        model = apps.get_model(model_path)
        print(f"Model Name: {model.__name__}")
        qs = model.objects.all()

        # Create a worksheet for the queryset
        worksheet = workbook.create_sheet(title=model.__name__)
        fields = [field.name for field in qs.model._meta.fields]
        worksheet.append(fields)

        # Write the queryset rows into the worksheet
        for obj in qs:
            row = []
            for field in fields:
                # Check if the field is a ForeignKey
                if isinstance(qs.model._meta.get_field(field), ForeignKey):
                    # Get the ID of the related object
                    related_object = getattr(obj, field)
                    row_value = str(related_object.id) if related_object else None
                elif getattr(qs.model._meta.get_field(field), 'choices', None):
                    # If the field has choices, use the get_FOO_display() method
                    display_method = f'get_{field}_display'
                    row_value = str(getattr(obj, display_method)())
                else:
                    # For other fields, use the current behavior
                    row_value = str(getattr(obj, field))

                row.append(row_value)
            worksheet.append(row)

    workbook.save(response)
    return response

