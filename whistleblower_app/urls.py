from django.urls import path, include

from . import views
from .views import file_upload_view

urlpatterns = [
    path("", views.index, name="index"),
    path('accounts/', include('allauth.urls')),
    path('upload/', file_upload_view, name='upload'),

]
