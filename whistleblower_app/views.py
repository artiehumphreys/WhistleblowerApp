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
    username = request.user.username if request.user.is_authenticated else "anonymous"
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES, username)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.user = username
            file_obj = request.FILES['file']
            s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
            extra_args = {
                'Metadata': {
                    'username': username,
                    'description': uploaded_file.description,
                    'status': 'new',
                    'note': ''
                }
            }
            uploaded_file.save()
            s3.upload_fileobj(file_obj, 'b29-whistleblower', file_obj.name, ExtraArgs=extra_args)
            
    else:
        form = UploadFileForm()
    return render(request, "whistleblower_app/file_upload.html", {'form': form})