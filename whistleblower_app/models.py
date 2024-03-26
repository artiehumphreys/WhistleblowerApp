from django.db import models
from django.conf import settings


class UploadedFile(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(default = "No Description Available.")
    user = models.CharField(max_length=255, default = "No User Data Available")