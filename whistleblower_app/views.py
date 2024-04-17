from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.files.base import ContentFile
from django.template import loader
from .forms import UploadFileForm
from .models import UploadedFile, Submission
import boto3
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import logout
from users import templates
import tempfile
import os



def index(request):
    if(request.user.is_authenticated):
        return redirect("/profile/")
    return render(request, "whistleblower_app/index.html", {'form': UploadFileForm})

def file_upload_view(request):
    username = request.user.username if request.user.is_authenticated else "anonymous"
    if request.method == 'POST':
        if not request.FILES:
            content = 'No File Attached'
            default_file = ContentFile(content.encode(), name='default.txt')
            request.FILES['file'] = default_file
        form = UploadFileForm(request.POST, request.FILES, username)
        if form.is_valid():
            submission = Submission(user=username)
            submission.save()
            s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
            for file in form.cleaned_data['file']:
                uploaded_file = form.save(commit=False)
                uploaded_file.submission = submission
                uploaded_file.file = file
                uploaded_file.user = username
                uploaded_file.save()
                extra_args = {
                    'Metadata': {
                        'title': uploaded_file.title,
                        'username': username,
                        'description': uploaded_file.description,
                        'status': 'new',
                        'note': '',
                        'submission_id': str(uploaded_file.submission.id)
                    }
                }
                s3.upload_fileobj(file, 'b29-whistleblower', file.name, ExtraArgs=extra_args)
    else:
        form = UploadFileForm()
    return render(request, "whistleblower_app/file_upload.html", {'form': form})


def list_files(request):
    files = UploadedFile.objects.all()
    return render(request, "users/templates/siteadmin.html", {'files': files})

def logout_view(request):
    logout(request)
    return redirect("/whistleblower/")