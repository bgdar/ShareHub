from django.db import models
from django.conf import settings

# Create your models here.


class Hub(models.Model):
    """Data utama untuk hubs
    di sini berisi message dengan file , beda dengan message biasa """

    # Django otomatis membuat id primary key, Anda tidak wajib menulis baris ini.
    # Namun jika ingin eksplisit menggunakan AutoField, ini sudah benar.
    id = models.AutoField(primary_key=True)
    message = models.CharField(max_length=200)

    # Perubahan: CharField max_length=25 terlalu pendek untuk path file.
    # Disarankan ganti ke FileField atau minimal CharField(max_length=255)
    file_path = models.CharField(max_length=255)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,  # Tidak menghapus komentar/postingan saat user dihapus
        null=True,
        blank=True,
        related_name="hubs",
    )
    # Penamaan standar Python menggunakan 'created_at' dan 'updated_at' (ditambah huruf 'd')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Hub"
        verbose_name_plural = "Hubs"


class HubMessage(models.Model):
    """handle untuk Message message yang akan di tampilakn di hub"""
    message = models.TextField()

 # user yang mengetik
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="hub_message"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Hub Message"
        verbose_name_plural = "Hub Message"


class HubComment(models.Model):
    """Untuk handle dan menyimpan komentar-komentar dari user"""

    #  ingin teks panjang tanpa batas, gunakan TextField().
    comment = models.TextField()

    # Tambahan: Menghubungkan komentar ke postingan Hub utama
    hub = models.ForeignKey(
        Hub,
        on_delete=models.CASCADE,  # Jika postingan Hub dihapus, komentarnya ikut terhapus
        related_name="comments"
    )

    #  Menghubungkan komentar ke user yang menulisnya
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="hub_comments"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Hub Comment"
        verbose_name_plural = "Hub Comments"
