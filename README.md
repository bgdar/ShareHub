<h1 align="center"> ShareHub  </h1>

<p align="center">

Aplikasi share file , image , dan lainya , layaknya media social

</p>

### Tech Stack

<p align="center">
  <img src="https://skillicons.dev/icons?i=django" width="50" alt="Django" />
  <img src="https://skillicons.dev/icons?i=python" width="50" alt="Python" />
  <img src="https://skillicons.dev/icons?i=javascript" width="50" alt="Alpine.js" />
  <img src="https://skillicons.dev/icons?i=html" width="50" alt="HTML" />
  <img src="https://skillicons.dev/icons?i=tailwindcss" width="50" alt="HTML" />
 
  <img src="https://img.shields.io/badge/uv-FF6F00?logo=python&logoColor=white&style=for-the-badge" height="40" alt="uv" />
</p>

### started

```bash
# ative virtula env ( linux | mac)
source .venv/bin/activate
# jalanakn migration untuk isi database
python manage.py migrate
# run project
uv run python manage.py runserver
```

use this password for generated or test

> jika belum punya register aja dulu

```bash
user : daraja
pass : dar_231=[]

```

### Main App

> page App yang akan menjadi halaman '/'
> `accounts` ('\accounts\') = untuk mengelola **Users** , baik login , logout , dll
> `pages` ('\pages\') akan menjadi App utama yg menghandle halaman untuk di tampilkan
> `hub` ('\hub\')= bagian pages untuk cominity berinteraksi nantinya
> `api` ('\api\')= app API untuk handle seperti , upload file , dan lain sebagainay

### Static

#### **Api**

- **file** = berisi file file yang akan di simpan

1.  `arsip` "agak berat jadi ada batas mimal" = .zip, .rar, .7z, .tar, .gz, .bz2 ,dll
2.  `code` = .js, .ts, .py, .java, .c, .cpp, .php,.rs, .html, .css, .json, .xml, .yaml, .sh ,dll
3.  `document` = .pdf, .doc, .docx, .xls, .xlsx, .ppt, .pptx, .odt, .ods, .rtf, .txt, .md , dll
4.  `executable` "agar berat jadi ada batas minila " = .exe, .msi, .apk, .deb, .rpm, .dmg, .bin , dll
5.  `image` = .jpg, .jpeg, .png, .gif, .bmp, .tiff, .svg, .webp, .ico , dll

### Folder

- `media` = folder untuk menyimpan file

### table

- `fileManagements` = table untuk menyimpan file

### Dafar Api

1. Upload File

- **Endpoint**: `api/file/upload/`
- **Method**: `POST`
- **Deskripsi**: Mengunggah file baru ke server sekaligus menyimpan metadata ke database.
- **Request Body (form-data)**:
  - `file` _(File, required)_ → File yang ingin diupload.
  - `description` _(string, optional)_ → Deskripsi file.
  - `fileName` _(string, optional)_ → Nama file (jika tidak diisi, default = nama asli file).

- **Response (200)**:

```json
{
  "message": "File uploaded",
  "data": {
    "id": 1,
    "fileName": "example.txt",
    "description": "contoh file",
    "file_size": 1024,
    "code_file": "uploads/example.txt"
  }
}
```

- **Response Error (400)**:

```json
{ "error": "No file uploaded" }
```

2. List Files

- **Endpoint**: `api/file/list/`
- **Method**: `GET`
- **Deskripsi**: Mengambil daftar semua file yang tersimpan dalam database.
- **Response (200)**:

```json
[
  {
    "id": 1,
    "fileName": "example.txt",
    "description": "contoh file",
    "file_size": 1024,
    "code_file": "uploads/example.txt"
  },
  {
    "id": 2,
    "fileName": "image.png",
    "description": "gambar profil",
    "file_size": 2048,
    "image_file": "uploads/image.png"
  }
]
```

3. Download File

- **Endpoint**: `api/file/download/<int:file_id>/`
- **Method**: `GET`
- **Deskripsi**: Mengunduh file berdasarkan **ID**.
- **Parameter Path**:
  - `file_id` _(int, required)_ → ID file yang ingin diunduh.

- **Response (200)**:
  - File akan terunduh dengan `Content-Disposition: attachment; filename="nama_file.ext"`

- **Response Error (404)**:

```json
{ "error": "File not found" }
```

atau

```json
{ "error": "Invalid file ID" }
```

4. Delete File

- **Endpoint**: `api/file/delete/<int:pk>/`
- **Method**: `DELETE`
- **Deskripsi**: Menghapus file (baik di storage maupun di database).
- **Parameter Path**:
  - `pk` _(int, required)_ → ID file yang ingin dihapus.

- **Response (200)**:

```json
{ "message": "File deleted successfully." }
```

- **Response Error (405)**:

```json
{ "error": "Invalid request method." }
```

### Daftar App color

#45758a — background header (biru keabu-abuan, elegan & netral)
#f0c85e — teks judul "Django administration" (emas hangat, kontras tinggi)
#ffffff — latar belakang form (putih bersih)
#000000 — border input / teks utama (hitam pekat)
#d1d5db — warna input dan background default (abu-abu netral)
#5a7b8a — tombol log in (biru abu-abu lebih gelap, serasi dengan header)

Tambahan warna rujukan (umum):
#1f2937 — abu tua (teks header/sidebar)
#374151 — abu-abu gelap (secondary background)
#9ca3af — abu-abu terang (placeholder teks / garis pembatas)
#e5e7eb — abu-abu sangat terang (hover background / border halus)
#f9fafb — putih lembut (background alternatif)
#2563eb — biru utama (link / tombol aktif)
#3b82f6 — biru cerah (hover state tombol/link)
#10b981 — hijau utama (emerald, aksi positif) ✅
#059669 — hijau tambahan (status sukses)
#9333ea — ungu (aksen tambahan, misalnya badge / highlight)
**Kategori khusus**
#dc2626 — Error (merah utama)
#ef4444 — Error terang (background error ringan)
#16a34a — Success (hijau utama)
#22c55e — Success terang (notifikasi positif ringan)
#f59e0b — Warning (oranye utama)
#fbbf24 — Warning terang (background warning)
#0ea5e9 — Info (biru utama)
#38bdf8 — Info terang (notifikasi info ringan)
