from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.models.user import User


# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('id', 'username', 'is_active')
    search_fields = ('username',)
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Status', {'fields': ('is_active',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_active')},
        ),
    )

admin.site.register(User, CustomUserAdmin)