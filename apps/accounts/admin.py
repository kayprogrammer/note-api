from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group as DjangoGroup
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.utils.translation import gettext_lazy as _

from .forms import CustomAdminUserChangeForm, CustomAdminUserCreationForm
from .models import User


class Group(DjangoGroup):
    class Meta:
        verbose_name = "group"
        verbose_name_plural = "groups"
        proxy = True


class GroupAdmin(BaseGroupAdmin):
    pass


class UserAdmin(BaseUserAdmin):
    ordering = ["full_name"]
    add_form = CustomAdminUserCreationForm
    form = CustomAdminUserChangeForm
    model = User

    list_display = [
        "pkid",
        "id",
        "email",
        "full_name",
        "is_staff",
        "is_active",
    ]

    list_display_links = ["id", "email"]
    list_filter = [
        "email",
        "full_name",
        "is_staff",
        "is_active",
    ]
    fieldsets = (
        (
            _("Login Credentials"),
            {"fields": ("email", "password")},
        ),
        (
            _("Personal Information"),
            {"fields": ("full_name", "avatar")},
        ),
        (
            _("Permissions and Groups"),
            {
                "fields": (
                    "is_email_verified",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            _("Important Dates"),
            {"fields": ("date_joined", "last_login")},
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "full_name",
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

    search_fields = ["email", "full_name"]

    def render_change_form(
        self, request, context, obj, add=False, change=False, form_url=""
    ):
        if not "/add/" in request.path:
            # Allow only super users and article owner to update article
            if request.user != obj and request.user.is_superuser != True:
                context.update(
                    {
                        "show_save": False,
                        "show_save_and_continue": False,
                        "show_delete": False,
                        "show_save_and_add_another": False,
                    }
                )
        return super().render_change_form(request, context, add, change, form_url, obj)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            self.readonly_fields = [
                "groups",
                "user_permissions",
                "is_staff",
                "is_superuser",
                "is_active",
            ]
        return self.readonly_fields


admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.unregister(DjangoGroup)
