from .views import RegisterAPI, LoginAPI
from django.urls import path

urlpatterns = [
   path('auth/register', RegisterAPI.as_view(), name='register'),
   path('auth/login', LoginAPI.as_view(), name='login'),
]