from django.db import models
from django.conf import settings


class UploadedFile(models.Model):
    STATUS_CHOICES = (
        ('new', 'New'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    )

    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(default="No Description Available.")
    user = models.CharField(max_length=255, default="No User Data Available")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title