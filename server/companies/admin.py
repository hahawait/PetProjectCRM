from django.contrib import admin
from companies.models import Company, Contact, Job


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'created_at', 'updated_at')
    search_fields = ['id', 'name', 'address', 'created_at', 'updated_at']


class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'name', 'position', 'email')
    search_fields = ['id', 'company', 'name', 'position', 'email']


class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'title', 'is_open', 'created_at', 'updated_at')
    search_fields = ['id', 'company', 'title', 'is_open', 'created_at', 'updated_at']

admin.site.register(Company, CompanyAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Job, JobAdmin)