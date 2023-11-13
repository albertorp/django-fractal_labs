from django.contrib import admin

from .models import Customer

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('email', 'user', 'tax_id_number', 'billing_address')
    list_filter = ('email', 'user')
    search_fields = ('email', 'user', 'tax_id_number')

admin.site.register(Customer, CustomerAdmin)

