from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import boto3
from django.conf import settings

def profile(request):
    if request.user.groups.filter(name="Site Admin").exists():
        s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        response = s3.list_objects_v2(Bucket='b29-whistleblower')
        files = []
        if 'Contents' in response:
            files = [{'name': item['Key']} for item in response['Contents']]
        return render(request, "siteadmin.html", {'files': files})
    else:
        return render(request, "profile.html")

def logout_view(request):
    logout(request)
    return redirect("/whistleblower/")

def test(request):
    return redirect("/whistleblower/")