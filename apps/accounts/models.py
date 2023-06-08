import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from apps.common.models import BaseModel
from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    full_name = models.CharField(verbose_name=(_("Full name")), max_length=300)
    email = models.EmailField(verbose_name=(_("Email address")), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_email_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    avatar = models.ImageField(
        default=None, upload_to="avatars/", null=True, blank=True
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.full_name


class Otp(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    code = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.user.full_name)

    def check_otp_expiration(self):
        now = timezone.now()
        diff = now - self.updated_at
        if diff.total_seconds() > int(settings.EMAIL_OTP_EXPIRE_SECONDS):
            return True
        return False


class Jwt(BaseModel):
    user = models.OneToOneField(
        User, related_name="login_user", on_delete=models.CASCADE
    )
    access = models.TextField()
    refresh = models.TextField()
