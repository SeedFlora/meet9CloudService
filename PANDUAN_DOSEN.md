# Panduan Dosen Lab 09 — Gradio dan evaluasi sentimen

**Repo materi:** `SeedFlora/meet9CloudService` · **durasi contoh:** 100 menit · **jalur wajib:** Python lokal tanpa akun · **jalur pilihan:** DistilBERT dan Hugging Face Space bila layanan tersedia. Mahasiswa menerima [modul dengan kunci lengkap](MODUL_MAHASISWA.md), sehingga nilai praktik ditentukan oleh bukti run dan penjelasan hasil milik mereka, bukan hafalan kode.

## Hasil belajar dan alur kerja nyata

Mahasiswa memisahkan data latih, fungsi prediksi, aturan ambang keputusan, UI, dan evaluasi. Kasusnya adalah triase ulasan pelanggan: tim operasional membutuhkan label awal dan bukti kapan skor tidak cukup untuk keputusan otomatis. Jelaskan sejak awal bahwa 24 sampel latihan adalah bahan eksperimen, bukan model produksi.

## Persiapan sebelum kelas

1. Buka root repo ini di PowerShell atau terminal Bash. Pastikan Python 3, port 7860 kosong, dan internet tersedia hanya saat instalasi pertama.
2. PowerShell: `python -m venv .venv`; `.\.venv\Scripts\python -m pip install -r requirements.txt`. Bash: `python3 -m venv .venv`; `.venv/bin/python -m pip install -r requirements.txt`.
3. Jalankan `.\.venv\Scripts\python core.py` dan `.\.venv\Scripts\python -B tests\challenge.py` (atau path Bash setara). Harapkan `sanity check lulus` dan **9 PASS, 0 FAIL**. Uji ini tidak mengunduh DistilBERT.
4. Jalankan `.\.venv\Scripts\python app.py`; buka `http://127.0.0.1:7860`. Pastikan halaman memuat input, radio model, slider, panel probabilitas, panel JSON, dan tabel token.
5. Siapkan dua terminal: satu untuk server, satu untuk test/perintah. Jangan jalankan Gradio ganda di port 7860. Lihat [panduan Git](PANDUAN_GIT.md) dan minta mahasiswa memakai repo milik sendiri.

Pada komputer verifikasi, baseline, UI Gradio **6.29.0** sesuai `requirements.txt`, dan checker 9 PASS semuanya lulus. Jalankan checker lagi pada mesin kelas untuk mendeteksi perbedaan lingkungan.

## Rencana mengajar menit demi menit

| Menit | Demo dosen | Tindakan mahasiswa | Bukti/pertanyaan |
|---|---|---|---|
| 0–10 | Tunjukkan `training.tsv` dan struktur `core.py`/`app.py`. | Hitung contoh dan label. | Mengapa data latih bukan data evaluasi? |
| 10–25 | Jalankan `core.py`, baca tokenisasi dan smoothing. | Jalankan sanity check. | Output lulus dan 24 contoh. |
| 25–45 | Jalankan UI; uji kalimat positif dan negatif. | Isi dua input dan catat skor. | Screenshot kedua hasil dan token. |
| 45–60 | Naikkan ambang 0,5 → 0,9 pada teks yang sama. | Bandingkan skor serta `Detail.decision`. | Skor tetap, keputusan berubah. |
| 60–70 | Kosongkan input dan jelaskan pesan validasi. | Uji input kosong/model salah lewat checker. | Error terstruktur, server tetap hidup. |
| 70–85 | Jalankan `tests/challenge.py`. | Catat 9 PASS dan jawab pertanyaan. | Jelaskan tiap check; bukan sekadar salin output. |
| 85–100 | Bahas batas model, opsi DistilBERT, Git. | Simpan laporan, screenshot sendiri, push. | Repo mahasiswa dan refleksi. |

## Kunci demo langkah demi langkah

**1. Data.** `Get-Content .\training.tsv | Select-Object -First 5` menunjukkan header dan contoh positive. `core.py` memuat 24 baris, memisahkan kata dengan regex Unicode, dan membangun frekuensi per label. Jika TSV diubah menjadi satu label saja, `load_training()` kini memberi error yang jelas; diskusikan mengapa klasifier dua kelas perlu kedua label.

**2. Baseline.** `.\.venv\Scripts\python core.py` menampilkan `Baseline terlatih; sanity check lulus.`. Dua `assert` hanya pemeriksaan dasar. Jangan menyebutnya metrik akurasi.

**3. Prediksi.** Di browser pilih **Baseline lokal** dan ambang 0,5. `layanan ini cepat dan membantu` memberi skor positif sekitar **0,8986**, `decision=positive`. `aplikasi sering gagal dibuka` memberi skor negatif sekitar **0,8545**. Bila nilai berubah setelah mahasiswa menyunting data, fokus pada arah keputusan dan alasan perubahan.

**4. Ambang.** Teks positif yang sama pada ambang 0,9 tetap punya probabilitas positif sekitar 0,8986, tetapi `decision=negative`. Panel Gradio Label menonjolkan kelas dengan probabilitas terbesar; panel JSON berisi keputusan menurut ambang. Minta mahasiswa menjelaskan beda skor dan aturan bisnis sebelum melihat kunci.

**5. Validasi.** Input kosong menghasilkan `Detail.error = Masukkan teks terlebih dahulu.`. `analyze("uji", "model tak dikenal", 0.5)` juga mengembalikan error. Mode DistilBERT hanya pilihan tambahan; jika dependency/checkpoint tidak tersedia, jangan menahan kelas.

**6. Pemeriksa.** `.\.venv\Scripts\python -B tests\challenge.py` memeriksa sembilan syarat: 24 contoh dan dua label, tokenisasi, skor dua polaritas, perubahan keputusan pada 0,9, keluaran UI, input kosong, mode salah, serta TSV dapat dimuat. **9 PASS, 0 FAIL** berarti jalur baseline teruji; kualitas model pada data nyata tetap perlu evaluasi terpisah.

![UI Gradio sesudah prediksi nyata](screenshots/09_web_hasil.png)

*Command/tindakan:* `python app.py` kemudian klik **Analisis**. *Fungsi:* menunjukkan aliran input ke model dan tiga keluaran. *Cara kerja:* Gradio memanggil `analyze`, model menghitung skor, JSON menampilkan ambang/keputusan. *Baca hasil:* sekitar 0,8986 untuk contoh positif pada ambang 0,5.

![UI Gradio pada ambang 0,9](screenshots/09_web_ambang.png)

*Command/tindakan:* ubah slider menjadi 0,9 dan klik lagi. *Fungsi:* memperlihatkan aturan keputusan. *Cara kerja:* `decide()` membandingkan skor dengan ambang tanpa training ulang. *Baca hasil:* skor sama, `decision=negative`.

![Hasil checker baseline Lab 09](screenshots/09_challenge_output.png)

*Command:* `.\.venv\Scripts\python -B tests\challenge.py`. *Fungsi:* verifikasi data/model/UI sebelum penilaian. *Cara kerja:* sembilan pemeriksaan otomatis dijalankan tanpa mengunduh DistilBERT. *Baca hasil:* 9 PASS, 0 FAIL; keluaran aktual ditata ulang agar terbaca.

## Kunci pertanyaan dan diskusi

1. Skor yang tinggi pada kalimat yang mirip data latih tidak membuktikan generalisasi; perlu data uji terpisah dan metrik precision, recall, confusion matrix.
2. Ambang lebih tinggi biasanya mengurangi keputusan positif; false positive dapat turun, false negative dapat naik. Tradeoff harus ditentukan sesuai biaya salah klasifikasi.
3. Prediksi pertama DistilBERT memerlukan unduhan bila belum ada cache, load bobot, dan inisialisasi; objek `_transformer` disimpan sehingga berikutnya lebih cepat.
4. Model Inggris pada teks Indonesia adalah perbandingan lintas bahasa yang tidak terkendali. Gunakan set evaluasi bahasa yang sama serta metrik yang sama sebelum menyimpulkan.

## Penilaian dan penyelesaian masalah

Nilai bukti praktik: dua teks dan ambang (30%), penjelasan skor vs keputusan (25%), validasi dan checker (20%), analisis keterbatasan (15%), laporan/Git rapi (10%). Jika port 7860 bentrok, hentikan proses Gradio lama. Jika install gagal, cek interpreter/venv dan ulangi `python -m pip install -r requirements.txt`; jangan menginstal DistilBERT untuk menyelesaikan baseline. Jika screenshot kosong, tunggu UI selesai memuat sebelum mengambilnya. Sembunyikan token atau ulasan pribadi dari laporan. Setelah kelas, hentikan server dengan `Ctrl+C`.


## Bukti visual tambahan untuk demo

![UI Gradio sebelum analisis](screenshots/09_web_awal.png)

*Command:* `.\.venv\Scripts\python app.py`, lalu buka port 7860. *Fungsi:* mengenalkan kontrol. *Cara kerja:* Gradio menyusun Textbox, Radio, Slider, tombol, Label, JSON, dan tabel. *Baca hasil:* form siap menerima teks.

![Hasil negatif](screenshots/lab09_negative.png)

*Command/tindakan:* isi `aplikasi sering gagal dibuka` dan klik **Analisis**. *Fungsi:* membandingkan polaritas. *Cara kerja:* token negatif menggeser skor Naive Bayes. *Baca hasil:* label negatif sekitar 0,8545 pada data bawaan; gambar dari praktik sebelumnya.

![Validasi input kosong](screenshots/lab09_empty.png)

*Command/tindakan:* kosongkan Textbox dan klik **Analisis**. *Fungsi:* menguji validasi UI. *Cara kerja:* `analyze` memberi `Detail.error` tanpa mematikan server. *Baca hasil:* pesan agar teks dimasukkan; gambar dari praktik sebelumnya.
