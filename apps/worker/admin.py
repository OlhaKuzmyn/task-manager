from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin


@admin.register(get_user_model())
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + (
        "position",
        "is_manager",
        "team",
    )
    fieldsets = UserAdmin.fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "position",
                        "is_manager",
                        "team",
                    )
                },
            ),
        )
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "position",
                        "is_manager",
                        "team",
                    )
                },
            ),
        )
    )
