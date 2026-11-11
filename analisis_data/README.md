# Sajian Analisis Data Tiket HIMUP

Sajian data untuk bimbingan: hasil analisis **788 tiket IT Service Desk HIMUP**
periode **Sep–Nov 2026**, disusun sebagai halaman HTML statis (bukan dashboard,
bukan prototipe aplikasi).

Buka berkas `index.html` langsung di browser, atau jalankan server lokal:

```bash
python3 -m http.server 8000
# lalu buka http://localhost:8000/
```

## Isi

| Bagian | Isi |
| :---: | :--- |
| 01 | Latar belakang: tiga persoalan utama beserta angkanya |
| 02 | Perbandingan alur kerja sekarang (WhatsApp) vs alur yang diusulkan |
| 03 | Pembagian beban kerja antar teknisi |
| 04 | Pencapaian SLA per prioritas (P1–P4) |
| 05 | Hambatan di lapangan: waktu tunggu IR, pengiriman, dan vendor |
| 06 | Masalah berulang dan urutan prioritas pembuatan panduan mandiri |
| 07 | Kategori, status, dan dua tingkat penanganan (Layer 1 / Layer 2) |
| 08 | Rancangan aturan penugasan teknisi + simulator bobot |
| 09 | Rancangan tiga layar sistem + ringkasan masalah, bukti, dan usulan |

## Struktur berkas

```
analisis_data/
├── index.html              # seluruh sajian (satu halaman)
├── assets/
│   ├── data.js             # data agregat hasil olahan tiket
│   ├── style.css           # gaya tampilan
│   ├── js/app.js           # pemuatan data, navigasi, animasi angka
│   ├── js/charts.js        # 14 grafik (ECharts)
│   ├── js/panels.js        # tabel, kartu, simulator, komponen dinamis
│   ├── vendor/             # echarts.min.js, gsap.min.js
│   └── diagram_*.puml/svg  # diagram use case (arsip, tidak dipakai di halaman)
├── diagrams/               # diagram proses AS-IS / TO-BE (arsip)
└── tools/                  # skrip Python pembangun data & diagram
```

> **Catatan:** diagram proses (AS-IS/TO-BE dan use case) tidak lagi ditampilkan di
> halaman agar penyajian fokus pada data. Berkasnya tetap disimpan pada folder
> `diagrams/` sebagai arsip.

## Membangun ulang data

`assets/data.js` dihasilkan dari berkas Excel rekapan tiket oleh `tools/build_data.py`.
Berkas sumber tidak disertakan di repositori ini.

```bash
python3 tools/build_data.py
```
