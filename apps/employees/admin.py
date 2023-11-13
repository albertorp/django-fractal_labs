from django.contrib import admin

from .models import Employee

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'manager')
    list_filter = ('user', 'manager')
    #search_fields = ('user')

admin.site.register(Employee, EmployeeAdmin)