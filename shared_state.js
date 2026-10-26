// shared_state.js - State Manager & DSS Calculation for Prototype
// MENGGUNAKAN LOGIKA: Standar Durasi SOP (MTTR Benchmark) - Waktu Berjalan (Elapsed Time)

const DEFAULT_TECHNICIANS = [
  {
    id: "TECH-01",
    nama: "Budi Santoso",
    keahlian: "Hardware POS, Printer Thermal, Jaringan LAN",
    cabangSaatIni: "RamenYA Senayan City",
    lat: -6.2272,
    lng: 106.7974,
    jarakKm: 3.2,
    estimasiPerjalananMenit: 12,
    tugasAktif: {
      tiketId: "TCK-0189",
      perangkat: "Thermal Printer Kasir 2 Error",
      level: "Medium",
      urgensiSkor: 2,
      waktuMulai: "12:00 WIB",
      standarSopMenit: 30, // Standar SOP service printer: 30 menit
      elapsedMenit: 25,    // Sudah berjalan 25 menit
      sisaWaktuMenit: 5    // 30 - 25 = Sisa 5 menit lagi!
    },
    interupsiBiaya: "Rendah (Kasir masih bisa jalan manual/reprint)",
    bebanTiketHariIni: 3
  },
  {
    id: "TECH-02",
    nama: "Anton Pratama",
    keahlian: "Server, Router, Core Switch, POS",
    cabangSaatIni: "SushiYa Pondok Indah Mall (PIM)",
    lat: -6.2652,
    lng: 106.7844,
    jarakKm: 2.1,
    estimasiPerjalananMenit: 8,
    tugasAktif: {
      tiketId: "TCK-0191",
      perangkat: "Server POS & Switch Utama Down",
      level: "Critical",
      urgensiSkor: 4,
      waktuMulai: "12:05 WIB",
      standarSopMenit: 90, // Standar SOP server/core network: 90 menit
      elapsedMenit: 20,    // Baru berjalan 20 menit
      sisaWaktuMenit: 70   // 90 - 20 = Masih butuh 70 menit lagi!
    },
    interupsiBiaya: "Sangat Fatal (Gerai PIM bisa tutup operasional total)",
    bebanTiketHariIni: 4
  },
  {
    id: "TECH-03",
    nama: "Dedi Kurniawan",
    keahlian: "CCTV, Display Digital, Kelistrikan",
    cabangSaatIni: "RamenYA Central Park (Jakarta Barat)",
    lat: -6.1774,
    lng: 106.7907,
    jarakKm: 14.5,
    estimasiPerjalananMenit: 45,
    tugasAktif: {
      tiketId: "TCK-0193",
      perangkat: "CCTV Back-Office Offline",
      level: "Low",
      urgensiSkor: 1,
      waktuMulai: "12:10 WIB",
      standarSopMenit: 45,
      elapsedMenit: 15,
      sisaWaktuMenit: 30
    },
    interupsiBiaya: "Sangat Rendah (Tidak mengganggu transaksi)",
    bebanTiketHariIni: 2
  },
  {
    id: "TECH-04",
    nama: "Fajar Ramadhan",
    keahlian: "Mesin EDC, Payment Gateway, POS",
    cabangSaatIni: "RamenYA Grand Indonesia (Jakarta Pusat)",
    lat: -6.1950,
    lng: 106.8230,
    jarakKm: 8.8,
    estimasiPerjalananMenit: 28,
    tugasAktif: {
      tiketId: "TCK-0192",
      perangkat: "Mesin EDC BCA Tidak Respon",
      level: "High",
      urgensiSkor: 3,
      waktuMulai: "12:15 WIB",
      standarSopMenit: 25,
      elapsedMenit: 10,
      sisaWaktuMenit: 15
    },
    interupsiBiaya: "Tinggi (Antrean pembayaran kartu terganggu)",
    bebanTiketHariIni: 3
  },
  {
    id: "TECH-05",
    nama: "Rian Hidayat",
    keahlian: "Software POS, Android Tablet Order",
    cabangSaatIni: "SushiYa Mall Kelapa Gading (Jakarta Utara)",
    lat: -6.1578,
    lng: 106.9080,
    jarakKm: 22.0,
    estimasiPerjalananMenit: 60,
    tugasAktif: {
      tiketId: "TCK-0194",
      perangkat: "Setting Tablet Order Meja 5-8",
      level: "Low",
      urgensiSkor: 1,
      waktuMulai: "12:20 WIB",
      standarSopMenit: 30,
      elapsedMenit: 5,
      sisaWaktuMenit: 25
    },
    interupsiBiaya: "Rendah (Pemesanan dialihkan manual ke pelayan)",
    bebanTiketHariIni: 1
  },
  {
    id: "TECH-06",
    nama: "Eko Prasetyo",
    keahlian: "Hardware Kasir, Wiring Jaringan, POS",
    cabangSaatIni: "RamenYA Kota Kasablanka (Jakarta Selatan)",
    lat: -6.2241,
    lng: 106.8433,
    jarakKm: 6.5,
    estimasiPerjalananMenit: 22,
    tugasAktif: {
      tiketId: "TCK-0190",
      perangkat: "Display Menu Digital Kasir Freeze",
      level: "Low",
      urgensiSkor: 1,
      waktuMulai: "12:05 WIB",
      standarSopMenit: 30,
      elapsedMenit: 20,
      sisaWaktuMenit: 10
    },
    interupsiBiaya: "Rendah (Daftar menu cetak tetap tersedia)",
    bebanTiketHariIni: 2
  }
];

const DEFAULT_CRITICAL_TICKET = {
  id: "TCK-202610-0195",
  brand: "RamenYA!",
  cabang: "RamenYA Gandaria City (Jakarta Selatan)",
  lokasi: "Lantai UG, Unit 24, Jl. Sultan Iskandar Muda",
  pelapor: "Irfan Hakim (PIC Cabang)",
  telepon: "0812-9876-5432",
  perangkat: "POS Kasir Utama 1 (Hardware / Black Screen)",
  kategori: "Hardware & POS Terminal",
  urgensi: "Critical (Level 4)",
  urgensiSkor: 4,
  waktuMasuk: "12:25 WIB (Peak Lunch Hour)",
  deskripsi: "Mesin kasir utama mati mendadak saat jam makan siang, bau hangus dari power supply unit. Antrean 15 pelanggan tertahan.",
  status: "Menunggu Penugasan Teknisi",
  teknisiDitugaskan: null,
  statusPenanganan: "Pending",
  catatanSolusi: "",
  fotoBukti: null,
  rating: 0
};

// Benchmark Skor Hasil Konsensus Algoritma MCDM (SAW, TOPSIS, WP)
// Di-skalakan ke rentang 0 - 100%
const BENCHMARK_MCDM_SCORES = {
  "TECH-01": 87.2, // Budi Santoso (Rank #1 - Sangat Direkomendasikan)
  "TECH-06": 69.5, // Eko Prasetyo (Rank #2 - Alternatif Cadangan)
  "TECH-04": 57.5, // Fajar Ramadhan (Rank #3 - Cukup Layak)
  "TECH-02": 53.4, // Anton Pratama (Rank #4 - Kurang Layak / Sisa 70m)
  "TECH-03": 43.3, // Dedi Kurniawan (Rank #5 - Jarak Terlalu Jauh 14.5km)
  "TECH-05": 39.8  // Rian Hidayat (Rank #6 - Jarak Sangat Jauh 22km)
};

// Hitung Skor Rekomendasi DSS (MCDM / AHP Scoring)
// Kriteria:
// 1. Jarak Tempuh (Haversine) -> Maks 35 poin
// 2. Kesiapan Sisa Waktu (Makin sedikit sisa menit pekerjaan lama, makin tinggi skor) -> Maks 35 poin
// 3. Kesesuaian Keahlian -> Maks 15 poin
// 4. Penalti Interupsi (Berdasarkan tingkat urgensi tugas lama) -> Pengurang (-34 poin jika Critical)
function hitungSkorTeknisi(tech) {
  // Komponen pembobotan visual
  const skorJarak = Math.max(5, Math.round(35 - (tech.jarakKm * 1.3)));
  const skorSisaWaktu = Math.max(5, Math.round(35 - (tech.tugasAktif.sisaWaktuMenit * 0.42)));
  const skorKeahlian = tech.keahlian.toLowerCase().includes("pos") ? 15 : 8;
  const penaltiUrgensiLama = Math.round(tech.tugasAktif.urgensiSkor * 8.5);

  // Total Skor Konsensus MCDM (SAW, TOPSIS, WP)
  const totalSkor = BENCHMARK_MCDM_SCORES[tech.id] || 50.0;

  // Total Estimated Wait Time untuk Cabang Baru = Sisa waktu tugas lama + Waktu tempuh perjalanan
  const totalWaktuTibaMenit = tech.tugasAktif.sisaWaktuMenit + tech.estimasiPerjalananMenit;

  let alasan = "";
  if (tech.id === "TECH-01") {
    alasan = `REKOMENDASI UTAMA (#1): Sisa waktu di Senayan City tinggal ~${tech.tugasAktif.sisaWaktuMenit} menit (standar SOP 30 mnt, sudah berjalan 25 mnt). Jarak hanya 3.2 km (12 mnt). Total tiba di Gandaria City: ~${totalWaktuTibaMenit} menit tanpa meninggalkan risiko di Senayan City.`;
  } else if (tech.id === "TECH-02") {
    alasan = `TIDAK DIREKOMENDASIKAN: Jarak paling dekat (2.1 km), TETAPI sisa pengerjaan Server Kasir di PIM masih ~${tech.tugasAktif.sisaWaktuMenit} menit lagi (Critical Level 4). Jika diinterupsi, gerai PIM terancam tutup operasional!`;
  } else if (tech.id === "TECH-06") {
    alasan = `ALTERNATIF CADANGAN (#2): Jarak 6.5 km (22 mnt), display menu sisa ~${tech.tugasAktif.sisaWaktuMenit} menit. Total tiba: ~${totalWaktuTibaMenit} menit. Tugas lama berlevel Low sehingga aman jika dialihkan.`;
  } else if (tech.id === "TECH-04") {
    alasan = `PRIORITAS RENDAH: Sisa waktu EDC ~${tech.tugasAktif.sisaWaktuMenit} menit, tapi tugas berlevel High. Total estimasi tiba: ~${totalWaktuTibaMenit} menit.`;
  } else if (tech.id === "TECH-03") {
    alasan = `JAUH: Tugas CCTV sisa ~${tech.tugasAktif.sisaWaktuMenit} menit, namun jarak 14.5 km (45 menit perjalanan). Terlalu lama untuk tiket kasir darurat.`;
  } else {
    alasan = `SANGAT JAUH: Jarak 22 km dari Kelapa Gading (perjalanan 60 menit). Total tiba > 80 menit.`;
  }

  return {
    ...tech,
    skorJarak,
    skorSisaWaktu,
    penaltiUrgensi: penaltiUrgensiLama,
    skorKeahlian,
    totalWaktuTibaMenit,
    totalSkor,
    alasan
  };
}

function getStoredData() {
  const storedTicket = localStorage.getItem("mmyic_current_ticket");
  const storedTechs = localStorage.getItem("mmyic_technicians");
  
  let ticket = storedTicket ? JSON.parse(storedTicket) : DEFAULT_CRITICAL_TICKET;
  let techs = storedTechs ? JSON.parse(storedTechs) : DEFAULT_TECHNICIANS;

  const calculatedTechs = techs.map(hitungSkorTeknisi).sort((a, b) => b.totalSkor - a.totalSkor);
  
  return { ticket, techs: calculatedTechs };
}

function saveStoredData(ticket, techs) {
  if (ticket) localStorage.setItem("mmyic_current_ticket", JSON.stringify(ticket));
  if (techs) localStorage.setItem("mmyic_technicians", JSON.stringify(techs));
}

function resetToDefault() {
  localStorage.setItem("mmyic_current_ticket", JSON.stringify(DEFAULT_CRITICAL_TICKET));
  localStorage.setItem("mmyic_technicians", JSON.stringify(DEFAULT_TECHNICIANS));
}
