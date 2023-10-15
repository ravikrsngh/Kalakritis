from django.contrib import admin
from django.contrib.auth.models import Group
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken,BlacklistedToken
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.


admin.site.site_header = 'Kalakritis'
admin.site.site_title = 'Kalakritis'
admin.site.index_title = 'Kalakritis Admin'

class UserAddressInline(admin.TabularInline):
    model = UserAddress
    extra = 0

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    fieldsets = (
        ('Authentication Details', {
            'fields': ('email', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name','phone_number','temp_otp')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        })
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    ordering = ["email"]

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(Group)
