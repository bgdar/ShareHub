# from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required

from django.http import HttpRequest

import os
from enum import Enum
from .models import fileManagement

# Upload File


class JenisFIle(Enum):
    CODE = "code"
    IMAGE = "image"
    DOCUMENT = "document"
    ARSIP = "arsip"
    EXECUTABLE = "executable"


@login_required(login_url="accounts:accounts_login")
@csrf_exempt
def upload_file(request: HttpRequest):
    if request.method == "POST":
        file_obj = request.FILES.get("file")  # ambil file dari request
        description = request.POST.get("description", "")
        fileName = request.POST.get(
            "fileName", file_obj.name if file_obj else "unknown"
        )
        jenis_file = request.POST.get("jenis_file")
        print("jenis file ", jenis_file)

        user = request.user

        if file_obj:
            path = default_storage.save(
                f"uploads/{file_obj.name}", ContentFile(file_obj.read())
            )
            file_size = file_obj.size

            # simpan metadata ke database
            file_entry = fileManagement.objects.create(
                fileName=fileName,
                description=description,
                file_size=file_size,
                user=user,
                # atau sesuaikan field lain
                code_file=file_obj if jenis_file == JenisFIle.CODE else None,
                document_file=(file_obj if jenis_file == JenisFIle.DOCUMENT else None),
                executable_file=(
                    file_obj if jenis_file == JenisFIle.EXECUTABLE else None
                ),
                image_file=file_obj if jenis_file == JenisFIle.IMAGE else None,
            )
            messages.info(request=request, message="file uploade")
            return redirect("page_file_upload")
            # return JsonResponse({"message": "File uploaded", "data": model_to_dict(file_entry)})
        else:
            messages.warning(request=request, message="No file uploaded")
            return redirect("page_file_upload")

    return JsonResponse({"error": "Invalid request"}, status=405)


# List semua file
@login_required(login_url="accounts:accounts_login")
def list_files(request: HttpRequest):
    files = fileManagement.objects.all().values()
    print("file : ", files)
    return JsonResponse(list(files), safe=False)


@login_required(login_url="accounts:accounts_login")
# Download file by ID
def download_file(request, file_id):
    try:
        file_entry = fileManagement.objects.get(id=file_id)

        if file_entry.code_file:
            file_path = file_entry.code_file.path
            file_name = file_entry.code_file.name.split("/")[-1]

            with open(file_path, "rb") as f:
                response = HttpResponse(
                    f.read(), content_type="application/octet-stream"
                )
                response["Content-Disposition"] = f"attachment; filename={
                    file_name}"
                return response
        else:
            return JsonResponse({"error": "File not found"}, status=404)
    except fileManagement.DoesNotExist:
        return JsonResponse({"error": "Invalid file ID"}, status=404)


@login_required(login_url="accounts:accounts_login")
def delete_file(request, pk):
    if request.method == "DELETE":
        file_instance = get_object_or_404(fileManagement, pk=pk)

        # Hapus file fisik di storage jika ada
        file_fields = [
            file_instance.code_file,
            file_instance.document_file,
            file_instance.arsip_file,
            file_instance.executable_file,
            file_instance.image_file,
        ]

        for file_field in file_fields:
            if file_field and os.path.isfile(file_field.path):
                os.remove(file_field.path)

        # Hapus data di database
        file_instance.delete()

        return JsonResponse({"message": "File deleted successfully."}, status=200)

    return JsonResponse({"error": "Invalid request method."}, status=405)
