from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed
from apps.accounts.authentication import Authentication


class IsAuthenticatedCustom(BasePermission):
    def has_permission(self, request, view):
        http_auth = request.META.get("HTTP_AUTHORIZATION")
        if not http_auth:
            raise AuthenticationFailed("Auth Bearer not provided!")
        user = Authentication.decodeJWT(http_auth)
        if not user:
            raise AuthenticationFailed("Auth token invalid or expired!")
        request.user = user
        if request.user and request.user.is_authenticated:
            return True
        return False
