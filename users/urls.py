from django.urls import path
from . import views

urlpatterns = [
    path('profile/ajax/change_status/', views.change_file_status, name='change_file_status'),
    path('profile/ajax/change_note/', views.change_file_note, name='change_file_note'),
    path("profile/", views.profile, name ="login"),
    path("logout", views.logout_view),
    path("",views.test),
]