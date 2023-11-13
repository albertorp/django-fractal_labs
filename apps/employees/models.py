from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.utils.models import BaseModel


class Employee(BaseModel):
    """
    An employee is everyone that...

    Fields:

    """


    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    manager = models.BooleanField(default=False, help_text=_('Is the employee a manager?'))

    def __str__(self):
        return self.name