from django.urls import path
from . import views

urlpatterns = [
    path("", views.login, name = "login"),
    path('social/signup/', views.login, name='signup_redirect'),
    path("logout", views.logout_view)
]