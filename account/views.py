from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password

from .models import User
from .utils import set_cookie, verify_token, generate_token, redirect_to_main

main_site = 'http://127.0.0.1:3000'

# register page
def register(request):
    return render(request, 'account/register.html')

# login page
def login(request):
    # check token is valid redirect user to main application
    if verify_token(request.COOKIES.get('token')):
        return redirect(main_site)

    return render(request, 'account/login.html')

# register user
def registerUser(request):

    name = request.POST['name']
    email = request.POST['email']
    contact = request.POST['contact']
    password = request.POST['password']
    
    try:
      user = User(name=name,email=email,contact=contact)
      if password:
         user.password = make_password(password)
      user.full_clean()
      id = user.save()._id
      redirect_to_main(id, redirect)
    except Exception as e:
      print(e.args)
      return render(request, 'account/register.html', {"messages": e})

# log user
def logUser(request):
    # validate post data
    email = request.POST['email']
    password = request.POST['password']
   
    user = User.objects.get(email=email)
    print(user.password)
    is_correct = check_password(password, user.password)
    print(is_correct)

    if not user and is_correct:
      return render(request, 'account/login.html', {"messages": "Incorrect email or password"})
      
     

