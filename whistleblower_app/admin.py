from django.contrib import admin
from .models import UploadedFile

class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'description', 'status', 'note')

admin.site.register(UploadedFile, UploadedFileAdmin)
