from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .validators import validate_full_name, validate_email


class RegisterSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=300, validators=[validate_full_name])
    email = serializers.EmailField(validators=[validate_email])
    password = serializers.CharField(validators=[validate_password])


class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class RefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class ResendEmailVerificationOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
