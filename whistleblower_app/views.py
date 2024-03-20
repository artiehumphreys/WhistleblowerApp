from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .forms import UploadFileForm
from .models import UploadedFile
import boto3
from django.conf import settings



def index(request):
    return render(request, "whistleblower_app/index.html", {'form': UploadFileForm})

def file_upload_view(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.save()
            return render(request, "whistleblower_app/file_upload.html", {'form': form})
    else:
        form = UploadFileForm()
    return render(request, "whistleblower_app/file_upload.html", {'form': form})

def list_files(request):
    s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    response = s3.list_objects_v2(Bucket='b29-whistleblower')

    files = []
    if 'Contents' in response:
        files = [{'name': item['Key']} for item in response['Contents']]

    return render(request, "users/templates/siteadmin.html", {'files': files})