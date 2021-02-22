import jwt
import datetime
from decouple import config

secret = config('TOKEN_SECRET')
main_site = config('MAIN_SITE')

# verify token: if not exist, expired or invalid , render login page
def verify_token(token):
    if not token:
      return False
    try:
      jwt.decode(token, secret, algorithms=["HS256"])
      return True
    except:
      return False

# generate new token

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

def redirect_to_main(id, redirect):
  response = redirect(main_site)
  token = generate_token(id)
  return set_cookie(response, token)