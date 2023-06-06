from django.contrib.auth import authenticate
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from .serializers import (
    RegisterSerializer,
    VerifyEmailSerializer,
    SendOtpSerializer,
    SetNewPasswordSerializer,
    LoginSerializer,
    RefreshSerializer,
)
from .models import User, Otp, Jwt
from apps.common.responses import CustomSuccessResponse, CustomErrorResponse
from apps.common.serializers import ResponseSerializer
from .senders import Util
from .authentication import Authentication


class RegisterView(APIView):
    serializer_class = RegisterSerializer

    @extend_schema(
        summary="Register a new user",
        responses=ResponseSerializer,
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(**serializer.validated_data)
        Util.send_activation_otp(user)
        return CustomSuccessResponse({"message": "Registration Successful"}, status=201)


class VerifyEmailView(APIView):
    serializer_class = VerifyEmailSerializer

    @extend_schema(
        summary="Verify user email",
        request=VerifyEmailSerializer,
        responses=ResponseSerializer,
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(email=serializer.validated_data["email"])
        if not user.exists():
            return CustomErrorResponse({"message": "Incorrect email"})
        user = user.get()

        otp = Otp.objects.filter(user=user, code=serializer.validated_data["otp"])
        if not otp.exists():
            return CustomErrorResponse({"message": "Incorrect Otp"})
        otp = otp.get()

        if otp.check_otp_expiration() == True:
            return CustomErrorResponse({"message": "Expired otp"})

        user.is_email_verified = True
        user.save()
        Util.welcome_email(user)
        return CustomSuccessResponse({"message": "Verification Successful"}, status=201)


class LoginView(APIView):
    serializer_class = LoginSerializer

    @extend_schema(
        summary="Login in to the application",
        request=LoginSerializer,
        responses=ResponseSerializer,
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            request,
            username=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )
        if not user:
            return CustomErrorResponse({"message": "Invalid credentials"}, status=404)
        if not user.is_email_verified:
            return CustomErrorResponse({"message": "Email not verified"})

        Jwt.objects.filter(user=user).delete()

        access = Authentication.get_access_token(
            {"user_id": str(user.id), "full_name": user.full_name}
        )
        refresh = Authentication.get_refresh_token()

        Jwt.objects.create(user=user, access=access, refresh=refresh)

        return CustomSuccessResponse(
            {
                "message": "Login successful",
                "data": {"access": access, "refresh": refresh},
            }
        )


class RefreshView(APIView):
    serializer_class = RefreshSerializer

    @extend_schema(
        summary="Generate new authentication tokens",
        request=RefreshSerializer,
        responses=ResponseSerializer,
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh = serializer.validated_data["refresh"]

        jwt = Jwt.objects.filter(refresh=refresh)
        if not jwt.exists():
            return CustomErrorResponse(
                {"message": "Refresh token not found"}, status=401
            )
        jwt = jwt.get()

        token = Authentication.verify_token(refresh)
        if not token:
            return CustomErrorResponse(
                {"message": "Refresh token is invalid or expired"}, status=401
            )

        access = Authentication.get_access_token({"user_id": str(jwt.user.id)})
        refresh = Authentication.get_refresh_token()

        jwt.access = access
        jwt.refresh = refresh
        jwt.save()
        return CustomSuccessResponse(
            {
                "message": "Refresh successful",
                "data": {"access": access, "refresh": refresh},
            }
        )


class ResendEmailVerificationOtpView(APIView):
    serializer_class = SendOtpSerializer

    @extend_schema(
        summary="Resend verification otp",
        request=SendOtpSerializer,
        responses=ResponseSerializer,
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        user = User.objects.filter(email=email)
        if not user.exists():
            return CustomErrorResponse({"message": "Incorrect email!"}, status=404)
        if user[0].is_email_verified == True:
            return CustomSuccessResponse(
                {"message": "Email already verified. Proceed to login!"}
            )
        Util.send_activation_otp(user[0])
        return CustomSuccessResponse({"message": "New otp sent!"})


class SendPasswordResetOtpView(APIView):
    serializer_class = SendOtpSerializer

    @extend_schema(
        summary="Send Password Reset Otp",
        request=SendOtpSerializer,
        responses=ResponseSerializer,
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        user = User.objects.filter(email=email)
        if not user.exists():
            return CustomErrorResponse({"message": "Incorrect email!"}, status=404)
        Util.send_password_change_otp(user[0])
        return CustomSuccessResponse({"message": "Otp sent!"})


class SetNewPasswordView(APIView):
    serializer_class = SetNewPasswordSerializer

    @extend_schema(
        summary="Send Password Reset Otp",
        request=SetNewPasswordSerializer,
        responses=ResponseSerializer,
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        otp = serializer.data["otp"]
        password = serializer.data["password"]

        # Validate user
        user = User.objects.filter(email=email)
        if not user.exists():
            return CustomErrorResponse({"message": "Incorrect email!"}, status=404)
        user = user.get()

        # Validate Otp
        otp = Otp.objects.filter(user=user, code=otp)
        if not otp.exists():
            return CustomErrorResponse({"message": "Incorrect Otp"})
        otp = otp.get()

        if otp.check_otp_expiration() == True:
            return CustomErrorResponse({"message": "Expired otp"})

        # Set password
        user.set_password(password)
        user.save()
        Util.password_reset_confirmation(user)
        return CustomSuccessResponse({"message": "Password reset success!"})
