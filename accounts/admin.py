from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ('username', 'email', 'is_active', 'is_troll', 'date_joined',)
    list_filter = ('is_active', 'is_troll',)

    ordering = ('-date_joined',)


UserAdmin.fieldsets += (('Extra info', {'fields': ('is_troll',)}),)

admin.site.register(CustomUser, CustomUserAdmin)
