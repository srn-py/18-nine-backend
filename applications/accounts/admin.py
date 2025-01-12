from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from applications.accounts.models import CustomUser


# CustomUser Admin
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = [
        'username', 'email', 'phone_number', 'is_staff', 'is_active',
        'referral_code'
    ]
    search_fields = ['username', 'email', 'phone_number', 'referral_code']
    list_filter = [
        'is_staff', 'is_active', 'send_promo_mail', 'first_order_placed'
    ]
    fieldsets = (
        (None, {'fields': ('username', 'email', 'phone_number', 'password')}),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'referral_code')
        }),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'groups',
                'user_permissions')
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Preferences'), {
            'fields': ('send_promo_mail', 'first_order_placed')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'phone_number', 'password1', 'password2'
            ),
        }),
    )