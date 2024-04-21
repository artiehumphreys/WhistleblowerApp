from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


def login_view(request):
    return render(request, 'auth_app/login.html')

@require_http_methods(["GET", "POST"])
def login_logic(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('login')
        else:
            return render(request, 'auth_app/login.html', {'user_error': 'The email and password you entered did not match our records. Please double-check and try again.'})
    else:
        return render(request, 'auth_app/login.html')
    
@require_http_methods(["GET", "POST"])
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        try:
            validate_email(email)
        except ValidationError:
            return render(request, 'auth_app/newaccount.html', {'email_error': 'Please enter a valid email address.'})
        if User.objects.filter(username=username).exists():
            return render(request, 'auth_app/newaccount.html', {'user_error': 'Username is either already taken or invalid. Please consider entering a new username'})
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return redirect('login_page')
    else:
        form = UserCreationForm()
        return render(request, 'auth_app/newaccount.html', {'form': form})
def create_new_view(request):
    return render(request, 'auth_app/newaccount.html')

# Create your views here.
