from django.shortcuts import render
from django.conf import settings
from django.http import HttpRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.core.serializers import serialize

from .models import HubComment, Hub, HubMessage
import os
import json


@login_required(login_url="accounts:accounts_login")
def hub(request: HttpRequest):
    """Menampilkan halaman utama Hub menggabungkan Hub (File) dan HubMessage (Chat Biasa)"""
    current_user = request.user

    hubs_queryset = Hub.objects.select_related("user").all()
    messages_queryset = HubMessage.objects.select_related("user").all()

    combined_list = []

    # Process postingan Hub (Berisi File)
    for h in hubs_queryset:
        comments_queryset = HubComment.objects.filter(
            hub=h).select_related("user").order_by("created_at")

        comments_list = []
        for c in comments_queryset:
            comments_list.append({
                "pk": c.pk,
                "fields": {
                    "comment": c.comment,
                    "created_at": c.created_at.isoformat() if c.created_at else None,
                    "user_username": c.user.username if c.user else "Anonymous"
                }
            })

        combined_list.append({
            "pk": f"hub_{h.pk}",  # Tambahkan prefix ID agar tidak bentrok
            "type": "file",
            "fields": {
                "message": h.message,
                "file_path": h.file_path,
                "created_at": h.created_at.isoformat() if h.created_at else None,
                "created_at_dt": h.created_at,  # Digunakan untuk sorting python
                "user_username": h.user.username if h.user else "Anonymous"
            },
            "comments": comments_list
        })

    # Process postingan HubMessage (Chat Biasa)
    for m in messages_queryset:
        combined_list.append({
            "pk": f"msg_{m.pk}",
            "type": "chat",
            "fields": {
                "message": m.message,
                "file_path": None,  # Tidak ada file
                "created_at": m.created_at.isoformat() if m.created_at else None,
                "created_at_dt": m.created_at,  # Digunakan untuk sorting python
                "user_username": m.user.username if m.user else "Anonymous"
            },
            # HubMessage tidak punya relasi komentar (atau bisa diisi array kosong)
            "comments": []
        })

    # Urutkan gabungan postingan berdasarkan tanggal terbaru (descending)
    combined_list.sort(
        key=lambda x: x["fields"]["created_at_dt"], reverse=True)

    # Hapus helper datetime Python agar bisa di-serialize ke JSON
    for item in combined_list:
        del item["fields"]["created_at_dt"]

    data_hub_json = json.dumps(combined_list)

    return render(
        request,
        "hub/hub.html",
        context={
            "user": current_user,
            "data_hub": data_hub_json
        }
    )


@login_required
def api_add_hud_file(request: HttpRequest):
    if request.method == "POST":
        message = request.POST.get("message")
        upload_source = request.POST.get("upload_source")
        file_path = request.POST.get(
            "path_file") if upload_source == "file" else None

        # Buat dan simpan data ke database Hub
        hub_post = Hub.objects.create(
            user=request.user,
            message=message,
            file_path=file_path
        )

        # Jika request dikirim via AJAX / Alpine.js fetch
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({
                "status": "success",
                "message": "Data berhasil disimpan!",
                "data": {
                    "id": hub_post.id,
                    "message": hub_post.message,
                    "file_path": hub_post.file_path,
                }
            })

        # Jika dikirim via Form submit biasa
        # Ganti dengan name url halaman hub Anda
        return redirect("hub")

    return JsonResponse({"error": "Method not allowed"}, status=405)


@login_required
def api_add_message(request: HttpRequest):
    """Endpoint API khusus untuk menyimpan pesan teks (HubMessage) tanpa file"""
    if request.method == "POST":
        if request.content_type == "application/json":
            try:
                data = json.loads(request.body)
                message_text = data.get("message", "").strip()
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON"}, status=400)
        else:
            # Mendukung standard Form submit
            message_text = request.POST.get("message", "").strip()

        if not message_text:
            return JsonResponse({"error": "Pesan tidak boleh kosong"}, status=400)

        new_msg = HubMessage.objects.create(
            user=request.user,
            message=message_text
        )

        # Jika request berupa Fetch/AJAX, kembalikan JSON
        if request.content_type == "application/json":
            return JsonResponse({
                "pk": new_msg.pk,
                "fields": {
                    "message": new_msg.message,
                    "created_at": new_msg.created_at.isoformat(),
                    "user_username": request.user.username
                }
            })

        return redirect("hub")

    return JsonResponse({"error": "Method tidak diizinkan"}, status=405)


@login_required
def api_add_comment(request, hub_id):
    """Endpoint API untuk menyimpan komentar"""
    if request.method == "POST":
        try:
            # Jika user mencoba mengomentari pesan biasa (HubMessage)
            if isinstance(hub_id, str) and hub_id.startswith("msg_"):
                return JsonResponse({"error": "Pesan biasa tidak dapat dikomentari"}, status=400)

            # Jika postingan berkas (Hub)
            if isinstance(hub_id, str) and hub_id.startswith("hub_"):
                real_id = hub_id.replace("hub_", "")
            else:
                real_id = hub_id

            data = json.loads(request.body)
            comment_text = data.get("comment", "").strip()

            if not comment_text:
                return JsonResponse({"error": "Komentar tidak boleh kosong"}, status=400)

            hub_obj = get_object_or_404(Hub, pk=real_id)

            new_comment = HubComment.objects.create(
                hub=hub_obj,
                user=request.user,
                comment=comment_text
            )

            return JsonResponse({
                "pk": new_comment.pk,
                "fields": {
                    "comment": new_comment.comment,
                    "created_at": new_comment.created_at.isoformat(),
                    "user_username": request.user.username if request.user else "Anonymous"
                }
            })
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except (ValueError, Hub.DoesNotExist):
            return JsonResponse({"error": "ID Hub tidak valid"}, status=400)

    return JsonResponse({"error": "Method tidak diizinkan"}, status=405)


@login_required
def api_hub_list(request):
    """Menyediakan daftar file dalam bentuk JSON untuk Alpine.js"""

    # Tentukan folder tempat Anda menyimpan file yang bisa dipilih user.
    # Contoh di bawah menggunakan folder 'uploads' di dalam direktori STATIC_ROOT / STATICFILES_DIRS
    # Anda juga bisa menggantinya ke settings.MEDIA_ROOT jika menggunakan file media.
    target_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')

    file_list = []

    # Pastikan folder tujuan ada agar tidak memicu error
    if os.path.exists(target_dir):
        # Ambil semua file di dalam folder tersebut
        for index, file_name in enumerate(os.listdir(target_dir), start=1):
            file_path = os.path.join(target_dir, file_name)

            if os.path.isfile(file_path):
                # Ukuran dalam satuan Bytes
                file_size = os.path.getsize(file_path)

                file_list.append({
                    "id": index,
                    # Path relatif untuk disimpan ke database
                    "fileName": f"uploads/{file_name}",
                    "file_size": file_size
                })

    # safe=False digunakan karena kita mengirim data berbentuk List/Array JSON, bukan Dictionary
    return JsonResponse(file_list, safe=False)


@login_required
def detail_file_view(request, id: int):

    print("id detail file", id)
    # Ambil data Hub berdasarkan ID (atau 404 jika tidak ditemukan)
    hub_item = get_object_or_404(Hub.objects.select_related('user'), id=id)

    print("hasil hub item : ", hub_item)

    file_content = None
    file_extension = None

    # Jika ada path_file, coba baca kontennya (opsional: untuk file teks/code)
    if hub_item.file_path:
        file_extension = os.path.splitext(hub_item.file_path)[-1].lower()
        text_extensions = ['.txt', '.py', '.js',
                           '.html', '.css', '.json', '.md', '.csv']
        if file_extension in text_extensions:
            full_path = os.path.join(
                settings.MEDIA_ROOT, str(hub_item.file_path))
            if os.path.exists(full_path):
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        file_content = f.read()
                except Exception as e:
                    file_content = f"Gagal membaca isi file: {str(e)}"

    context = {
        'hub': hub_item,
        'file_content': file_content,
        'file_extension': file_extension,
    }
    return render(request, 'hub/detail-file.html', context)

# @login_required(login_url="accounts:accounts_login")
# def upload(request: HttpRequest):
#     if request.method == "GET":
#         return render(request, "hub/upload.html")


# -----API --------
@login_required(login_url="accounts:accounts_login")
def hub_message(request: HttpRequest):
    """upload , update message dari hub.html"""
    user = request.user
    if request.method == "POST":
        # update message
        message = request.POST.get("message")
        path_file = request.POST.get("mess")
        # dapatkan dari api yang di kirim kembali yang di kirm
        path_file = request.POST.get("file_path")
        Hub.objects.create(
            message=message,
            file_path=path_file,
            user=user,
        )
        messages.info(request, message="Message Updated")
        return redirect("hub")


def page_not_found(request: HttpRequest):
    render(request=request, template_name="404.html")
