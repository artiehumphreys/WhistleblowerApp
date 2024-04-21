from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.http import require_http_methods

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
            return render(request, 'users/profile.html')
        else:
            return HttpResponse("Invalid username or password.", status=401)
    else:
        return render(request, 'auth_app/login.html')
    
@require_http_methods(["GET", "POST"])
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already taken.", status=400)
        
        user = User.objects.create_user(username=username, password=password)
        user.save()
        return redirect('login_page')
    else:
        return render(request, 'auth_app/newaccount.html')  
def create_new_view(request):
    return render(request, 'auth_app/newaccount.html')

# Create your views here.
