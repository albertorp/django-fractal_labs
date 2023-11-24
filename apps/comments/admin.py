from django.contrib import admin

# Register your models here.

from .models import Comment
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'text', 'user', 'content_type')
    list_filter = ('user', 'content_type')
    search_fields = ('text', 'user', )
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Comment, CommentAdmin)


class CommentInline(admin.TabularInline):
    model = Comment
    extra=0