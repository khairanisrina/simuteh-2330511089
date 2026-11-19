# SIMUTEH - Praktikum Computer Vision (P1-P6)

**Sistem Pemeriksaan Mutu Daun Teh Berbasis Citra** untuk Kelompok Tani Teh Rakyat, Kabupaten Sukabumi.

Nama: Khansa Nisrina | NIM: 2330511089 | Kelas: TI-7B | SEED: 1089

Mata kuliah Computer Vision, Program Studi Teknik Informatika, Universitas Muhammadiyah Sukabumi.

## Versi (tag)

| Tag | Isi | Kegiatan |
|---|---|---|
| `v0.1-praproses` | Modul praproses | Evaluasi P1-P4 |
| `v0.2-tepi` | Deteksi tepi dan algoritma Canny | Praktikum P5 |
| `v0.3-morfologi` | Morfologi, komponen terhubung, dan modul `bercak.py` | Praktikum P6 |

## Struktur repository

```
simuteh-2330511089/
|-- data/
|   |-- sintetis/              citra, mask_daun, mask_bercak, label.csv (hasil skrip)
|-- notebook/
|   |-- B1..B5                 Evaluasi P1-P4 (lingkungan, warna, histogram, penapisan, praproses)
|   |-- P5_tepi.ipynb          Gradien, operator tepi, dan Canny
|   |-- P6_morfologi.ipynb     Morfologi, pengukuran bercak, dan integrasi bercak.py
|-- src/
|   |-- buat_dataset_sintetis.py
|   |-- utils_cv.py
|   |-- praproses.py           rangkaian praproses (dari P1-P4)
|   |-- utils_tepi.py          kode awal P5-P6 (tepi acuan, skor tepi, mask awal)
|   |-- bercak.py              modul analisis bercak (dibangun di P6)
|-- hasil/                     gambar, tabel .csv, param_praproses.json, param_bercak.json
|-- laporan/                   laporan dan slide
|-- requirements.txt
|-- README.md
```

## Cara menjalankan

1. Pasang pustaka (Python 3.10 atau lebih baru):
   ```
   pip install -r requirements.txt
   ```
2. Bangkitkan dataset sintetis dari folder utama. Pastikan `SEED = 1089` di dalam skrip:
   ```
   python src/buat_dataset_sintetis.py
   ```
3. Jalankan notebook di folder `notebook/` secara berurutan, dari awal sampai akhir (Restart & Run All):
   `B1` sampai `B5`, lalu `P5_tepi.ipynb`, lalu `P6_morfologi.ipynb`.

Semua notebook dijalankan dari folder `notebook/`, sehingga jalur berkas di dalam kode diawali `../`.

## Cara memakai `analisis_daun`

Modul `bercak.py` menerima citra BGR hasil praproses, lalu mengembalikan jumlah bercak, persen bercak, dan kelas mutu.

```python
import sys, json
sys.path.append("../src")

from utils_cv import baca
from praproses import praproses
from bercak import analisis_daun

PARAM = json.load(open("../hasil/param_praproses.json"))
PB    = json.load(open("../hasil/param_bercak.json"))

img   = baca("../data/sintetis/citra/teh_041.png")
hasil = analisis_daun(praproses(img, PARAM), PB)

print(hasil["jumlah_bercak"], hasil["persen_bercak"], hasil["kelas"])
```

Keluaran `analisis_daun` berupa kamus dengan kunci `mask_daun`, `mask_bercak`, `jumlah_bercak`, `persen_bercak`, `kelas` (Sehat, Bercak Ringan, atau Bercak Berat), dan `bercak` (ukuran setiap bercak: luas, keliling, kebulatan, rasio aspek).

## Ringkasan hasil

### P5: Deteksi tepi (`v0.2-tepi`)

- Operator dan kanal dengan F1 tepi tertinggi: [ISI: operator, kanal, nilai F1 dari Tabel 6 petunjuk]
- Pengaruh praproses terhadap F1: [ISI: naik atau turun, berapa, pada kondisi apa]
- Parameter Canny terbaik: sigma = [ISI], ambang = [ISI] (F1 = [ISI])
- Ambang otomatis berbasis median: [ISI: berhasil atau gagal pada kondisi mana] dan perbaikan memakai `canny_persentil` (q = [ISI])
- Keputusan pemakaian deteksi tepi pada SIMUTEH: [ISI: dipakai untuk apa, tidak dipakai untuk apa, singkat]

### P6: Morfologi dan analisis bercak (`v0.3-morfologi`)

- Kombinasi pembersih bercak terpilih: k = [ISI], SE [ISI: bentuk] dengan opening [ISI] dan closing [ISI]
- Aturan penyaringan terpilih: luas_min = [ISI], bulat_min = [ISI], rasio_maks = [ISI]
- Evaluasi `bercak.py` pada 60 citra:

| Ukuran | Nilai |
|---|---|
| Galat absolut rerata persen bercak | [ISI] |
| Korelasi persen prediksi dan acuan | [ISI] |
| Akurasi kelas | [ISI] |
| Daun sehat dinilai berbercak | [ISI] |
| Daun berbercak dinilai sehat | [ISI] |
| Kondisi cahaya dengan akurasi terendah | [ISI] |

- Parameter final tersimpan di `hasil/param_bercak.json`.

## Keterbatasan

- Dataset sintetis; bercak berbentuk lingkaran sehingga aturan kebulatan belum teruji pada foto nyata.
- `mask_daun_awal` dan `bercak_awal` masih sementara dan akan diganti dengan metode segmentasi pada Pertemuan 7.
- Batas kelas (0,1% dan 2,0%) ditentukan dari dataset yang sama dengan evaluasi, sehingga akurasi cenderung optimistis. [ISI: tambahkan keterbatasan lain dari analisismu]
- Konversi 0,4375 mm per piksel mengasumsikan jarak kamera 200 mm.

## Rencana selanjutnya

Pertemuan 7 (segmentasi): ambang global dan adaptif, Otsu, region growing, watershed, dan klaster. Hasilnya dievaluasi dengan IoU terhadap mask acuan, lalu diteruskan ke `bersihkan` dan `ukur_dan_saring` di `bercak.py`.
