from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from . import models as accounts_models
from .threads import EmailThread
import random


class Util:
    @staticmethod
    def send_activation_otp(user):
        subject = "Verify your email"
        otp = random.randint(1000, 9999)
        message = render_to_string(
            "activation_email.html",
            {
                "name": user.full_name,
                "otp": otp,
            },
        )

        otp_object, created = accounts_models.Otp.objects.get_or_create(user=user)
        otp_object.code = otp
        otp_object.save()

        email_message = EmailMessage(subject=subject, body=message, to=[user.email])
        email_message.content_subtype = "html"
        EmailThread(email_message).start()

    @staticmethod
    def send_password_change_otp(user):
        subject = "Your account password reset email"
        otp = random.randint(1000, 9999)
        message = render_to_string(
            "password_reset_email.html",
            {
                "name": user.full_name,
                "otp": otp,
            },
        )
        otp_object, created = accounts_models.Otp.objects.get_or_create(user=user)
        otp_object.code = otp
        otp_object.save()
        email_message = EmailMessage(subject=subject, body=message, to=[user.email])
        email_message.content_subtype = "html"

        EmailThread(email_message).start()

    @staticmethod
    def password_reset_confirmation(user):
        subject = "Password Reset Successful!"
        message = render_to_string(
            "password_reset_confirmation_email.html",
            {
                "name": user.full_name,
            },
        )
        email_message = EmailMessage(subject=subject, body=message, to=[user.email])
        email_message.content_subtype = "html"
        EmailThread(email_message).start()

    @staticmethod
    def welcome_email(user):
        subject = "Welcome to Notes App!"
        message = render_to_string(
            "welcome_email.html",
            {
                "user": user,
            },
        )
        email_message = EmailMessage(subject=subject, body=message, to=[user.email])
        email_message.content_subtype = "html"
        EmailThread(email_message).start()
