from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.login_view, name='login_page'),
    path('create/', views.create_new_view, name='create_new'),
    path('user/', views.login_logic, name='login_logic'),
    path('register/', views.register_view, name='register'),
]