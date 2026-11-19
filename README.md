# SIMUTEH - Evaluasi Praktikum P1-P4 Computer Vision
Nama: Khansa Nisrina | NIM: 2330511089 | Kelas: TI-7B | SEED: 1089

## Cara menjalankan
1. `pip install -r requirements.txt`
2. Dari folder utama: `python src/buat_dataset_sintetis.py`
3. Jalankan notebook di folder `notebook/` dari awal sampai akhir.

## Ringkasan hasil
- Kanal terpilih: R (KB tertinggi pada semua kondisi cahaya)
- Praproses final: {"gamma": "auto", "clahe_clip": 1.0, "clahe_tile": 4, "clahe_otomatis": true, "penapis": "median", "kernel": 3}
- Rerata KB sesudah praproses per kondisi: {'bayangan': 7.82, 'gelap': 10.91, 'kontras_rendah': 7.71, 'normal': 13.02, 'terang': 12.03}
