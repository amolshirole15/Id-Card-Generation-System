from django.contrib import admin
from eqrApp import models

# Register your models here.
admin.site.register(models.Employee)

# Register the Profile model
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('organization_name', 'organization_code', 'organization_type', 'contact_email', 'date_joined')
    search_fields = ('organization_name', 'organization_code')

admin.site.register(models.Profile, ProfileAdmin)