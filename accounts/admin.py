from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser


UserAdmin.list_display += ('is_troll',)
UserAdmin.list_filter += ('is_troll',)
UserAdmin.fieldsets += (('Extra info', {'fields': ('is_troll',)}),)

admin.site.register(CustomUser, CustomUserAdmin)
