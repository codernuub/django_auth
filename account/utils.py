import jwt
import datetime
from decouple import config
from .models import User


secret = config('TOKEN_SECRET')
prod = config('MODE')
domain = config('COOKIE_DOMAIN')


def buildQuery(username):
    query_user = {}
    if '@' in str(username):
       query_user["email"]=username
    else:
       query_user["contact"]=username
    return query_user


def fetchUser(username):
    try:
       query_user = buildQuery(username)
       return User.objects.get(**query_user)
    except Exception as e:
       return None
       

def generate_token(userId):
    payload = {
        "userId": userId,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=120),
    }
    token = jwt.encode(payload, secret, algorithm="HS256")
    return token

#set cookie for token
def cookieOptions(token):
    return {
        "key":"token",
        "value":token,
        "max_age":(60 * 60 * 1000),
        "secure":False,
        "domain":domain
    }
    

def catchError(e):
  print(e.__name);