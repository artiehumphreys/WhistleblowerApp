from django.urls import path
from . import views

urlpatterns = [
    path("profile", views.profile, name ="login"),
    path("logout", views.logout_view),
    path("",views.test)
]