from .views import LoginAPI
from django.urls import path

urlpatterns = [
   path('auth/login', LoginAPI.as_view(), name='login'),
]