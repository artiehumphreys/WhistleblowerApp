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
    username = request.user.username if request.user.is_authenticated else "Anonymous"

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            submission = Submission(user=username)
            submission.save()

            files = request.FILES.getlist('file[]')
            if not files:
                content = 'No File Attached'
                default_file = ContentFile(content.encode(), name='default.txt')
                files = [default_file]

            s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

            for file in files:
                uploaded_file = UploadedFile(
                    submission=submission,
                    file=file,
                    user=username,
                    title=form.cleaned_data['title'],
                    description=form.cleaned_data['description'],
                    tag=form.cleaned_data['tag'],
                    status='new'
                )
                uploaded_file.save()

                extra_args = {
                    'Metadata': {
                        'title': uploaded_file.title,
                        'username': username,
                        'description': uploaded_file.description,
                        'status': 'new',
                        'note': '',
                        'submission_id': str(submission.id),
                        'tag': uploaded_file.tag
                    }
                }
                file_name = f"{submission.id}_{file.name}"
                s3.upload_fileobj(file.file, 'b29-whistleblower', file_name, ExtraArgs=extra_args)

        if username == 'Anonymous':
            return redirect('index')

        return redirect("/profile/")


def list_files(request):
    files = UploadedFile.objects.all()
    return render(request, "users/templates/siteadmin.html", {'files': files})

def logout_view(request):
    logout(request)
    return redirect("/whistleblower/")