from django.contrib import admin

from .models import Employee

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'manager')
    list_filter = ('user', 'manager')
    #search_fields = ('user')
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Employee, EmployeeAdmin)