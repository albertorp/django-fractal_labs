from django.contrib import admin

# Register your models here.

from .models import Attachment, FileAttachment

class FileAttachmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'title', 'type', 'owner', 'submitted_by')
    list_filter = ('owner', 'submitted_by', 'type')
    # search_fields = ('text', 'user', )
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(FileAttachment, FileAttachmentAdmin)


class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'attachment', 'content_type')
    # list_filter = ('user', 'content_type')
    # search_fields = ('text', 'user', )
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Attachment, AttachmentAdmin)


