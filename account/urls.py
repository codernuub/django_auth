from django.urls import path
from . import views

app_name="account"

urlpatterns =(
   #path('', views.login, name="login"),
   path('login', views.logUser, name="userLogin"),
   path('registerUser', views.register, name='register'),
   path('register', views.registerUser, name='userSignup'),
)