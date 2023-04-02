from django.conf import settings

from datetime import datetime, timedelta

from .models import User, Jwt

import jwt
import random
import string


def get_random(length):
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))


def get_access_token(payload):
    return jwt.encode(
        {"exp": datetime.now() + timedelta(minutes=5), **payload},
        settings.SECRET_KEY,
        algorithm="HS256",
    )


def get_refresh_token():
    return jwt.encode(
        {"exp": datetime.now() + timedelta(hours=24), "data": get_random(10)},
        settings.SECRET_KEY,
        algorithm="HS256",
    )


def decodeJWT(bearer):
    if not bearer:
        return None

    token = bearer[7:]

    try:
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
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
