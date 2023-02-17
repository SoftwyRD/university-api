"""Admin for project."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core import models


class UserAdmin(BaseUserAdmin):
    """Fields to be displayed in the admin panel."""

    ordering = ["id"]
    list_display = ["username", "email"]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "first_name",
                    "middle_name",
                    "last_name",
                    "username",
                    "email",
                    "password",
                ),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
        (
            "Important Dates",
            {
                "fields": ("last_login",),
            },
        ),
    )
    readonly_fields = [
        "last_login",
    ]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "middle_name",
                    "last_name",
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Subject)
admin.site.register(models.Weekday)
admin.site.register(models.SubjectSection)
admin.site.register(models.SectionSchedule)
admin.site.register(models.Selection)
