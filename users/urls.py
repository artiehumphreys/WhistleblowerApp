from django.urls import path, include
from . import views

urlpatterns = [
    path('ajax/change_status/', views.change_file_status, name='change_file_status'),
    path("", views.profile, name ="login"),
    path('login/', views.login_view, name='login_page'),
    path('create/', views.create_new_view, name='create_new'),
    path('user/', views.login_logic, name='login_logic'),
    path('register/', views.register_view, name='register'),
    path("logout/", views.logout_view, name="logout"),
    path('delete_submission/<submission_id>', views.delete_submission, name='delete_submission'),
    path('accounts/', include('allauth.urls')),

    # path("logout/", views.logout_view, name="logout"),
    # path("",views.redirect)
]