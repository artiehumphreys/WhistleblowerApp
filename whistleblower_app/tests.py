from .models import UploadedFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from django.test import TestCase,Client
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch



class UploadedFileTestCase(TestCase):
    def test_file_creation(self):
        file = SimpleUploadedFile("test_file.txt", b"file_content")
        uploaded_file = (UploadedFile.objects.create
        (
            title="test file",
            file=file,
            description="This is a test description.",
            user="Test User"
        ))
        self.assertIsNotNone(uploaded_file)
        self.assertEqual(uploaded_file.title, "test file")
        self.assertEqual(uploaded_file.description, "This is a test description.")
        self.assertEqual(uploaded_file.user, "Test User")
        self.assertLessEqual((timezone.now() - uploaded_file.uploaded_at).total_seconds(), 1)

    def test_default_values(self):
        uploaded_file = (UploadedFile.objects.create
        (
            title="Test File",
            file=SimpleUploadedFile("test_file.txt", b"file_content")
        ))
        self.assertEqual(uploaded_file.description, "No Description Available.")
        self.assertEqual(uploaded_file.user, "No User Data Available")



