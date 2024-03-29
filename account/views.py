import json
import bcrypt
from rest_framework import generics, status
from django.http import HttpResponse

from .utils import fetchUser, generate_token, cookieOptions

# LOGIN API


class LoginAPI(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):

        try:

          username = request.data["username"]
          password = request.data["password"]

          user = fetchUser(username)
          
          if not user:
            raise Exception("Incorrect username and password")

          check = bcrypt.checkpw(password.encode('utf8'), user.password.encode('utf8'))
           
          if not check:
            raise Exception("Incorrect username and password")

          token = generate_token(str(user._id))
         
          return HttpResponse(json.dumps({
              "status": "success",
              "message": "loggedIn",
          }), content_type="application/json", status=200).set_cookie(**cookieOptions(token))

        except Exception as e:

            return HttpResponse(json.dumps({
                "status": "fail",
                "message": str(e)
            }), content_type="application/json", status=400)
