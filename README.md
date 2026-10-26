# Panduan Prototipe UI: Alur Ticketing & Sistem Penentuan Teknisi Lapangan Dinamis

**Studi Kasus:** Departemen IT Infrastructure — PT Maju Mapan YIC (RamenYA! & SushiYa)  
**Tujuan:** Prototipe antarmuka interaktif (*Clickable Prototype*) untuk memvisualisasikan pergeseran fokus Tugas Akhir ke **Alur Kerja Ticketing & Sistem Pengambil Keputusan (SPK) Penugasan Teknisi Lapangan**.  
**Referensi UI:** `himup_ticketing_fe-main` (Tailwind CSS, Palet Warna RamenYA Crimson Red `#e11d48`, Font Poppins, Card-based Layout).

---

## 1. Daftar File Alur Prototipe (Berurutan & Bernomor)

Seluruh berkas prototype disimpan di direktori `prototype_flow_penentuan_teknisi/` dan dapat langsung dibuka di browser apa pun:

| Nomor File | Nama Berkas | Aktor / Role | Deskripsi & Peran Alur |
| :---: | :--- | :--- | :--- |
| **00** | [`index.html`](./index.html) | *Portal Utama* | **Beranda Utama & Hub Navigasi:** Ringkasan konteks riset, metrik 91 cabang & 6 teknisi, tombol reset data, dan akses cepat ke tiap langkah. |
| **01** | [`01_dashboard_operasional.html`](./01_dashboard_operasional.html) | IT SPV / Manager | **Dashboard Monitoring:** Memperlihatkan kondisi awal di mana **seluruh 6 teknisi lapangan sedang sibuk** bekerja di outlet lain (*100% busy*). |
| **02** | [`02_pelaporan_tiket_pic_cabang.html`](./02_pelaporan_tiket_pic_cabang.html) | PIC Cabang | **Formulir Laporan Darurat:** PIC Cabang Gandaria City melaporkan POS Kasir Utama mati mendadak saat jam makan siang (*Critical Level 4*). |
| **03** | [`03_antrean_tiket_it_spv.html`](./03_antrean_tiket_it_spv.html) | IT SPV | **Meja Triage SPV:** IT Supervisor meninjau tiket darurat masuk dan memicu sistem pendukung keputusan (SPK) penentuan teknisi. |
| **04** | [`04_spk_rekomendasi_teknisi.html`](./04_spk_rekomendasi_teknisi.html) | IT SPV (DSS) | ⭐ **INTI RISET (HERO FEATURE):** Sistem Pendukung Keputusan menghitung matriks trade-off (Jarak Haversine, Estimasi Sisa Waktu SOP, dan Biaya Interupsi Tugas Lama) untuk 6 teknisi. |
| **05** | [`05_dispatch_dan_notifikasi.html`](./05_dispatch_dan_notifikasi.html) | IT SPV | **Konfirmasi Dispatch:** Eksekusi penugasan tiket ke teknisi terpilih (Budi Santoso), transmisi notifikasi mobile, dan simulasi rute GPS. |
| **06** | [`06_mobile_app_teknisi.html`](./06_mobile_app_teknisi.html) | IT Support Lapangan | **Aplikasi Mobile Teknisi:** Tampilan smartphone teknisi realistis: *hanya 2 aksi operasional (Check-in saat tiba & Check-out saat selesai)* tanpa slider persen fiktif! |
| **07** | [`07_verifikasi_resolusi_tiket.html`](./07_verifikasi_resolusi_tiket.html) | PIC Cabang & SPV | **Resolusi & Penutupan Resmi:** Verifikasi hasil perbaikan di outlet, rating kepuasan bintang 5, pencatatan log waktu (SLA 33 menit), dan status Closed. |
| **Data** | [`shared_state.js`](./shared_state.js) | *State Engine* | Logika perhitungan skor SPK, data benchmark durasi SOP 6 teknisi, dan persistensi status tiket via `localStorage`. |

---

## 2. Inovasi Desain: Mengapa Menggunakan "Estimasi Standar Waktu SOP"?

Di dunia operasional IT Support lapangan nyata, **tidak masuk akal jika teknisi mengupdate persentase pengerjaan (misal 85%) secara manual di tengah membongkar mesin**.

Oleh karena itu, sistem ini menerapkan pendekatan ilmiah berbasis **Standar Durasi Penanganan (Standard Service Time / MTTR Benchmark)**:
1. **Standar Waktu per Perangkat di SOP:**
   - Thermal Printer: Standar **30 menit**.
   - Mesin EDC: Standar **25 menit**.
   - Server & Core Network: Standar **90 menit**.
2. **Kalkulasi Sisa Waktu Otomatis oleh Sistem:**
   $$\text{Estimasi Sisa Waktu} = \text{Standar SOP} - (\text{Waktu Sekarang} - \text{Waktu Check-in})$$
3. **Penyederhanaan Aplikasi Mobile Teknisi:**
   Teknisi lapangan hanya melakukan 2 ketukan:
   - **Ketukan 1 (Check-in):** Saat tiba di cabang (mencatat jam mulai otomatis).
   - **Ketukan 2 (Check-out):** Saat perbaikan selesai (upload foto bukti & part pengganti).

---

## 3. Bedah Logika SPK pada Langkah 04 (*The Hero Feature*)

Dosen pembimbing meminta penyelesaian konkret atas dilema:  
> *"Bagaimana menentukan teknisi mana yang dikirim ketika semua teknisi sedang bekerja? Apakah yang dekat tapi sedang menangani kasus berat, atau yang jauh tapi menangani kasus ringan?"*

### Formulasi Kriteria SPK pada Prototype:
1. **Kriteria Jarak Spasial ($C_1$ - Bobot 35%):** Dihitung dari koordinat outlet asal ke outlet tujuan menggunakan **Formula Haversine**.
2. **Kriteria Kesiapan Sisa Waktu ($C_2$ - Bobot 35%):** Makin sedikit estimasi menit tersisa dari pekerjaan lama, makin cepat teknisi siap berangkat.
3. **Kesesuaian Keahlian Hardware/POS ($C_3$ - Bobot 15%):** Teknisi dengan spesialisasi perangkat keras kasir mendapat nilai tambah.
4. **Penalti Biaya Interupsi Tugas Lama ($C_4$ - Bobot Negatif):**  
   - Jika teknisi sedang menangani kasus *Critical* di cabang lama, diberikan penalti berat ($-34$ poin).
   - Jika teknisi sedang menangani kasus *Low*, penalti sangat kecil ($-8.5$ poin).

### Perbandingan Nyata Hasil Perhitungan:
- **Budi Santoso (Ranking 1 - Skor: 79.5):**  
  Berada di *RamenYA Senayan City* (Jarak: 3.2 km, 12 menit). Tugas saat ini adalah *Printer Thermal (SOP 30 mnt)* yang **sudah berjalan 25 menit (Sisa ~5 Menit)**.  
  *Kesimpulan:* Menunggu Budi 5 menit menyelesaikan pekerjaannya lalu meluncur (total tiba ~17 menit) adalah keputusan paling optimal tanpa menimbulkan risiko di Senayan City!
- **Anton Pratama (Ranking 5 - Skor: 48.0):**  
  Berada di *SushiYa PIM* (**Jarak paling dekat: 2.1 km, 8 menit**). **TETAPI** sedang menangani *Server Kasir CRITICAL* yang baru berjalan 20 menit (Sisa ~70 Menit).  
  *Kesimpulan:* Jika Anton dipaksa pindah, gerai PIM terancam tutup operasional dan omzet hilang ganda. Sistem cerdas otomatis menggugurkan Anton dari rekomendasi utama meskipun jaraknya paling dekat!

---

## 4. Cara Menjalankan & Mempresentasikan ke Dosen Pembimbing

1. **Buka Berkas:** Klik dua kali berkas `index.html` atau buka melalui browser apa pun.
2. **Panduan Demo Berurutan:**
   - Mulai dari `01_dashboard_operasional.html` untuk memperlihatkan kondisi riil 6 teknisi sibuk dengan data sisa waktu otomatis.
   - Buka `02_pelaporan_tiket_pic_cabang.html` untuk mensimulasikan laporan kasir mati di jam makan siang.
   - Buka `03_antrean_tiket_it_spv.html` untuk melihat antrean triage SPV.
   - **Tunjukkan `04_spk_rekomendasi_teknisi.html` sebagai bukti implementasi ilmiah peminatan Software Engineering:** Jelaskan tabel perbandingan ranking dan alasan mengapa Budi Santoso terpilih di atas Anton Pratama.
   - Buka `06_mobile_app_teknisi.html` untuk menunjukkan bahwa teknisi lapangan hanya perlu melakukan check-in dan check-out sederhana.
   - Buka `07_verifikasi_resolusi_tiket.html` untuk melihat penutupan tiket secara transparan.
3. **Reset State:** Jika ingin mengulang demonstrasi dari awal, tekan tombol **"🔄 Reset State Prototype"** pada bagian header.
