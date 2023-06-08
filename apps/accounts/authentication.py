from django.conf import settings
from rest_framework.authentication import BaseAuthentication

from datetime import datetime, timedelta

from .models import User, Jwt

import jwt
import random
import string


class Authentication(BaseAuthentication):
    def get_user(self, user_id):
        try:
            user = User.objects.get(id=user_id)
            return user
        except Exception:
            return None

    @staticmethod
    def verify_token(token):
        # decode the token
        try:
            decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except Exception:
            return None

        # check if token as exipired
        exp = decoded_data["exp"]

        if datetime.now().timestamp() > exp:
            return None

        return decoded_data

    @staticmethod
    def get_random(length):
        return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))

    @staticmethod
    def get_access_token(payload):
        return jwt.encode(
            {
                "exp": datetime.utcnow()
                + timedelta(seconds=int(settings.ACCESS_TOKEN_EXPIRE_SECONDS)),
                **payload,
            },
            settings.SECRET_KEY,
            algorithm="HS256",
        )

    @staticmethod
    def get_refresh_token():
        return jwt.encode(
            {
                "exp": datetime.utcnow()
                + timedelta(seconds=int(settings.REFRESH_TOKEN_EXPIRE_SECONDS)),
                "data": Authentication.get_random(10),
            },
            settings.SECRET_KEY,
            algorithm="HS256",
        )

    @staticmethod
    def decodeJWT(bearer):
        if not bearer:
            return None

        token = bearer[7:]

        try:
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except Exception as e:
            print(e)
            return None

        if decoded:
            try:
                user = User.objects.get(id=decoded["user_id"])
                jwt_obj = Jwt.objects.filter(user=user)
                if not jwt_obj.exists():
                    return None
                return user
            except Exception:
                return None
