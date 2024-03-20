from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from whistleblower_app.models import UploadedFile

def profile(request):
    if(request.user.is_authenticated == False):
        return redirect("/whistleblower/")
    if request.user.groups.filter(name="Site Admin").exists():
        files = UploadedFile.objects.all()
        return render(request, "siteadmin.html", {'files': files})
    else:
        return render(request, "profile.html", {'user': request.user})

def logout_view(request):
    logout(request)
    return redirect("/whistleblower/")

def test(request):
    return redirect("/whistleblower/")