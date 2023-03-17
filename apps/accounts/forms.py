from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import User

# -----ADMIN USER CREATION AND AUTHENTICATION------------#
class CustomAdminUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ["email", "full_name"]
        error_class = "error"


class CustomAdminUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ["email", "full_name"]
        error_class = "error"
