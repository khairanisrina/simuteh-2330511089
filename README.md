
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

```text
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
   ```bash
   pip install -r requirements.txt
   ```

2. Bangkitkan dataset sintetis dari folder utama. Pastikan `SEED = 1089` di dalam skrip:
   ```bash
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

- Operator dan kanal dengan F1 tepi tertinggi: **Canny pada kanal R (Red)**, dengan F1 = **0,985** pada citra mentah (sigma = 2, ambang 30/90). Setelah praproses, F1 mencapai **0,983**. Hasil ini menunjukkan kanal R paling informatif untuk mendeteksi tepi bercak pada dataset yang diuji.

- Pengaruh praproses terhadap F1: praproses meningkatkan F1 pada kanal R untuk Sobel dari 0,538 menjadi 0,905, Prewitt dari 0,605 menjadi 0,918, dan LoG dari 0,921 menjadi 0,927. Namun, F1 Canny sedikit turun dari 0,985 menjadi 0,983. Pada kanal Gray, F1 juga cenderung turun, yaitu Sobel 0,831 menjadi 0,821, Prewitt 0,856 menjadi 0,811, LoG tetap 0,740, dan Canny 0,754 menjadi 0,746. Dengan demikian, pengaruh praproses bergantung pada kanal dan operator yang digunakan.

- Parameter Canny terbaik: sigma = **2**, ambang = **30/90** (F1 = **0,983**, presisi = 0,989, recall = 0,978 pada kanal R sesudah praproses). Namun, untuk mempertahankan bercak kecil, sigma = 1 dan ambang 30/90 lebih sensitif dengan recall bercak ringan 0,981, meskipun F1 keseluruhan turun menjadi 0,824.

- Ambang otomatis berbasis median: memberikan hasil yang kurang konsisten, terutama pada kondisi kontras rendah. Pada kanal Gray, F1 turun menjadi 0,000, sedangkan pada kanal R F1 mencapai 0,849. Ambang otomatis juga kurang baik dibanding ambang tetap pada kondisi bayangan dan gelap. Perbaikan menggunakan `canny_persentil` dengan **q = 98**, yang menghasilkan F1 = **0,991** pada kanal R, dibandingkan rerata F1 0,931 dari ambang median otomatis. Nilai F1 q=98 pada lima kondisi cahaya berada pada rentang 0,978–0,996.

- Keputusan pemakaian deteksi tepi pada SIMUTEH: deteksi tepi digunakan sebagai alat bantu menemukan batas daun dan mengeksplorasi batas bercak, bukan sebagai segmentasi akhir atau pengukur luas bercak. Gradien morfologi dengan SE 3×3 dipilih untuk membantu menemukan batas daun, sedangkan kanal R dengan Canny digunakan untuk eksplorasi batas bercak. Penghitungan persentase bercak tetap menggunakan mask wilayah biner yang dibersihkan melalui morfologi dan dianalisis dengan komponen terhubung.

### P6: Morfologi dan analisis bercak (`v0.3-morfologi`)

- Kombinasi pembersih bercak terpilih: k = **4**, SE **elips** dengan ukuran **5×5**, menggunakan opening **5×5** dan closing **5×5**. Opening diprioritaskan untuk menghilangkan derau dan komponen kecil. Pada citra teh_021, opening menurunkan jumlah komponen dari 191 menjadi 14 dan meningkatkan IoU dari 0,187 menjadi 0,649. Closing digunakan setelah opening untuk membantu menutup celah kecil pada objek. SE elips 5×5 dipertahankan karena sesuai dengan karakter bercak sintetis yang cenderung membulat, meskipun SE persegi 5×5 menghasilkan galat jumlah komponen yang lebih rendah pada eksperimen tertentu.

- Aturan penyaringan terpilih: luas_min = **20 piksel**, bulat_min = **0,5**, rasio_maks = **1,8**. Kombinasi ketiga aturan ini menghasilkan galat jumlah komponen terendah dibandingkan aturan tanpa penyaringan maupun penyaringan sebagian.

- Evaluasi `bercak.py` pada 60 citra:

| Ukuran | Nilai |
|---|---|
| Galat absolut rerata persen bercak | 0,284 poin persentase |
| Korelasi persen prediksi dan acuan | 0,970 |
| Akurasi kelas | 91,7% (55/60 citra benar) |
| Daun sehat dinilai berbercak | 1 citra (False Positive) |
| Daun berbercak dinilai sehat | 3 citra (False Negative) |
| Kondisi cahaya dengan akurasi terendah | Kontras rendah: 75,0% |

- Lima citra yang salah kelas terdiri dari satu citra sehat yang diprediksi bercak ringan, tiga citra bercak ringan yang diprediksi sehat, dan satu citra bercak berat yang diprediksi bercak ringan. Kesalahan terutama berkaitan dengan luas bercak yang terukur terlalu kecil atau kandidat bercak palsu yang lolos penyaringan.

- Pada citra `teh_041`, modul menghasilkan 10 komponen bercak dengan total luas 3.878 piksel atau 742,27 mm². Pengukuran menggunakan konektivitas 8 dan skala 0,4375 mm/piksel.

- Parameter final tersimpan di `hasil/param_bercak.json`.

## Keterbatasan

- Dataset sintetis; bercak berbentuk lingkaran sehingga aturan kebulatan belum teruji pada foto nyata. Bentuk bercak sintetis belum mewakili variasi bercak lapangan yang tidak beraturan, memanjang, menyatu, atau memiliki tepi kabur.

- `mask_daun_awal` dan `bercak_awal` masih menggunakan pendekatan berbasis aturan intensitas dan akan dikembangkan dengan metode segmentasi pada Pertemuan 7.

- Batas kelas (0,1% dan 2,0%) ditentukan dari dataset yang sama dengan evaluasi, sehingga akurasi cenderung optimistis. Belum ada pemisahan data latih, validasi, dan uji yang independen untuk mengukur kemampuan generalisasi pada citra baru.

- Konversi 0,4375 mm per piksel mengasumsikan jarak kamera 200 mm dan geometri pengambilan gambar tetap. Perubahan jarak kamera, fokus, atau perspektif dapat menyebabkan hasil pengukuran luas fisik tidak akurat sehingga diperlukan kalibrasi menggunakan objek referensi.

- Kondisi kontras rendah menjadi sumber kesalahan utama, dengan akurasi kelas hanya 75%. Pada kondisi ini, bercak kecil berpotensi hilang pada tahap pembentukan mask atau penyaringan komponen.

- Penyaringan berdasarkan kebulatan minimal 0,5 dan rasio aspek maksimal 1,8 berisiko menghilangkan bercak nyata yang bentuknya memanjang atau tidak beraturan.

- False Negative lebih berisiko karena daun yang sebenarnya berpenyakit dapat dinilai sehat dan lolos pemeriksaan. Hasil sistem karena itu tetap perlu diperiksa oleh petugas dan tidak boleh menjadi satu-satunya dasar keputusan mutu daun.

- Evaluasi belum mengukur generalisasi pada foto lapangan. Akurasi 91,7% merupakan hasil pada dataset sintetis yang digunakan dalam pengujian, bukan jaminan performa pada kondisi perkebunan sebenarnya.

## Rencana selanjutnya

Pertemuan 7 (segmentasi): ambang global dan adaptif, Otsu, region growing, watershed, dan klaster. Hasilnya dievaluasi dengan IoU terhadap mask acuan, lalu diteruskan ke `bersihkan` dan `ukur_dan_saring` di `bercak.py`.

Pengembangan selanjutnya juga akan memprioritaskan evaluasi citra dengan kontras rendah, bercak kecil, serta bentuk bercak yang tidak beraturan. Data akan dipisahkan menjadi data latih, validasi, dan uji berdasarkan citra atau sesi pengambilan. Parameter ditentukan menggunakan data validasi dan dievaluasi satu kali pada data uji terpisah untuk memperoleh hasil yang lebih objektif.
