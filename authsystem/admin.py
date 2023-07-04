from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    fields = (
        'id', 'email', 'username', 'created', 'is_active', 'is_staff', 'is_superuser', 
    )
    list_editable = (
        'is_active', 'is_staff', 'is_superuser', 
    )
    list_display = (
        'id', 'email', 'username', 'created', 'is_active', 'is_staff', 'is_superuser', 
    )
    search_fields = (
        'id', 'email', 'username', 'created', 'is_active', 'is_staff', 'is_superuser', 
    )
    readonly_fields = (
        'id', 'created',
    )

admin.site.register(User, UserAdmin)