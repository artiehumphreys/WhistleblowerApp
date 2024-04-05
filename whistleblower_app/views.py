from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .forms import UploadFileForm
from .models import UploadedFile
import boto3
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


def index(request):
    return render(request, "whistleblower_app/index.html", {'form': UploadFileForm})

def file_upload_view(request):
    username = request.user.username if request.user.is_authenticated else "anonymous"
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES, username)
        if form.is_valid():
            s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
            for file in request.FILES.getlist('file'):
                uploaded_file = form.save(commit=False)
                uploaded_file.file = file
                uploaded_file.user = username
                file_obj = request.FILES['file']
                uploaded_file.save()
                extra_args = {
                    'Metadata': {
                        'title': uploaded_file.title,
                        'username': username,
                        'description': uploaded_file.description,
                        'status': 'new',
                        'note': ''
                    }
                }
                s3.upload_fileobj(file_obj, 'b29-whistleblower', file.name, ExtraArgs=extra_args)
            
    else:
        form = UploadFileForm()
    return render(request, "whistleblower_app/file_upload.html", {'form': form})