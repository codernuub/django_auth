from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password

from .models import User
from .utils import set_cookie, verify_token, generate_token, redirect_to_main



# register page
def register(request):
    return render(request, 'account/register.html')

# login page
def login(request):
    # check token is valid redirect user to main application
    if verify_token(request.COOKIES.get('token')):
        return redirect("127.0.0.1:3000")

    return render(request, 'account/login.html')

# register user
def registerUser(request):

    name = request.POST['name']
    email = request.POST['email']
    contact = request.POST['contact']
    password = request.POST['password']

    try:
        user = User(name=name, email=email, contact=contact)
        if password:
            user.password = make_password(password)
        user.full_clean()
        user.save()
        return redirect_to_main(user._id, redirect)
    except Exception as e:
        return render(request, 'account/register.html', {"messages": e})

# log user


def logUser(request):
    # validate post data
    email = request.POST['email']
    password = request.POST['password']
     
    if email and password:
      try:
        user = User.objects.get(email=email)
        is_correct = check_password(password, user.password)
        
        if not user and is_correct:
          return render(request, 'account/login.html', {"message": "Incorrect email or password"})
        else:
          return redirect_to_main(str(user._id), redirect)

      except User.DoesNotExist:
          return render(request, 'account/login.html', {"message": "Incorrect email or password"})

    else:
      return render(request, 'account/login.html', {"message": "Please fill all fields"})
