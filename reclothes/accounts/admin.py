from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        'username',
        'id',
        'email',
        'is_staff',
        'is_superuser',
        'is_active',
        'date_joined',
        'last_login',
    )
    readonly_fields = ('last_login', 'date_joined')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'username', 'id')
