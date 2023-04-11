import jwt
import datetime
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from authentication.models import User


# creation a middleware to get user authenticated
class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            id = decode_access_token(token)
            user = User.objects.get(pk=id)
            return (user, None)
        raise exceptions.AuthenticationFailed("Non authentifié")


def create_access_token(id):
    user = User.objects.get(pk=id)
    return jwt.encode({
        "role": user.role,
        "user_id": id,
        # "exp": datetime.datetime.now() + datetime.timedelta(seconds=60),
        "exp": datetime.datetime.now() + datetime.timedelta(days=2),
        "iat": datetime.datetime.utcnow()  # creation time
    }, "access_secret", algorithm='HS256')


def decode_access_token(token):
    try:
        payload = jwt.decode(token, 'access_secret', algorithms='HS256')
        return payload['user_id']
    except:
        raise exceptions.AuthenticationFailed("Non authentifié")


def create_refresh_token(id):
    user = User.objects.get(pk=id)
    return jwt.encode({
        'user_id': id,
        'role': user.role,
        'exp': datetime.datetime.now() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow()  # creation time
    }, 'refresh_secret', algorithm='HS256')


def decode_refresh_token(token):
    try:
        payload = jwt.decode(token, 'refresh_secret', algorithms='HS256')
        return payload['user_id']
    except:
        raise exceptions.AuthenticationFailed("Non authentifié")
