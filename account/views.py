import json
from django.contrib.auth.hashers import make_password, check_password

from rest_framework import generics, status
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse

from .utils import generate_token, set_cookie, catchError

from .models import User

#REGISTER API
class RegisterAPI(generics.GenericAPIView):
  
    def post(self, request, *args, **kwargs):
        try:
          request.data['password'] = make_password(request.data['password']); 
          user = User(
                name=request.data['name'], 
                email=request.data['email'],
                contact=request.data['contact'],
                password=request.data['password']
          )
          user.full_clean()
          user.save()
          
          token = generate_token(str(user._id))
          responseData = {
              "status":'success',
              "message":"logged In",
              "data":None
          }
          response = HttpResponse(json.dumps(responseData), content_type="application/json")
          return set_cookie(response, token)

        except Exception as e:
          
          responseData = {
              "status":"fail",
              "message":dict(e)
          }
          return JsonResponse(responseData, status=status.HTTP_400_BAD_REQUEST)

#LOGIN API
class LoginAPI(generics.GenericAPIView):
 
   def post(self, request, *args, **kwargs):
        responseData = {}
        try:
          username=request.data['data']
          password=request.data['password']

          if not username and password:
            raise Exception("Please fill all fields")

          user = User.objects.get(contact=username)
          
          check_password(request.data['password'], user.password)

          token = generate_token(str(user._id))

          responseData["status"] = "success"
          responseData["message"] = "logged In",

          response = HttpResponse(json.dumps(responseData), content_type="application/json")
          return set_cookie(response, token)
        except Exception as e:

          responseData["status"] = "fail"

          if type(e).__name__ == 'DoesNotExist':
            responseData['message'] = "please provide valid credentials"
          else :
            responseData['message'] = str(e)
          return JsonResponse(responseData, status=status.HTTP_400_BAD_REQUEST)