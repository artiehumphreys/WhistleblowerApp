from django.db import models
from django.conf import settings
import uuid


def generate_unique_id():
    id = uuid.uuid4()
    return str(id).replace('-', '')

class Submission(models.Model):
    id = models.UUIDField(primary_key=True, default=generate_unique_id, editable=False)
    user = models.CharField(max_length=255)
    submitted_at = models.DateTimeField(auto_now_add=True)


class UploadedFile(models.Model):
    STATUS_CHOICES = (
        ('new', 'New'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    )
    TAG_CHOICES = (
        ('physical', 'Physical Bullying'),
        ('verbal', 'Verbal Abuse'),
        ('cyber', 'Cyberbullying'),
        ('racism', 'Racist Bullying'),
        ('sexual', 'Inappropriate Sexual Comments'),
        ('social', 'Social Bullying'),
        ('emotional', 'Emotional Intimidation'),
        ('other', 'Other'),
    )
    submission = models.ForeignKey(Submission, related_name='files', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(default="")
    user = models.CharField(max_length=255, default="No User Data Available")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    note = models.TextField(blank=True, null=True)
    tag = models.CharField(max_length=30, choices=TAG_CHOICES)

    def __str__(self):
        return self.title