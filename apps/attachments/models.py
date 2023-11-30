from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from apps.utils.models import BaseModel



def user_folder_item_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/FILES/<username>/<item_type>/<filename>
    return 'FILES/{0}/{1}/{2}'.format(instance.owner.username, instance.type, filename)


class FileAttachment(BaseModel):
    """
    The FileAttachment class represents the actual file uploaded to the system. This file always "belongs"
    to a customer, represented here by a user. In order to be able to upload and manipulate files, the customer 
    must have a valid user in the system

    I am calling it FileAttachment because just "file" is a bit confusing
    """

    class FileTypes(models.TextChoices):
        REQ = 'REQ', _('Requirement')
        QUOT = 'QUOT', _('Quotation')
        JOB = 'JOB', _('Job')
        INV = 'INV', _('Invoice')
        OTH = 'OTH', _('Other')

    title = models.CharField(_('title'), max_length=200, null=True, blank=True, help_text=_('Provide a title for the file. If you leave it blank, we will use the filename'))
    description = models.TextField(_('description'), null=True, blank=True, help_text=_('Provide a description of the file'))
    file = models.FileField(_('file'), upload_to=user_folder_item_path)
    type = models.CharField(_('type'), choices=FileTypes.choices, max_length=4, default=FileTypes.OTH)
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('owner'), related_name='files')
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, verbose_name=_('submitted by'), related_name='files_uploaded')

    def __str__(self):
        return self.file.name

    class Meta:
        ordering = ['-created_at']


class Attachment(BaseModel):
    """
    The Attachment class is the one that links a specific file with a specific object
    """
    attachment = models.ForeignKey(FileAttachment, on_delete=models.CASCADE, verbose_name=_('attachment')) 
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    # def __str__(self):
    #     return self.text[:50]

    # class Meta:
    #     ordering = ['-created_at']