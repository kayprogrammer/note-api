from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model

User = get_user_model()


def validate_full_name(value):
    words = value.split()
    if not len(words) == 2:
        raise ValidationError(
            _("You must enter exactly two names"), code="invalid_name"
        )
    return value


def validate_email(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError("Email already registered")
