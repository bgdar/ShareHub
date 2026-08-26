from django.db import models
from django.conf import settings

# Create your models here.


class FileManagement(models.Model):
    id = models.AutoField(primary_key=True)
    fileName = models.CharField(max_length=15)
    description = models.CharField(max_length=200, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    file_size = models.PositiveIntegerField(blank=True)
    # user_id = models.ForeignKey(
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,  # jika user dihapus, data ikut terhapus
        related_name="fileManagement",
        null=True,
    )
    # Simpan ke media/file/..
    # simpan berdasarkan katagort
    code_file = models.FileField(upload_to="file/code", blank=True, null=True)
    document_file = models.FileField(
        upload_to="file/documents/", blank=True, null=True)
    arsip_file = models.FileField(
        upload_to="file/arsip", blank=True, null=True)
    executable_file = models.FileField(
        upload_to="file/executable", blank=True, null=True
    )
    image_file = models.FileField(
        upload_to="file/image", blank=True, null=True)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
