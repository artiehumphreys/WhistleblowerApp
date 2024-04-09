from django.urls import path
from . import views

urlpatterns = [
    path('ajax/change_status/', views.change_file_status, name='change_file_status'),
    path("", views.profile, name ="login"),
    path("logout/", views.logout_view, name="logout"),
    # path("logout/", views.logout_view, name="logout"),
    # path("",views.redirect)
]