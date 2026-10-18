# Lab 09 — Hugging Face, Gradio, dan model sentiment

<!-- lecture-materials:start -->

## Materi teori sebelum praktikum

- [Pertemuan 09: Hugging Face Spaces](slides/Teori_Pertemuan_09.pptx)

Slide menghubungkan konsep, kasus kerja, bacaan/video resmi, dan langkah lab.

<!-- lecture-materials:end -->

**Kebijakan kelas:** Lab ini latihan formatif, tanpa tugas, nilai, atau penyerahan terpisah. Satu proyek besar dikerjakan oleh kelompok **3 orang**, dengan presentasi checkpoint minggu 7 (UTS) dan hasil akhir minggu 14 (UAS). Simpan hasil lab hanya bila berguna sebagai referensi atau bukti proses proyek. Baca [brief proyek kelompok](PROYEK_KELOMPOK.md). Bobot resmi tetap mengikuti RPS/LMS.

**Capaian:** membangun UI ML dengan beberapa tipe komponen, melatih baseline kecil, membandingkan hasil dengan DistilBERT, dan memahami biaya/latensi deployment. Jalur wajib berjalan lokal tanpa akun.

## Mulai praktikum lokal

Ikuti [modul mahasiswa langkah demi langkah](MODUL_MAHASISWA.md). Modul memakai **PowerShell, clone baru, satu perintah tiap langkah**, hasil yang diharapkan, dan screenshot contoh. Semua langkah utama berjalan lokal. Tidak ada laporan atau push terpisah yang wajib dikumpulkan.

## DistilBERT opsional

Instal dependency berat: `.\.venv\Scripts\python -m pip install -r requirements-transformer.txt` (PowerShell) atau `.venv/bin/python -m pip install -r requirements-transformer.txt` (bash). Pilih **DistilBERT English** pada UI. Unduhan checkpoint pertama membutuhkan internet dan ruang disk; model ini dilatih untuk teks bahasa Inggris, jadi gunakan contoh Inggris. Catat latensi pertama (unduh + load) dan latensi setelah model siap.

Python 3.10+ memenuhi minimum versi [Transformers](https://pypi.org/project/transformers/5.19.0/) dan [PyTorch](https://pypi.org/project/torch/2.14.1/) yang diperiksa dalam rentang dependency opsional; instalasi model tetap terpisah dari baseline.

## Hugging Face Spaces dan iframe (perluasan opsional)

Selesaikan baseline lokal lebih dahulu. Jalur ini memerlukan akun dan akses membuat Gradio Space. Pilih hardware CPU yang tersedia pada akun. Periksa biaya/kuota di dashboard sebelum menyalakan compute.

1. Login ke Hugging Face, klik **New Space**, pilih nama, SDK **Gradio**, dan hardware CPU yang tersedia. Pilih visibilitas sesuai data demo. Catat URL Git repo Space milik Anda.
2. Buka PowerShell di folder induk praktikum. Clone URL tersebut ke folder baru. Salin `app.py`, `core.py`, `training.tsv`, dan `requirements.txt` dari repo Lab 09 ke root repo Space. Salin `SPACE_README.md` sebagai **README.md**. Metadata SDK dan `app_file` sekarang ada di root.
3. Pada **Space Settings → Variables and secrets**, tambahkan **Variable** `GRADIO_SERVER_NAME` bernilai `0.0.0.0`. Kode `app.py` membacanya melalui environment. Jalur laptop tetap memakai `127.0.0.1`.
4. Di folder repo Space, jalankan `git add app.py core.py training.tsv requirements.txt README.md`, `git commit -m "Add classroom sentiment demo"`, lalu `git push`. Gunakan autentikasi Git akun sendiri. Token hanya dimasukkan ke prompt autentikasi, bukan ke URL atau source.
5. Baca tab **Logs** sampai **Running**, buka app, lalu ulangi satu teks positif dan satu teks negatif. Tombol **Embed this Space** menyediakan URL aplikasi dan contoh iframe.
6. Pada halaman JSX proyek Next.js sendiri, salin iframe dari menu Embed. Isi `title="Sentiment demo"`, atur lebar `100%` dan tinggi yang cukup, lalu buka halaman Next.js untuk memastikan UI benar-benar termuat. URL repo `huggingface.co/spaces/...` berbeda dari URL aplikasi `*.hf.space`.

Perintah CLI login yang berlaku saat revisi adalah `hf auth login` setelah memasang `huggingface_hub`. Pembuatan repo tersedia melalui `hf repos create NAMA_SPACE --repo-type space --sdk gradio`. Dashboard di langkah 1 lebih mudah untuk memilih akses dan hardware. [Dokumentasi CLI resmi](https://huggingface.co/docs/huggingface_hub/en/guides/cli), [konfigurasi Spaces](https://huggingface.co/docs/hub/en/spaces-config-reference).

Static Space menjalankan HTML/JS, sehingga tidak menjalankan Python Gradio ini. DistilBERT baru tersedia di Space setelah dependency model opsional dimasukkan dan build berhasil. Demo cloud tidak termasuk hasil yang sudah diverifikasi pada screenshot lokal modul.

**Bukti:** tiga teks uji yang mencakup dua label, waktu respons, screenshot UI, dan perbandingan baseline vs DistilBERT (bila dicoba). **Git opsional:** push source dan data latihan; cache model dan `.venv` tidak boleh ikut.

Rujukan: [HF Spaces](https://huggingface.co/docs/hub/en/spaces-overview), [HF Spaces hardware](https://huggingface.co/docs/hub/main/spaces-gpus), [DistilBERT model](https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english), [Transformers pipeline](https://huggingface.co/docs/transformers/main_classes/pipelines).

Pemeriksa baseline: PowerShell `.\.venv\Scripts\python -B tests\challenge.py`; Bash `.venv/bin/python -B tests/challenge.py`. Hasil uji dengan Gradio 6.29.0: **9 PASS, 0 FAIL** tanpa DistilBERT.

Panduan: [modul mahasiswa dan kunci](MODUL_MAHASISWA.md), [panduan Git](PANDUAN_GIT.md). Screenshot ada di `screenshots/`.
