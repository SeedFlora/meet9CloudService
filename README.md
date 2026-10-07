# Lab 09 — Hugging Face, Gradio, dan model sentiment

<!-- lecture-materials:start -->

## Materi teori sebelum praktikum

- [Pertemuan 09: Hugging Face Spaces](slides/Teori_Pertemuan_09.pptx)

Slide menghubungkan konsep, kasus kerja, bacaan/video resmi, dan langkah lab.

<!-- lecture-materials:end -->

**Kebijakan kelas:** Lab ini latihan formatif, tanpa tugas, nilai, atau penyerahan terpisah. Satu proyek besar dikerjakan oleh kelompok **3 orang**, dengan presentasi checkpoint minggu 7 (UTS) dan hasil akhir minggu 14 (UAS). Simpan hasil lab hanya bila berguna sebagai referensi atau bukti proses proyek. Baca [brief proyek kelompok](PROYEK_KELOMPOK.md). Bobot resmi tetap mengikuti RPS/LMS.

**Capaian:** membangun UI ML dengan beberapa tipe komponen, melatih baseline kecil, membandingkan hasil dengan DistilBERT, dan memahami biaya/latensi deployment. Jalur wajib berjalan lokal tanpa akun.

## Lokal, ringan

Dari root repo Lab 09:

PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python core.py
.\.venv\Scripts\python app.py
```

Bash/WSL:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python core.py
.venv/bin/python app.py
```

Buka `http://127.0.0.1:7860`. Coba contoh positif/negatif, ubah ambang, dan periksa tabel token. UI memakai Markdown, Textbox, Radio, Slider, Button, Label, JSON, Dataframe, dan Examples. `core.py` melatih Naive Bayes dari data `training.tsv`; ini model kecil untuk praktik, bukan evaluator kualitas produksi.

## DistilBERT opsional

Instal dependency berat: `.\.venv\Scripts\python -m pip install -r requirements-transformer.txt` (PowerShell) atau `.venv/bin/python -m pip install -r requirements-transformer.txt` (bash). Pilih **DistilBERT English** pada UI. Unduhan checkpoint pertama membutuhkan internet dan ruang disk; model ini dilatih untuk teks bahasa Inggris, jadi gunakan contoh Inggris. Catat latensi pertama (unduh + load) dan latensi setelah model siap.

## Push ke Hugging Face Space (opsional)

Ketersediaan dan biaya hardware Space dapat berubah; periksa dokumentasi resmi serta akun/institusi pada hari praktik. **Jangan mengharuskan mahasiswa membeli plan.** Jika akun/institusi memenuhi syarat, buat Gradio Space, salin `app.py`, `core.py`, `training.tsv`, `requirements.txt`, dan isi `SPACE_README.md` sebagai `README.md` pada repo Space, lalu commit/push dengan autentikasi Git/HF CLI. Setiap push memicu rebuild. Baseline tidak membutuhkan GPU, tetapi deployment tetap mengikuti syarat plan/hardware akun. Jangan menaruh token di URL Git atau source.

Jika deploy tidak tersedia, tunjukkan demo lokal + video dan unggah kode ke GitHub. Static Space gratis dapat dipakai untuk halaman ringkasan, tetapi tidak menjalankan Python/Gradio. Jika Space publik tersedia, embed URL Space di halaman Next.js via iframe; URL harus sesuai domain Space milik Anda.

**Bukti:** tiga teks uji yang mencakup dua label, waktu respons, screenshot UI, dan perbandingan baseline vs DistilBERT (bila dicoba). **Git opsional:** push source dan data latihan; cache model dan `.venv` tidak boleh ikut.

Rujukan: [HF Spaces](https://huggingface.co/docs/hub/en/spaces-overview), [HF Spaces hardware](https://huggingface.co/docs/hub/main/spaces-gpus), [DistilBERT model](https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english), [Transformers pipeline](https://huggingface.co/docs/transformers/main_classes/pipelines).

Pemeriksa baseline: PowerShell `.\.venv\Scripts\python -B tests\challenge.py`; Bash `.venv/bin/python -B tests/challenge.py`. Hasil uji dengan Gradio 6.29.0: **9 PASS, 0 FAIL** tanpa DistilBERT.

Panduan: [modul mahasiswa dan kunci](MODUL_MAHASISWA.md), [panduan Git](PANDUAN_GIT.md). Screenshot ada di `screenshots/`.
