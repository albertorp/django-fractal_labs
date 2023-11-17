from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext_lazy as _



from apps.comments.models import Comment

# Create your models here.
from apps.utils.models import BaseModel

from apps.customers.models import Customer

class Currencies(models.TextChoices):
    AED = 'AED', _('UAE Dirham')
    USD = 'USD', _('US Dollar')
    EUR = 'EUR', _('Euro')
    GBP = 'GBP', _('UK Pound')

class BaseItem(BaseModel):
    """
    
    
    """
    # class ReadWrite(models.IntegerChoices):
    #     READ_ONLY = 0, _('Read Only') # Item is Read only. No changes allowed
    #     WRITE_ALL = 1, _('Write All') # Item can be modified by customers and staff
    #     WRITE_STAFF = 2, _('Write Staff') # Item can only be modified by staff, not by customer

    title = models.CharField(_('title'), max_length=200, help_text=_('Provide a title to identify this item'))
    description = models.TextField(_('description'), null=True, blank=True, help_text=_('Describe in detail the item'))
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=_('customer'), help_text=_('the item belongs to this customer'))
    deadline = models.DateField(_('deadline'), blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_sent = models.DateTimeField(blank=True, null=True)
    date_closed = models.DateTimeField(blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('owner'), help_text=_('user currently working on or responsible for this item'))
    comments = GenericRelation(Comment)
 
    # With the "Comments" model, this field should not be needed
    # closure_comments = models.TextField(_('closure comments'), null=True, blank=True, help_text=_('Details of how the item is to be closed, whether approved, rejected or closed'))
    # rw = models.SmallIntegerField(_('read_write'), choices=ReadWrite.choices, default=ReadWrite.WRITE_ALL)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    # def get_rw_display(self):
    #     return self.ReadWrite(self.rw).label




class Requirement(BaseItem):
    """
    REQUIREMENTS are enquiries or requests for proposals received from customers or potential customers. 
    They are based on BaseItem and add a status field with the following values:

    RECEIVED: The customer has created the REQUIREMENT and sent it. The Service Provider (SP) receives it. All REQUIREMENTS start in this status.
    ANALYSIS: An employee will look at the list of requirements and select one to start working on it. The status will change to ANALYSIS. The customer can no longer make changes. (Future: allow the customer to make changes. These should be flagged to the employee to make a note that the requirement has changed).
    TO_QUOTE: The employee deems the REQUIREMENT viable and sends it for quotation. A QUOTATION object is created with the information from the REQUIREMENT and linked back to it.
    REJECTED: The SP cannot do the work so the REQUIREMENT is rejected and the customer is informed.
    RETURNED: There is missing information, so the REQUIREMENT is sent back to the customer for clarification. The REQUIREMENT will stay in this state until more information is received, and then it will go back to RECEIVED, or if too much time has elapsed, it will automatically move to REJECTED.

    """
    class Status(models.IntegerChoices):
        RECEIVED = 0, _('Received')
        ANALYSIS = 1, _('Analysis')
        TO_QUOTE = 2, _('To Quote')
        REJECTED = -1, _('Rejected')
        RETURNED = -2, _('Returned')
    
    status = models.SmallIntegerField(_('status'), choices=Status.choices, default=Status.RECEIVED)
    deadline = models.DateField(_('deadline'), blank=True, null=True, help_text=_('Delivery date requested. This is only informational and there is no commitment until the Quotation is sent and approved'))

    class Meta:
        verbose_name = _('Requirement')
        verbose_name_plural = _('Requirements')

    def get_status_display(self):
        return self.Status(self.status).label
    


class Quotation(BaseItem):
    """
    QUOTATIONS are proposals for work received from customers or potential customers. 
    They are based on BaseItem and add a status field with the following values:

    DRAFT: The SP has created the QUOTATION from a REQUIREMENT and is now working on it.
    SENT: The QUOTATION is ready and once it’s sent to the customer, it goes to SENT state.
    APPROVED: The customer has approved the QUOTATION and a JOB can be created
	REJECTED: The customer has rejected the QUOTATION.
  	NEGOTIATE: The customer has replied and there is an ongoing dialogue about the QUOTATION. The QUOTATION in this state can be modified and updated.
    CANCELLED: The customer has not replied for too long and the QUOTATION is no longer valid

    """
   
    class Status(models.IntegerChoices):
        DRAFT = 0, _('Draft')
        SENT = 1, _('Sent')
        APPROVED = 2, _('Approved')
        REJECTED = -1, _('Rejected')
        NEGOTIATE = 3, _('Negotiate')
        CANCELLED = -2, _('Cancelled')

    
        
    
    status = models.SmallIntegerField(_('status'), choices=Status.choices, default=Status.DRAFT)
    # TODO replace the price from DecimalField to the MoneyField (integration from Pypi)
    price = models.DecimalField(_('Price proposed'), max_digits=10, decimal_places=2, blank=True, null=True)
    # TODO replace the currency to allow for multicurrency setups
    currency = models.CharField(_('Currency'), choices=Currencies.choices, max_length=3, blank=True, null=True, default='AED')
    # TODO The terms will later be a relationship with a Term model
    terms =  models.TextField(_('Terms'), null=True, blank=True, help_text=_('Terms and Conditions for this Quotation'))
    # We want to keep traceability from requirement to quoations. One requirement could be converted in
    # multiple quotation, so we will have a reference  in the Quotation to the originating Requirement
    requirement = models.ForeignKey(Requirement, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Requirement'))

    # validity: date until the QUOTATION is valid
    validity = models.DateField(_('Validity'),   blank=True, null=True, help_text=_('date until this quotation is valid'))


    class Meta:
        verbose_name = _('Quotation')
        verbose_name_plural = _('Quotations')

    def get_status_display(self):
        return self.Status(self.status).label
    



class Job(BaseItem):
    """
    JOBS are any piece of work that we do based on accepted quotations received from customers or potential customers. 
    They are based on BaseItem and add a status field with the following values:

    DRAFT: Initial state when the QUOTATION is accepted and the JOB is created. No work is done in this stage. No owner is assigned yet. The responsible from the SP verifies that the details are correct and plans the work (time and resources). An owner can then be assigned. Action: “Assign”
    NOT STARTED: The owner assigned previously will see the JOB in her list of JOBS. She can look at it and once she starts working on it, it goes to IN_PROGRESS. Action: “Start”
    IN_PROGRESS: The work is done by the owner and is ready to be reviewed. The owner must be changed to the reviewer. Action: “Done”
    IN_REVIEW: The work is reviewed by the owner (the new one) and is ready to be delivered. The work is sent to the customer and the JOB goes to DELIVERED status.
    DELIVERED: The work has been sent to the customer. Actions: Close, Rework
    REWORK: The work has been returned from the customer for rework
    CLOSED: The JOB has been finished and fully paid and no further work needs to be done.
    CANCELLED: For some reason the job has to be cancelled. This should also be explained in the comments

    """
    
    class Status(models.IntegerChoices):
        DRAFT = 0, _('Draft')
        NOT_STARTED = 1, _('Not Started')
        IN_PROGRESS = 2, _('In Progress')
        IN_REVIEW = 3, _('In Review')
        DELIVERED = 4, _('Delivered')
        REWORK = 5, _('Rework')
        CLOSED = -1, _('Closed')
        CANCELLED = -2, _('Cancelled')

    class Invoiced(models.IntegerChoices):
        NONE = 0, _('Not invoiced')
        PARTIAL = 1, _('Partially Invoiced')
        FULL = 2, _('Fully Invoiced')

    class Paid(models.IntegerChoices):
        NONE = 0, _('Not paid')
        PARTIAL = 1, _('Partially paid')
        FULL = 2, _('Fully paid')

    
    status = models.SmallIntegerField(_('status'), choices=Status.choices, default=Status.DRAFT)
    invoiced = models.SmallIntegerField(_('invoiced'), choices=Invoiced.choices, default=Invoiced.NONE)
    paid = models.SmallIntegerField(_('paid'), choices=Paid.choices, default=Paid.NONE)

    # TODO replace the price from DecimalField to the MoneyFiled (integration from Pypi)
    price = models.DecimalField(_('Price accepted'), max_digits=10, decimal_places=2, blank=True, null=True)
    # TODO replace the currency to allow for multicurrency setups
    currency = models.CharField(_('Currency'), choices=Currencies.choices, max_length=3, blank=True, null=True, default='AED')
    # TODO The terms will later be a relationship with a Term model
    terms =  models.TextField(_('Terms'), null=True, blank=True, help_text=_('Terms and Conditions for this Job'))
    # TODO We want to keep traceability from requirement to quoations and jobs. One quotation could be converted in
    # multiple jobs, so we will have a reference  in the Job to the originating quotation
    quotation = models.ForeignKey(Quotation, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Quotation'))


    class Meta:
        verbose_name = _('Job')
        verbose_name_plural = _('Jobs')

    def get_status_display(self):
        return self.Status(self.status).label

    def get_invoiced_display(self):
        return self.Invoiced(self.invoiced).label

    def get_paid_display(self):
        return self.Paid(self.paid).label


# All codes should have 5 or less characters
class TaxCodes(models.TextChoices):
    VAT = 'VAT', _('VAT')



class Invoice(BaseItem):
    """
    An invoice is sent to a customer in order to get the payment for a job (or several jobs). 
    Each job to be invoiced will be a separate invoice item

    DRAFT: The SP is preparing the INVOICE
    SENT: The INVOICE is ready and once it’s sent to the customer, it goes to SENT state.
    PARTIAL: The customer has approved the QUOTATION and a JOB can be created
    PAID: The customer has paid all invoice items in this INVOICE.
    OVERDUE: The invoice is overdue and needs to be paid.
    CANCELLED: The invoice has been cancelled (need to provide explanations)

    """
   
    class Status(models.IntegerChoices):
        DRAFT = 0, _('Draft')
        SENT = 1, _('Sent')
        PARTIAL = 2, _('Partial')
        PAID = 3, _('Paid')
        OVERDUE = 4, _('Overdue')
        CANCELLED = -2, _('Cancelled')

    
    status = models.SmallIntegerField(_('status'), choices=Status.choices, default=Status.DRAFT)
    price = models.DecimalField(_('Total Price'), max_digits=10, decimal_places=2, blank=True, null=True)
    # TODO replace the currency to allow for multicurrency setups
    currency = models.CharField(_('Currency'), choices=Currencies.choices, max_length=3, blank=True, null=True, default='AED')
    #stripe_id = 
    tax_code = models.CharField(_('Tax Code'), choices=TaxCodes.choices, max_length=5, blank=True, null=True)
    tax_pct = models.DecimalField(_('Tax %'), max_digits=6, decimal_places=2, blank=True, null=True, help_text='Tax Percentage to be added to the price')
    job = models.ForeignKey(Job, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Job'), help_text=_('If set, this job will be used for all the line items for this invoice'))

    class Meta:
        verbose_name = _('Invoice')
        verbose_name_plural = _('Invoices')

    def get_status_display(self):
        return self.Status(self.status).label
    
    def get_tax_code_display(self):
        return TaxCodes(self.tax_code).label
    


class InvoiceItem(models.Model):
    """
    An invoice item is the precise amount to be invoiced for each job. It will have the following fields:
    Invoice (FK). Parent invoice for this item
    Title
    Description
    Quantity, default 1
    Price (per unit)
    Tax code
    Tax pct
    Job (FK)
    Paid (Boolean, default FALSE)
    """
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, verbose_name=_('Invoice'), related_name='lineitems')
    title = models.CharField(_('title'), max_length=200, help_text=_('Provide a title to identify this line item'))
    description = models.TextField(_('description'), null=True, blank=True, help_text=_('If needed, provide additional detail for this line item'))
    quantity = models.DecimalField(_('quantity'), max_digits=6, decimal_places=2, default=1.00, help_text=_('Quantity of this line item'))
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2)
    tax_code = models.CharField(_('Tax Code'), choices=TaxCodes.choices, max_length=5, blank=True, null=True)
    tax_pct = models.DecimalField(_('Tax %'), max_digits=6, decimal_places=2, default=0.00, help_text='Tax Percentage to be added to the price')
    job = models.ForeignKey(Job, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Job'), help_text=_('If set, this job will be used for all the line items for this invoice'))
    paid = models.BooleanField(_('paid'), default=False)

    class Meta:
        verbose_name = _('Invoice Item')
        verbose_name_plural = _('Invoice Items')
    
    def get_tax_code_display(self):
        return TaxCodes(self.tax_code).label