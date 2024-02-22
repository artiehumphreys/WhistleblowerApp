from django.urls import path
from . import views

urlpatterns = [
    path("profile", views.profile, name = "login"),
    path('social/signup/', views.profile, name='signup_redirect'),
    path("logout", views.logout_view)
]