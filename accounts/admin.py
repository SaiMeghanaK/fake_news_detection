from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    ordering = ["email"]
    list_display = [
        "email",
        "role",
        "is_staff",
        "is_superuser",
        "is_active",
    ]
    search_fields = [
        "email"
    ]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                )
            }
        ),
        (
            "Personal Information",
            {
                "fields": (
                    "phone",
                    "profile_image",
                )
            }
        ),
        (
            "Role",
            {
                "fields": (
                    "role",
                )
            }
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            }
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),

                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "role",
                ),
            },
        ),
    )