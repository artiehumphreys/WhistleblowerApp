from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .forms import UploadFileForm
from .models import UploadedFile


def index(request):
    return render(request, "whistleblower_app/index.html")

def file_upload_view(request):
    print('hi')
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.save()
            return render(request, "whistleblower_app/file_upload.html", {'form': form})
    else:
        form = UploadFileForm()
    return render(request, "whistleblower_app/file_upload.html", {'form': form})

def list_files(request):
    files = UploadedFile.objects.all()
    return render(request, "users/templates/siteadmin.html", {'files': files})