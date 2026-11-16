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

## Tambahan: hubungkan model ke website (tanpa GPU)

Folder `web/` berisi dua halaman yang menghubungkan model ke website tanpa backend berat:

| File | Cara kerja | Perlu server Python? |
|---|---|---|
| `web/gradio-client.html` | memanggil endpoint `/analyze` milik `app.py` lewat [`@gradio/client`](https://www.npmjs.com/package/@gradio/client) | ya, `app.py` harus hidup |
| `web/browser-sentiment.html` | model `Xenova/bert-base-multilingual-uncased-sentiment` berjalan di browser dengan [Transformers.js](https://huggingface.co/docs/transformers.js) | tidak |

PowerShell, dua terminal dari root repo Lab 09:

```powershell
# Terminal 1
.\.venv\Scripts\python app.py
# Terminal 2
.\.venv\Scripts\python -m http.server 8000 --directory web
```

Buka <http://localhost:8000/gradio-client.html>, lalu <http://localhost:8000/browser-sentiment.html>. Jangan membuka file dengan dobel-klik (`file://`): app Gradio lokal hanya mengizinkan origin `localhost`, sehingga panggilan dari `file://` ditolak.

- Unduhan model browser pertama sekitar 170 MB (`model_quantized.onnx`), berikutnya dari cache browser. Model memberi label `1 star` sampai `5 stars`; halaman memetakan 4-5 bintang ke `positive` dan 1-2 bintang ke `negative`.
- Deploy gratis `browser-sentiment.html`: buat Space dengan SDK **Static** lalu unggah sebagai `index.html`, atau pakai GitHub Pages/Vercel. Static Space gratis untuk semua akun.
- `gradio-client.html` juga dapat memanggil Space publik: isi kolom sumber dengan `username/nama-space`. Space privat membutuhkan token, jadi panggil dari server (Route Handler Lab 08), bukan dari browser.
- Hasil uji 16 November 2026 (Chrome headless, Gradio 6.29.0): `gradio-client.html` mengembalikan keputusan `positive` (probabilitas 0.8986) untuk "layanan ini cepat dan membantu"; `browser-sentiment.html` memberi `5 stars` untuk kalimat itu dan `1 star` untuk "aplikasi sering gagal dibuka".

## Hugging Face Spaces dan iframe (perluasan opsional)

Selesaikan baseline lokal lebih dahulu. Per 16 November 2026, membuat Gradio/Docker Space berbasis CPU memerlukan paket berbayar (PRO). Akun free yang berumur minimal 30 hari dengan email terverifikasi boleh membuat maksimal 2 Gradio Space di ZeroGPU, tetapi app wajib memiliki fungsi `@spaces.GPU`; baseline Naive Bayes ini tidak memakainya. Jalur gratis untuk semua akun adalah Static Space berisi `web/browser-sentiment.html` (lihat bagian *Tambahan* di bawah). Periksa biaya/kuota di dashboard sebelum menyalakan compute ([Spaces overview](https://huggingface.co/docs/hub/spaces-overview), [ZeroGPU](https://huggingface.co/docs/hub/spaces-zerogpu)).

1. Login ke Hugging Face, klik **New Space**, pilih nama, SDK **Gradio**, dan hardware sesuai paket akun (CPU untuk PRO, ZeroGPU untuk akun free yang memenuhi syarat). Pilih visibilitas sesuai data demo. Catat URL Git repo Space milik Anda.
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
