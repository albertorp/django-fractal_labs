from django.contrib import admin

from .models import Requirement, Quotation, Job

class RequirementAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'title', 'status', 'deadline', 'owner')
    list_filter = ('customer', 'status', 'owner')
    search_fields = ('title', 'description', )

admin.site.register(Requirement, RequirementAdmin)


class QuotationAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'title', 'status', 'deadline', 'owner')
    list_filter = ('customer', 'status', 'owner')
    search_fields = ('title', 'description', )

admin.site.register(Quotation, QuotationAdmin)


class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'title', 'status', 'deadline', 'owner')
    list_filter = ('customer', 'status', 'owner')
    search_fields = ('title', 'description', )

admin.site.register(Job, JobAdmin)