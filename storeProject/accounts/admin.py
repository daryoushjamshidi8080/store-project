from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeFrom
from django.contrib.auth.models import Group


class UserAdmin(BaseUserAdmin):
    form = UserChangeFrom
    add_form = UserCreationForm

    list_display = ('email', 'phone_number', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        ('User Info', {
         'fields': ('email', 'phone_number', 'full_name', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_admin', 'last_login')}),
    )

    add_fieldsets = (
        ('User Info', {'fields': ('phone_number', 'email',
         'full_name', 'password1', 'password2')}),
        ('Permissions', {'fields': ('is_active', 'is_admin')}),
    )

    search_fields = ('email', 'phone_number', 'full_name')
    ordering = ('full_name',)
    filter_horizontal = ()


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
