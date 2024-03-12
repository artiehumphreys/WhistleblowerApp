from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def profile(request):
    if request.user.groups.filter(name="Site Admin").exists():
        return render(request, "siteadmin.html")
    else:
        return render(request, "profile.html")

def logout_view(request):
    logout(request)
    return redirect("/whistleblower/")

def test(request):
    return redirect("/whistleblower/")