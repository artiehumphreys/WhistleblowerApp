from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages


def profile(request):
    return render(request, "profile.html")

def logout_view(request):
    logout(request)
    return redirect("/whistleblower/")

def signup_redirect(request):
    messages.error(request, "Something wrong here, it may be that you already have account!")
    return redirect("homepage")