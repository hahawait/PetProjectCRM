from django.contrib import admin
from accounts.models import UserRole


class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    search_fields = ['user', 'role']


admin.site.register(UserRole, UserRoleAdmin)
