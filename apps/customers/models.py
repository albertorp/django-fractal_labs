from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
from apps.utils.models import BaseModel


class Customer(BaseModel):
    """
    A customer is everyone that has engaged with us, whether initially for information or requests
    or later on with projects and payments.

    To keep it simple, each customer is defined by their email address, which they should not change directly

    All other fields will be optional and the business logic will update them as and when needed

    email: email adress used by the customer or potential customer to identify in our site
    user: the user associated with this customer, if it exists. If the user is deleted, the customer will be set to null, in case we want to associate this customer with another user
    tax_id_number: tax identification number of the customer
    billing_address: billing address of the customer. TEMP: this will be replaced by a more robust address implementation. Needed for legal purposes for the invoices
    stripe_customer_id: stripe customer id of the customer. Link to the id of this customer as used in Stripe
    """
    email = models.EmailField('email', unique=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    tax_id_number = models.CharField(_('Tax Identification Nr'), max_length=20, blank=True, null=True)
    billing_address = models.CharField(_('Billing Address'), max_length=255, blank=True, null=True)
    stripe_customer_id = models.CharField(_('Stripe ID'), max_length=100, blank=True, null=True)

    def __str__(self):
        return self.email

    @property
    def email_username(self):
        return self.email.split('@')[0]