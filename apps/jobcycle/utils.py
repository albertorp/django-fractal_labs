from django.utils.translation import gettext_lazy as _

from .models import Requirement, Quotation, Job



def get_buttons_requirement(current_status):
    """
    This function will return a list of buttons that will be enabled in the template for RequirementUpdateView,
    depending on the current status of the Requirement
    """

    # First we define all the potential buttons for Requirements:
    button_save = {
        'type': 'submit',
        'name': 'save',
        'text': _('save'),
        'class': 'btn btn-primary',
    }
    button_analyse = {
        'type': 'submit',
        'name': 'analyse',
        'text': _('analyse'),
        'class': 'btn btn-primary',
    }
    button_quote = {
        'type': 'submit',
        'name': 'quote',
        'text': _('quote'),
        'class': 'btn btn-primary',
    }
    button_reject = {
        'type': 'submit',
        'name': 'reject',
        'text': _('reject'),
        'class': 'btn btn-primary',
    }
    button_return = {
        'type': 'submit',
        'name': 'return',
        'text': _('return'),
        'class': 'btn btn-primary',
    }
    # Then we filter the buttons depending on the current status of the Requirement
    buttons = [button_save, button_analyse, button_quote, button_return, button_reject]
    if current_status == Requirement.Status.RECEIVED:
        buttons = [button_save, button_analyse, button_reject]
    if current_status == Requirement.Status.ANALYSIS:
        buttons = [button_save, button_quote, button_return, button_reject]
    if current_status == Requirement.Status.TO_QUOTE or current_status == Requirement.Status.REJECTED:
        buttons = []
    if current_status == Requirement.Status.RETURNED:
        buttons = [button_save, button_analyse]

    

    return buttons



def get_buttons_quotation(current_status):
    """
    This function will return a list of buttons that will be enabled in the template for QuotationUpdateView,
    depending on the current status of the Quotation
    """

    # First we define all the potential buttons for Quotations:
    button_save = {
        'type': 'submit',
        'name': 'save',
        'text': _('save'),
        'class': 'btn btn-primary',
    }
    button_send = {
        'type': 'submit',
        'name': 'send',
        'text': _('send'),
        'class': 'btn btn-primary',
    }
    button_approved = {
        'type': 'submit',
        'name': 'approved',
        'text': _('approved'),
        'class': 'btn btn-primary',
    }
    button_rejected = {
        'type': 'submit',
        'name': 'rejected',
        'text': _('rejected'),
        'class': 'btn btn-primary',
    }
    button_negotiate = {
        'type': 'submit',
        'name': 'negotiate',
        'text': _('negotiate'),
        'class': 'btn btn-primary',
    }
    button_cancel = {
        'type': 'submit',
        'name': 'cancel',
        'text': _('cancel'),
        'class': 'btn btn-primary',
    }

    # Then we filter the buttons depending on the current status of the Requirement
    buttons = [button_save,
               button_send,
               button_approved,
               button_rejected,
               button_negotiate,
               button_cancel
               ]
    
    if current_status == Quotation.Status.DRAFT:
        buttons = [button_save, button_send, button_cancel]
    if current_status == Quotation.Status.SENT:
        buttons = [button_approved, button_rejected, button_negotiate,  button_cancel]
    if current_status in [Quotation.Status.APPROVED, Quotation.Status.CANCELLED, Quotation.Status.REJECTED]:
        buttons = []
    if current_status == Quotation.Status.NEGOTIATE:
        buttons = [button_save, button_approved, button_rejected, button_cancel]

    return buttons



def get_buttons_job(current_status):
    """
    This function will return a list of buttons that will be enabled in the template for JobUpdateView,
    depending on the current status of the Job
    """

    # First we define all the potential buttons for Jobs:
    button_save = {
        'type': 'submit',
        'name': 'save',
        'text': _('save'),
        'class': 'btn btn-primary',
    }
    button_assign = {
        'type': 'submit',
        'name': 'assign',
        'text': _('assign'),
        'class': 'btn btn-primary',
    }
    button_start = {
        'type': 'submit',
        'name': 'start',
        'text': _('start'),
        'class': 'btn btn-primary',
    }
    button_review = {
        'type': 'submit',
        'name': 'review',
        'text': _('review'),
        'class': 'btn btn-primary',
    }
    button_deliver = {
        'type': 'submit',
        'name': 'deliver',
        'text': _('deliver'),
        'class': 'btn btn-primary',
    }
    button_return = {
        'type': 'submit',
        'name': 'return',
        'text': _('return'),
        'class': 'btn btn-primary',
    }
    button_close = {
        'type': 'submit',
        'name': 'close',
        'text': _('close'),
        'class': 'btn btn-primary',
    }
    button_cancel = {
        'type': 'submit',
        'name': 'cancel',
        'text': _('cancel'),
        'class': 'btn btn-primary',
    }

    # Then we filter the buttons depending on the current status of the Requirement
    
    can_cancel = True  # In some cases, we will not want to have the Cancel button appear
    buttons = [button_save]
    if current_status == Job.Status.DRAFT:
        buttons = buttons + [button_assign]
    
    if current_status == Job.Status.NOT_STARTED:
        buttons = buttons + [button_start]

    if current_status in [Job.Status.IN_PROGRESS, Job.Status.REWORK]:
        buttons = buttons + [button_review]
        can_cancel = False
    
    if current_status == Job.Status.IN_REVIEW:
        buttons = buttons + [button_return, button_deliver]

    if current_status == Job.Status.DELIVERED:
        buttons = buttons + [button_return, button_close]

    if current_status in [Job.Status.CLOSED, Job.Status.CANCELLED]:
        buttons = []
        can_cancel = False

    if can_cancel:
        buttons = buttons + [button_cancel]


    return buttons



def get_buttons_webrequirement():
    """
    This function will return a list of buttons that will be enabled in the template for WebRequirementCreateView,
    """

    # First we define all the potential buttons for Requirements:
    button_save = {
        'type': 'submit',
        'name': 'save',
        'text': _('send'),
        'class': 'btn btn-primary',
    }
    button_reset = {
        'type': 'reset',
        'name': 'reset',
        'text': _('Clear'),
        'class': 'btn btn-primary',
    }
    
    buttons = [button_save, button_reset]
    

    return buttons

