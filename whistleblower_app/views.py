from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .forms import UploadFileForm


def index(request):
    return render(request, "whistleblower_app/index.html")

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