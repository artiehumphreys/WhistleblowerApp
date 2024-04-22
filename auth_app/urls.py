from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.login_logic, name='login_page'),
    path('create/', views.register_view, name='create_new'),
]