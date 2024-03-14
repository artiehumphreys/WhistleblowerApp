from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .forms import UploadFileForm


def index(request):
    return render(request, "whistleblower_app/index.html")


def file_upload_view(request):
    from django.shortcuts import redirect
    from .forms import UploadFileForm

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success_url')  # Redirect to a new URL
    else:
        form = UploadFileForm()
    return render(request, 'your_template.html', {'form': form})