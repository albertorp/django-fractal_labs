from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, UpdateView, CreateView

from .models import FileAttachment, Attachment
from .forms import FileAttachmentForm

from apps.jobcycle.models import Requirement, Quotation, Job, Invoice

# Create your views here.


class FileAttachmentListView(LoginRequiredMixin, ListView):
    model = FileAttachment  
    template_name = 'attachments/fileattachment_list.html' 
    context_object_name = 'fileattachment_list' 
    list_display = ('id', 'title', 'type', 'owner', 'submitted_by', 'created_at')
    title = _('FileAttachments')
    active_tab = 'fileattachments'
    paginate_by = 10

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['active_tab'] = self.active_tab
        context['model_name'] = self.model.__name__
        context['fields'] = self.list_display
        return context
    


class FileAttachmentUpdateView(LoginRequiredMixin, UpdateView):
    model = FileAttachment
    template_name = 'attachments/fileattachment_update.html'
    form_class = FileAttachmentForm
    success_url = reverse_lazy('attachments:fileattachment_list')
    title = _('FileAttachment Update')
    active_tab = 'fileattachments'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = self.title
        ctx['active_tab'] = self.active_tab
        # FileAttachments for the moment do not have the possibility to have comments associated to them
        # ctx['comments'] = self.object.comments.all()
        # ctx['count'] = self.object.comments.count()
        return ctx

    def get_form_kwargs(self):
        """ Used to pass the logged in user to the form in order to enable/disable fields """
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    

    def form_invalid(self, form):
        messages.error(self.request, _('Please check errors and try again'))
        return super().form_invalid(form)
    

    def form_valid(self, form):
        if 'save' in self.request.POST:
            messages.success(self.request, _('FileAttachment saved'))

        if 'cancel' in self.request.POST:
            messages.info(self.request, _('Operation cancelled'))
            return HttpResponseRedirect(self.get_success_url())


        return super().form_valid(form)


class FileAttachmentCreateView(LoginRequiredMixin, CreateView):
    model = FileAttachment 
    template_name = 'attachments/fileattachment_update.html'
    form_class = FileAttachmentForm
    success_url = reverse_lazy('attachments:fileattachment_list')
    title = _('FileAttachment Create')
    active_tab = 'fileattachments'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = self.title
        ctx['active_tab'] = self.active_tab
        ctx['create'] = True
        return ctx

    def get_form_kwargs(self):
        """ Used to pass the logged in user to the form in order to enable/disable fields """
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    
    def form_invalid(self, form):
        messages.error(self.request, _('Please check errors and try again'))
        return super().form_invalid(form)
    
    def form_valid(self, form):

        if 'item' in self.request.GET:
            id_param = self.request.GET['id']
            if self.request.GET['item'] == 'requirement':
                item = get_object_or_404(Requirement, pk=id_param)
                self.success_url = reverse_lazy('jobcycle:requirement_update', kwargs={'pk':id_param})
            elif self.request.GET['item'] == 'quotation':
                item = get_object_or_404(Quotation, pk=id_param)
                self.success_url = reverse_lazy('jobcycle:quotation_update', kwargs={'pk':id_param})
            elif self.request.GET['item'] == 'job':
                item = get_object_or_404(Job, pk=id_param)
                self.success_url = reverse_lazy('jobcycle:job_update', kwargs={'pk':id_param})
            else:
                # TODO error here. Check and raise exception
                pass

            # Ignore the form's owner field and set it to the customer in the item retrieved
            form.instance.owner = item.customer
            
            fileattachment = form.save()
            attachment = Attachment.objects.create(
                attachment = fileattachment,
                flow = form.cleaned_data['flow'],
                content_type=ContentType.objects.get_for_model(item),                
                object_id=item.pk
            )
            

        return super().form_valid(form)