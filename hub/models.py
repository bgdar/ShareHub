from django.db import models
from django.conf import settings

# Create your models here.


class hubs(models.Model):
    """Data utama untuk hubs yang di tampilkan di hub.html"""

    id = models.AutoField(primary_key=True)
    message = models.CharField(max_length=200)
    # path file yang di upload oleh user
    file_path = models.CharField(max_length=25)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,  # gak hilangkan komentar tapi menghapus arah user
        null=True,
        related_name="hubs",
    )
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class hubsComentar(models.Model):
    """untuk handle dan menyimpan comentar comentar dari user"""

    comentar = models.CharField()
