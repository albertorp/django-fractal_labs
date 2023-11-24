from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from apps.utils.models import BaseModel


class Comment(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, verbose_name=_('user'))
    text = models.TextField(_('text'))
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __str__(self):
        return self.text[:50]

    class Meta:
        ordering = ['-created_at']