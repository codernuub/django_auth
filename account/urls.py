from .views import RegisterAPI, TestAPI
from django.urls import path

urlpatterns = [
   path('register', RegisterAPI.as_view(), name='register'),
]