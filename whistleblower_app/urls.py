from django.urls import path, include

from . import views
from .views import file_upload_view

urlpatterns = [
    path("", views.index, name="index"),
    path('accounts/', include('allauth.urls')),
    path('upload/', file_upload_view, name='upload'),
    path("logout/", views.logout_view, name="logout"),
    path("upload/logout/", views.logout_view, name="logout"),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('profile/', include('users.urls'), name = "users"),
    path('login/', include('auth_app.urls'), name = "auth"),

]
