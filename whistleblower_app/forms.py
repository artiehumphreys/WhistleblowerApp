from django import forms
from .models import UploadedFile

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ('title', 'file', 'description')
        widgets = {

            'file': forms.ClearableFileInput(attrs={'allow_multiple_selected': True})

        }
