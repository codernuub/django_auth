from django.shortcuts import render, redirect
from django.http import HttpResponse
import jwt, datetime

whislist = {
    'user':'http://127.0.0.1:3000',
    'admin':'http://127.0.0.1:4000'
}


def verify_token(token):
  if token:
   try:
    payload = jwt.decode(token,'learning_django', algorithms=["HS256"])
    return { "userType":payload['userType']}
   except jwt.ExpiredSignatureError: 
    return { "userType":None, "message":"your login expired please login again" }
  
  else:
    return {"userType":None, "message":"Please login"}


def generate_token(userId, userType):
  token = jwt.encode({
      "userId":userId,
      "userType":userType,
      "exp":datetime.datetime.utcnow() + datetime.timedelta(seconds=120),
      }, 'learning_django', algorithm="HS256")
  return token


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


def login(request):
    context = verify_token(request.COOKIES.get('token'))

    if context["userType"]:
        type1 = context["userType"]
        print(type1)
        return redirect(whislist[type1])

    if request.method == 'POST':
       id = request.POST['id']
       response = redirect(whislist['user'])
       token = generate_token(id, 'user')  
       return set_cookie(response, token)
     
    if request.method == 'GET':
       return render(request,'account/login.html', context)


def register(request):
    return render(request,'account/register.html')