from django.test import TestCase

# Create your tests here.
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import fileManagement


class FileManagementAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Dummy file untuk upload
        self.test_file = SimpleUploadedFile(
            "test.txt", b"ini file testing", content_type="text/plain"
        )

    def test_upload_file(self):
        response = self.client.post(
            "/api/upload/",
            {
                "fileName": "File Uji",
                "description": "Ini file untuk unit test",
                "code_file": self.test_file,
            },
            format="multipart",
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.data)

    def test_list_files(self):
        # Buat data dummy dulu
        file_obj = fileManagement.objects.create(
            fileName="Dummy",
            description="File dummy",
            file_size=123,
        )

        response = self.client.get("/api/files/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) >= 1)
        self.assertEqual(response.data[0]["fileName"], file_obj.fileName)

    def test_get_file_detail(self):
        file_obj = fileManagement.objects.create(
            fileName="Detail File",
            description="Untuk detail test",
            file_size=50,
        )

        response = self.client.get(f"/api/files/{file_obj.pk}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["fileName"], "Detail File")

    def test_delete_file(self):
        file_obj = fileManagement.objects.create(
            fileName="File Delete",
            description="Untuk hapus test",
            file_size=75,
        )

        response = self.client.delete(f"/api/files/{file_obj.pk}/delete/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"],
                         "File deleted successfully.")
        self.assertFalse(fileManagement.objects.filter(
            pk=file_obj.pk).exists())
