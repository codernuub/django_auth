from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password

from .models import User
from .utils import set_cookie, verify_token, generate_token, redirect_to_main

from decouple import config

main_site = config('MAIN_SITE') # redirect user to this origin

# register page
def register(request):
    return render(request, 'account/register.html')

# login page
def login(request):
    # check token is valid redirect user to main application
    if verify_token(request.COOKIES.get('token')):
        return redirect(origin)

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
        u = user.save()
        return redirect_to_main(str(user._id), redirect)
    except Exception as e:
        return render(request, 'account/register.html', {"messages": e})


# log user
def logUser(request):
    # validate post data
    email = request.POST['email']
    password = request.POST['password']

    try:

        if not email and password:
            raise Exception("Please fill all fields")

        user = User.objects.get(email=email)
        correct = check_password(password, user.password)

        if not correct:
            raise Exception("Incorrect password")

        return redirect_to_main(str(user._id), redirect)

    except Exception as e:

        if type(e).__name__ == "DoesNotExist":
            e = "User not found"
        return render(request, 'account/login.html', {"message": e})
