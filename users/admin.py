# Import necessary modules.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


# Define the admin class for the CustomUser model.
class CustomUserAdmin(ModelAdmin, UserAdmin):
    # The form used for creating a new user in the admin.
    add_form = CustomUserCreationForm

    # The form used for changing an existing user in the admin.
    form = CustomUserChangeForm

    # The model this admin class is for.
    model = CustomUser

    # The columns to display in the admin list view.
    list_display = [
        "email",
        "first_name",
        "last_name",
        "is_agency",
        "is_staff",
    ]
    
    # Enable search to make autocomplete work
    search_fields = ["email", "first_name", "last_name"]

    # The fields to display when editing a user. Organized into sections (fieldsets).
    # This overrides the default fieldsets which include 'username'.
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal Information"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "bio",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_agency",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    # The fields to display when adding a new user.
    # 'password2' is for the confirmation field.
    add_fieldsets = (
        (None, {
            "fields": ("email", "password1", "password2", "is_agency"),
            "description": "Create a new user or agency account"
        }),
    )

    # The field to use for ordering the list view.
    ordering = ["email"]
    
    # Add filter for agency/non-agency users
    list_filter = ["is_agency", "is_staff", "is_superuser", "is_active"]


# Register your custom model and its admin class with the admin site.
admin.site.register(CustomUser, CustomUserAdmin)
