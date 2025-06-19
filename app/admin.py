from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User

class UserAdmin(BaseUserAdmin):
    model = User
    ordering = ['username']
    list_display = ['username', 'role', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_superuser', 'is_active']
    readonly_fields = ['last_login', 'date_joined']  # <-- add this

    fieldsets = (
        (None, {'fields': ('username', 'password', 'role', 'email',)}),
        (_('Permissions'), {
            'fields': ('is_staff', 'is_active', 'is_superuser')
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),  # OK now
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

    search_fields = ['email']


admin.site.register(User, UserAdmin)
