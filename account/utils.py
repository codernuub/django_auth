import jwt
import datetime
from decouple import config

secret = config('TOKEN_SECRET')

def generate_token(userId):
    payload = {
        "userId": userId,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=120),
    }
    token = jwt.encode(payload, secret, algorithm="HS256")
    return token

#set cookie for token
def set_cookie(response, token):
    response.set_cookie(
        key="token",
        value=token,
        max_age=120,
        httponly=True,
        secure=False,
        domain="127.0.0.1"
    )
    return response

def catchError(e):
  print(e.__name);