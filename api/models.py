from django.db import models

# Create your models here.


class fileManagement(models.Model):
    fileName = models.CharField(max_length=15)
    description = models.CharField(max_length=200, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    file_size = models.PositiveIntegerField(blank=True)
    # Simpan ke media/file/..
    code_file = models.FileField(
        upload_to="file/code", blank=True, null=True)
    document_file = models.FileField(
        upload_to="file/documents/", blank=True, null=True)
    arsip_file = models.FileField(
        upload_to="file/arsip", blank=True, null=True)
    executable_file = models.FileField(
        upload_to="file/executable", blank=True, null=True)
    image_file = models.FileField(
        upload_to="file/image", blank=True, null=True)
