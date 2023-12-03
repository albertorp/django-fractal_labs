from django.utils.translation import gettext_lazy as _

from .models import Requirement, Quotation, Job


class ButtonClass():
    primary = "text-white bg-primary-700 hover:bg-primary-800 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800"
    primary_outline = "text-primary-700 inline-flex items-center hover:text-white border border-primary-700 hover:bg-primary-800 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:border-primary-500 dark:text-primary-500 dark:hover:text-white dark:hover:bg-primary-700 dark:focus:ring-primary-900"
    danger = "text-danger-600 inline-flex items-center hover:text-white border border-danger-600 hover:bg-danger-600 focus:ring-4 focus:outline-none focus:ring-danger-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:border-danger-500 dark:text-danger-500 dark:hover:text-white dark:hover:bg-danger-600 dark:focus:ring-danger-900"


class Buttons():
    button_save = {
        'type': 'submit',
        'name': 'save',
        'text': _('Save'),
        'class': ButtonClass.primary,
    }
    button_cancel = {
        'type': 'button',
        'name': 'confirm_modal',
        'text': _('Cancel'),
        'class': ButtonClass.danger,
        'modal_target': 'modal-cancel',
        'modal_toggle': 'modal-cancel',
    }
    button_reject = {
        'type': 'button',
        'name': 'confirm_reject',
        'text': _('Reject'),
        'class': ButtonClass.danger,
        'modal_target': 'modal-reject',
        'modal_toggle': 'modal-reject',
    }
    button_send = {
        'type': 'submit',
        'name': 'send',
        'text': _('Send'),
        'class': ButtonClass.primary,
    }

    def make_buttons(button_type, button_name, button_text=None, button_class=None, button_target=None, button_toggle=None):
        """
        This function will return a button as a dictionary with the following keys and values:
        - type: The type of the button (e.g. submit, button)
        - name: The name of the button (e.g. save, confirm_modal)
        - text: The text to display on the button
        - class: The class of the button (e.g. ButtonClass.primary)
        - modal-target: The target of the modal (e.g. modal-cancel)
        - modal_toggle: The toggle of the modal (e.g. modal-cancel)
        """
        button = {
            'type': button_type,
            'name': button_name,
        }
        if button_text:
            button['text'] = button_text
        else:
            button['text'] = _(button_name.capitalize())
        if button_class:
            button['class'] = button_class
        else:
            button['class'] = ButtonClass.primary # we default to a primary button if class is not specified
        if button_target:
            button['modal_target'] = button_target
        if button_toggle:
            button['modal_toggle'] = button_toggle

        return button


def get_buttons_requirement(current_status):
    """
    This function will return a list of buttons that will be enabled in the template for RequirementUpdateView,
    depending on the current status of the Requirement
    """

    # First we define all the potential buttons for Requirements:
    button_save = Buttons.button_save
    button_analyse = Buttons.make_buttons('submit', 'analyse')
    button_quote = Buttons.make_buttons('submit', 'quote')
    button_reject = Buttons.button_reject
    button_return = Buttons.make_buttons('button', 'return', button_class=ButtonClass.danger, button_target='modal-return', button_toggle='modal-return')
    
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
    button_save = Buttons.button_save

    button_send = Buttons.button_send
    button_approved = Buttons.make_buttons('button', 'approved', button_target='modal-approval', button_toggle='modal-approval')
    button_rejected = Buttons.button_reject
    button_negotiate = Buttons.make_buttons('button', 'negotiate', button_class=ButtonClass.primary_outline, button_target='modal-negotiate', button_toggle='modal-negotiate')
    button_cancel = Buttons.button_cancel

    # Then we filter the buttons depending on the current status of the Requirement
    buttons = [button_save,
               button_send,
               button_approved,
               button_negotiate,
               button_rejected,
               button_cancel
               ]
    
    if current_status == Quotation.Status.DRAFT:
        buttons = [button_save, button_send, button_cancel]
    if current_status == Quotation.Status.SENT:
        buttons = [button_approved, button_negotiate, button_rejected, button_cancel]
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
    button_save = Buttons.button_save

    button_assign = Buttons.make_buttons('submit', 'assign')
    button_start = Buttons.make_buttons('submit', 'start')
    button_review = Buttons.make_buttons('submit', 'review')
    button_deliver = Buttons.make_buttons('submit', 'deliver')
    button_return = Buttons.make_buttons('button', 'return', button_class=ButtonClass.danger, button_target='modal-return', button_toggle='modal-return')
    button_close = Buttons.make_buttons('submit', 'close', button_class=ButtonClass.primary, button_target='modal-close', button_toggle='modal-close')
    button_cancel = Buttons.button_cancel

    # Then we filter the buttons depending on the current status of the Requirement
    
    can_cancel = True  # In some cases, we will not want to have the Cancel button appear
    buttons = [button_save]
    if current_status == Job.Status.DRAFT:
        buttons = buttons + [button_assign]
    
    if current_status == Job.Status.NOT_STARTED:
        buttons = [button_start]

    if current_status in [Job.Status.IN_PROGRESS, Job.Status.REWORK]:
        buttons = buttons + [button_review]
        can_cancel = False
    
    if current_status == Job.Status.IN_REVIEW:
        buttons = buttons + [button_deliver, button_return]

    if current_status == Job.Status.DELIVERED:
        buttons = buttons + [button_return, button_close]

    if current_status in [Job.Status.CLOSED, Job.Status.CANCELLED]:
        buttons = []
        can_cancel = False

    if can_cancel:
        buttons = buttons + [button_cancel]


    return buttons



def get_buttons_invoice(current_status):
    """
    This function will return a list of buttons that will be enabled in the template for InvoiceUpdateView,
    depending on the current status of the Quotation
    """

    # First we define all the potential buttons for Invoices:
    button_save = Buttons.button_save

    button_send = Buttons.button_send

   
    button_cancel = {
        'type': 'submit',
        'name': 'cancel',
        'text': _('Cancel'),
        'class': ButtonClass.danger,
    }

    # Then we filter the buttons depending on the current status of the Requirement
    buttons = [button_save,
               button_send,
               button_cancel
               ]
    
    # if current_status == Quotation.Status.DRAFT:
    #     buttons = [button_save, button_send, button_cancel]
    # if current_status == Quotation.Status.SENT:
    #     buttons = [button_approved, button_rejected, button_negotiate,  button_cancel]
    # if current_status in [Quotation.Status.APPROVED, Quotation.Status.CANCELLED, Quotation.Status.REJECTED]:
    #     buttons = []
    # if current_status == Quotation.Status.NEGOTIATE:
    #     buttons = [button_save, button_approved, button_rejected, button_cancel]

    return buttons





def get_buttons_webrequirement():
    """
    This function will return a list of buttons that will be enabled in the template for WebRequirementCreateView,
    """

    # First we define all the potential buttons for Requirements:
    button_save = {
        'type': 'submit',
        'name': 'save',
        'text': _('Send'),
        'class': ButtonClass.primary,
    }
    button_reset = {
        'type': 'reset',
        'name': 'reset',
        'text': _('Clear'),
        'class': ButtonClass.danger,
    }
    
    buttons = [button_save, button_reset]
    

    return buttons

