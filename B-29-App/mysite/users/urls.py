from django.urls import path
from . import views

urlpatterns = [
    path('social/signup/', views.signup_redirect, name='signup_redirect'),
]