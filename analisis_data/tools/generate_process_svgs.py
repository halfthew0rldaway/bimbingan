#!/usr/bin/env python3
"""
Generate presentation-ready SVG preview files for:
1. docs/presentation/diagrams/conventional-helpdesk-process.svg
2. docs/presentation/diagrams/proposed-helpdesk-process.svg
Matching the PlantUML source files line-by-line.
"""

from pathlib import Path

OUT_DIR = Path("docs/presentation/diagrams")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def build_conventional_svg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 840" width="100%" height="auto"
     role="img" aria-label="Alur Proses Bisnis Helpdesk Konvensional AS-IS"
     style="background:#ffffff; border-radius:12px; border:1px solid #cbd5e1; box-shadow:0 3px 8px rgba(15,23,42,.08)">
  <defs>
    <marker id="arr-red" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#dc2626"/>
    </marker>
    <marker id="arr-orange" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#ea580c"/>
    </marker>
    <marker id="arr-slate" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#475569"/>
    </marker>
  </defs>

  <!-- Title Header -->
  <rect x="0" y="0" width="1100" height="48" fill="#fee2e2" />
  <text x="24" y="25" font-family="Inter, sans-serif" font-size="13.5" font-weight="800" fill="#991b1b">
    ALUR PROSES BISNIS HELPDESK KONVENSIONAL (AS-IS SAAT INI)
  </text>
  <text x="24" y="41" font-family="Inter, sans-serif" font-size="10" font-weight="600" fill="#7f1d1d">
    Identifikasi 5 Titik Kritis Hambatan (Bottleneck) Berdasarkan Analisis 788 Tiket Operasional
  </text>
  <rect x="910" y="12" width="165" height="24" rx="4" fill="#dc2626" />
  <text x="992" y="28" text-anchor="middle" font-family="Inter, sans-serif" font-size="10.5" font-weight="800" fill="#ffffff">
    5 TITIK HAMBATAN
  </text>

  <!-- Swimlane Backgrounds & Headers -->
  <!-- Lane 1 -->
  <rect x="15" y="60" width="255" height="32" rx="4" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1"/>
  <text x="142" y="80" text-anchor="middle" font-family="Inter, sans-serif" font-size="11" font-weight="800" fill="#1e293b">
    1. STAF OUTLET / CABANG
  </text>
  <line x1="15" y1="92" x2="15" y2="730" stroke="#e2e8f0" stroke-width="1"/>
  <line x1="270" y1="92" x2="270" y2="730" stroke="#e2e8f0" stroke-width="1"/>

  <!-- Lane 2 -->
  <rect x="285" y="60" width="255" height="32" rx="4" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1"/>
  <text x="412" y="80" text-anchor="middle" font-family="Inter, sans-serif" font-size="11" font-weight="800" fill="#1e293b">
    2. ADMIN HELPDESK IT
  </text>
  <line x1="540" y1="92" x2="540" y2="730" stroke="#e2e8f0" stroke-width="1"/>

  <!-- Lane 3 -->
  <rect x="555" y="60" width="255" height="32" rx="4" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1"/>
  <text x="682" y="80" text-anchor="middle" font-family="Inter, sans-serif" font-size="11" font-weight="800" fill="#1e293b">
    3. TEKNISI LAPANGAN (L1/L2)
  </text>
  <line x1="810" y1="92" x2="810" y2="730" stroke="#e2e8f0" stroke-width="1"/>

  <!-- Lane 4 -->
  <rect x="825" y="60" width="260" height="32" rx="4" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1"/>
  <text x="955" y="80" text-anchor="middle" font-family="Inter, sans-serif" font-size="11" font-weight="800" fill="#1e293b">
    4. PURCHASING &amp; LOGISTIK
  </text>

  <!-- START NODE -->
  <circle cx="142" cy="115" r="10" fill="#0f172a" />
  <line x1="142" y1="125" x2="142" y2="145" stroke="#475569" stroke-width="1.8" marker-end="url(#arr-slate)"/>

  <!-- STEP 1: Gangguan Terjadi -->
  <g transform="translate(30, 145)">
    <rect width="225" height="52" rx="7" fill="#ffffff" stroke="#64748b" stroke-width="1.5" />
    <text x="112" y="22" text-anchor="middle" font-family="Inter, sans-serif" font-size="10.5" font-weight="700" fill="#0f172a">Gangguan Mesin POS / Jaringan</text>
    <text x="112" y="38" text-anchor="middle" font-family="Inter, sans-serif" font-size="9" fill="#64748b">Operasional kasir restoran terhenti</text>
  </g>

  <line x1="142" y1="197" x2="142" y2="225" stroke="#dc2626" stroke-width="2" marker-end="url(#arr-red)"/>

  <!-- STEP 2: BOTTLENECK 01 (Chat Bebas) -->
  <g transform="translate(25, 225)">
    <rect width="235" height="85" rx="7" fill="#fee2e2" stroke="#dc2626" stroke-width="2.2" />
    <rect x="8" y="7" width="219" height="18" rx="3" fill="#dc2626" />
    <text x="117" y="20" text-anchor="middle" font-family="Inter, sans-serif" font-size="9.5" font-weight="800" fill="#ffffff">🔴 BOTTLENECK 01: CHAT BEBAS</text>
    <text x="117" y="42" text-anchor="middle" font-family="Inter, sans-serif" font-size="10" font-weight="700" fill="#991b1b">Kirim Laporan Teks Bebas di WA</text>
    <text x="117" y="58" text-anchor="middle" font-family="Inter, sans-serif" font-size="8.5" fill="#7f1d1d">Pesan tertimbun saat jam sibuk restoran</text>
    <text x="117" y="72" text-anchor="middle" font-family="Inter, sans-serif" font-size="8.5" fill="#7f1d1d">Tanpa kode aset &amp; waktu respon tak tercatat</text>
  </g>

  <!-- Hand-off Lane 1 to Lane 2 -->
  <path d="M 260 267 L 412 267 L 412 295" fill="none" stroke="#dc2626" stroke-width="2" marker-end="url(#arr-red)"/>

  <!-- STEP 3: Manual Triage (Lane 2) -->
  <g transform="translate(295, 295)">
    <rect width="235" height="60" rx="7" fill="#ffedd5" stroke="#ea580c" stroke-width="1.8" />
    <rect x="8" y="6" width="219" height="16" rx="3" fill="#ea580c" />
    <text x="117" y="18" text-anchor="middle" font-family="Inter, sans-serif" font-size="9" font-weight="800" fill="#ffffff">KOORDINASI MANUAL (WAITING)</text>
    <text x="117" y="38" text-anchor="middle" font-family="Inter, sans-serif" font-size="10" font-weight="700" fill="#9a3412">Admin Triage Pesan Chat WA</text>
    <text x="117" y="52" text-anchor="middle" font-family="Inter, sans-serif" font-size="8.5" fill="#7c2d12">Waktu respon bergantung admin membaca chat</text>
  </g>

  <line x1="412" y1="355" x2="412" y2="385" stroke="#dc2626" stroke-width="2.5" marker-end="url(#arr-red)"/>

  <!-- STEP 4: BOTTLENECK 02 (Penugasan Subjektif) -->
  <g transform="translate(295, 385)">
    <rect width="235" height="85" rx="7" fill="#fee2e2" stroke="#dc2626" stroke-width="2.2" />
    <rect x="8" y="7" width="219" height="18" rx="3" fill="#dc2626" />
    <text x="117" y="20" text-anchor="middle" font-family="Inter, sans-serif" font-size="9.5" font-weight="800" fill="#ffffff">🔴 BOTTLENECK 02: BEBAN TIMPANG 7.3×</text>
    <text x="117" y="42" text-anchor="middle" font-family="Inter, sans-serif" font-size="10" font-weight="700" fill="#991b1b">Tag (@) Teknisi Subjektif di Grup</text>
    <text x="117" y="58" text-anchor="middle" font-family="Inter, sans-serif" font-size="8.5" fill="#7f1d1d">Tanpa melihat antrean beban aktif</text>
    <text x="117" y="72" text-anchor="middle" font-family="Inter, sans-serif" font-size="8.5" font-weight="700" fill="#b91c1c">Sony 190 tiket vs Taqiy hanya 26 tiket</text>
  </g>

  <!-- Hand-off Lane 2 to Lane 3 -->
  <path d="M 530 427 L 682 427 L 682 225" fill="none" stroke="#dc2626" stroke-width="2" marker-end="url(#arr-red)"/>

  <!-- STEP 5: BOTTLENECK 03 (Tanpa Timer SLA) (Lane 3) -->
  <g transform="translate(565, 225)">
    <rect width="235" height="85" rx="7" fill="#fee2e2" stroke="#dc2626" stroke-width="2.2" />
    <rect x="8" y="7" width="219" height="18" rx="3" fill="#dc2626" />
    <text x="117" y="20" text-anchor="middle" font-family="Inter, sans-serif" font-size="9.5" font-weight="800" fill="#ffffff">🔴 BOTTLENECK 03: TANPA SLA TIMER</text>
    <text x="117" y="42" text-anchor="middle" font-family="Inter, sans-serif" font-size="10" font-weight="700" fill="#991b1b">Penanganan Remote / Kunjungan</text>
    <text x="117" y="58" text-anchor="middle" font-family="Inter, sans-serif" font-size="8.5" fill="#7f1d1d">Tidak ada indikator live sisa batas waktu</text>
    <text x="117" y="72" text-anchor="middle" font-family="Inter, sans-serif" font-size="8.5" font-weight="700" fill="#b91c1c">23.4% Tiket P2 molor rata-rata 21.2 jam</text>
  </g>

  <line x1="682" y1="310" x2="682" y2="340" stroke="#475569" stroke-width="1.8" marker-end="url(#arr-slate)"/>

  <!-- Decision: Butuh Part? (Lane 3) -->
  <g transform="translate(682, 365)">
    <polygon points="0,-24 45,0 0,24 -45,0" fill="#f8fafc" stroke="#475569" stroke-width="2"/>
    <text x="0" y="4" text-anchor="middle" font-family="Inter, sans-serif" font-size="9" font-weight="800" fill="#0f172a">Butuh Part?</text>
  </g>

  <!-- Branch: YA to Lane 4 -->
  <path d="M 727 365 L 835 365" fill="none" stroke="#dc2626" stroke-width="2" marker-end="url(#arr-red)"/>
  <text x="765" y="357" font-family="Inter, sans-serif" font-size="9" font-weight="800" fill="#dc2626">YA</text>

  <!-- STEP 6: BOTTLENECK 04 (Status Mengambang) (Lane 4) -->
  <g transform="translate(835, 325)">
    <rect width="245" height="90" rx="7" fill="#fee2e2" stroke="#dc2626" stroke-width="2.2" />
    <rect x="8" y="7" width="229" height="18" rx="3" fill="#dc2626" />
    <text x="122" y="20" text-anchor="middle" font-family="Inter, sans-serif" font-size="9.5" font-weight="800" fill="#ffffff">🔴 BOTTLENECK 04: STATUS MENGAMBANG</text>
    <text x="122" y="42" text-anchor="middle" font-family="Inter, sans-serif" font-size="10" font-weight="700" fill="#991b1b">Menunggu Approval IR &amp; Pengiriman</text>
    <text x="122" y="58" text-anchor="middle" font-family="Inter, sans-serif" font-size="8.5" fill="#7f1d1d">Timer SLA terus berjalan semu (5-14 hari)</text>
    <text x="122" y="74" text-anchor="middle" font-family="Inter, sans-serif" font-size="8.5" font-weight="700" fill="#b91c1c">77 tiket tertunda &amp; penalti SLA semu</text>
  </g>

  <!-- Return from Lane 4 to Lane 3 -->
  <path d="M 957 415 L 957 465 L 682 465 L 682 495" fill="none" stroke="#ea580c" stroke-width="2" marker-end="url(#arr-orange)"/>
  <text x="825" y="460" text-anchor="middle" font-family="Inter, sans-serif" font-size="8.5" fill="#9a3412">Part tiba &gt;&gt; pasang ke mesin kasir</text>

  <!-- Branch: TIDAK from decision -->
  <line x1="637" y1="365" x2="600" y2="365" stroke="#475569" stroke-width="1.8"/>
  <path d="M 600 365 L 600 495 L 682 495" fill="none" stroke="#475569" stroke-width="1.8"/>
  <text x="612" y="357" font-family="Inter, sans-serif" font-size="9" font-weight="800" fill="#475569">TIDAK</text>

  <!-- STEP 7: Selesai Konfirmasi Lisan (Lane 3) -->
  <g transform="translate(565, 495)">
    <rect width="235" height="48" rx="7" fill="#ffffff" stroke="#64748b" stroke-width="1.5" />
    <text x="117" y="20" text-anchor="middle" font-family="Inter, sans-serif" font-size="10" font-weight="700" fill="#0f172a">Konfirmasi Lisan di Chat WhatsApp</text>
    <text x="117" y="36" text-anchor="middle" font-family="Inter, sans-serif" font-size="8.5" fill="#64748b">Teknisi mengabarkan kasus "Done"</text>
  </g>

  <!-- Hand-off Lane 3 to Lane 2 for monthly recap -->
  <path d="M 565 519 L 412 519 L 412 560" fill="none" stroke="#dc2626" stroke-width="2.5" marker-end="url(#arr-red)"/>

  <!-- STEP 8: BOTTLENECK 05 (Rekap Excel Manual) (Lane 2) -->
  <g transform="translate(295, 560)">
    <rect width="235" height="85" rx="7" fill="#fee2e2" stroke="#dc2626" stroke-width="2.2" />
    <rect x="8" y="7" width="219" height="18" rx="3" fill="#dc2626" />
    <text x="117" y="20" text-anchor="middle" font-family="Inter, sans-serif" font-size="9.5" font-weight="800" fill="#ffffff">🔴 BOTTLENECK 05: REKAP EXCEL MANUAL</text>
    <text x="117" y="42" text-anchor="middle" font-family="Inter, sans-serif" font-size="10" font-weight="700" fill="#991b1b">Salin Chat WA ke Spreadsheet Bulanan</text>
    <text x="117" y="58" text-anchor="middle" font-family="Inter, sans-serif" font-size="8.5" fill="#7f1d1d">Rawan duplikasi baris &amp; formula error (Err:509)</text>
    <text x="117" y="72" text-anchor="middle" font-family="Inter, sans-serif" font-size="8.5" font-weight="700" fill="#b91c1c">Manajemen tanpa telemetri real-time</text>
  </g>

  <!-- STOP NODE -->
  <line x1="412" y1="645" x2="412" y2="675" stroke="#475569" stroke-width="1.8" marker-end="url(#arr-slate)"/>
  <circle cx="412" cy="690" r="14" fill="#ffffff" stroke="#0f172a" stroke-width="3"/>
  <circle cx="412" cy="690" r="8" fill="#0f172a"/>

  <!-- LEGEND BOX (Bottom Right) -->
  <g transform="translate(565, 600)">
    <rect width="515" height="120" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2" />
    <text x="16" y="22" font-family="Inter, sans-serif" font-size="11" font-weight="800" fill="#0f172a">LEGENDA &amp; SIMBOL ALUR KONVENSIONAL:</text>
    
    <rect x="16" y="32" width="18" height="12" rx="2" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
    <text x="42" y="42" font-family="Inter, sans-serif" font-size="10" font-weight="700" fill="#991b1b">Garis Merah Bold:</text>
    <text x="155" y="42" font-family="Inter, sans-serif" font-size="9.5" fill="#334155">Titik Hambatan Kritis (Bottleneck) — Menyebabkan chat tertimbun, overwork, &amp; SLA breach</text>

    <rect x="16" y="56" width="18" height="12" rx="2" fill="#ffedd5" stroke="#ea580c" stroke-width="1.8"/>
    <text x="42" y="66" font-family="Inter, sans-serif" font-size="10" font-weight="700" fill="#9a3412">Garis Oranye:</text>
    <text x="155" y="66" font-family="Inter, sans-serif" font-size="9.5" fill="#334155">Waktu Tunggu &amp; Koordinasi Manual — Menunggu admin membaca chat / kurir sparepart</text>

    <rect x="16" y="80" width="18" height="12" rx="2" fill="#ffffff" stroke="#64748b" stroke-width="1.5"/>
    <text x="42" y="90" font-family="Inter, sans-serif" font-size="10" font-weight="700" fill="#334155">Garis Abu-abu:</text>
    <text x="155" y="90" font-family="Inter, sans-serif" font-size="9.5" fill="#334155">Aktivitas Operasional Standar</text>

    <text x="16" y="110" font-family="Inter, sans-serif" font-size="8.5" font-weight="600" fill="#64748b">
      Sumber Data: Analisis 788 tiket operasional IT Support Helpdesk (docs/cleaned_data/cleaned_tickets.csv)
    </text>
  </g>
</svg>'''

def build_proposed_svg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1150 860" width="100%" height="auto"
     role="img" aria-label="Alur Proses Bisnis Helpdesk Terusulkan TO-BE"
     style="background:#ffffff; border-radius:12px; border:1px solid #cbd5e1; box-shadow:0 3px 8px rgba(15,23,42,.08)">
  <defs>
    <marker id="arr-green" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#16a34a"/>
    </marker>
    <marker id="arr-blue" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#2563eb"/>
    </marker>
    <marker id="arr-slate2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#475569"/>
    </marker>
  </defs>

  <!-- Title Header -->
  <rect x="0" y="0" width="1150" height="48" fill="#dcfce7" />
  <text x="24" y="25" font-family="Inter, sans-serif" font-size="13.5" font-weight="800" fill="#14532d">
    ALUR PROSES BISNIS HELPDESK TERUSULKAN (TO-BE SISTEM HELPDESK WEB)
  </text>
  <text x="24" y="41" font-family="Inter, sans-serif" font-size="10" font-weight="600" fill="#166534">
    Otomasi Penugasan Multi-Kriteria (TOPSIS), Countdown SLA Live, dan Pembekuan Timer On-Hold
  </text>
  <rect x="940" y="12" width="185" height="24" rx="4" fill="#16a34a" />
  <text x="1032" y="28" text-anchor="middle" font-family="Inter, sans-serif" font-size="10.5" font-weight="800" fill="#ffffff">
    SOLUSI TERINTEGRASI
  </text>

  <!-- Swimlane Headers -->
  <!-- Lane 1: Outlet -->
  <rect x="15" y="60" width="215" height="32" rx="4" fill="#f8fafc" stroke="#bbf7d0" stroke-width="1"/>
  <text x="122" y="80" text-anchor="middle" font-family="Inter, sans-serif" font-size="10.5" font-weight="800" fill="#166534">
    1. STAF OUTLET CABANG
  </text>
  <line x1="230" y1="92" x2="230" y2="745" stroke="#e2e8f0" stroke-width="1"/>

  <!-- Lane 2: System Engine -->
  <rect x="240" y="60" width="225" height="32" rx="4" fill="#eff6ff" stroke="#bfdbfe" stroke-width="1"/>
  <text x="352" y="80" text-anchor="middle" font-family="Inter, sans-serif" font-size="10.5" font-weight="800" fill="#1e40af">
    2. ENGINE SISTEM HELPDESK
  </text>
  <line x1="465" y1="92" x2="465" y2="745" stroke="#e2e8f0" stroke-width="1"/>

  <!-- Lane 3: Admin -->
  <rect x="475" y="60" width="215" height="32" rx="4" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1"/>
  <text x="582" y="80" text-anchor="middle" font-family="Inter, sans-serif" font-size="10.5" font-weight="800" fill="#1e293b">
    3. ADMIN HELPDESK IT
  </text>
  <line x1="690" y1="92" x2="690" y2="745" stroke="#e2e8f0" stroke-width="1"/>

  <!-- Lane 4: Technician -->
  <rect x="700" y="60" width="215" height="32" rx="4" fill="#f8fafc" stroke="#bbf7d0" stroke-width="1"/>
  <text x="807" y="80" text-anchor="middle" font-family="Inter, sans-serif" font-size="10.5" font-weight="800" fill="#166534">
    4. TEKNISI LAPANGAN
  </text>
  <line x1="915" y1="92" x2="915" y2="745" stroke="#e2e8f0" stroke-width="1"/>

  <!-- Lane 5: Purchasing -->
  <rect x="925" y="60" width="210" height="32" rx="4" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1"/>
  <text x="1030" y="80" text-anchor="middle" font-family="Inter, sans-serif" font-size="10.5" font-weight="800" fill="#1e293b">
    5. PURCHASING / LOGISTIK
  </text>

  <!-- START NODE -->
  <circle cx="122" cy="115" r="10" fill="#0f172a" />
  <line x1="122" y1="125" x2="122" y2="145" stroke="#475569" stroke-width="1.8" marker-end="url(#arr-slate2)"/>

  <!-- STEP 1: Solusi 01 RAG (Lane 1) -->
  <g transform="translate(25, 145)">
    <rect width="195" height="85" rx="7" fill="#dcfce7" stroke="#16a34a" stroke-width="2.2" />
    <rect x="8" y="7" width="179" height="18" rx="3" fill="#16a34a" />
    <text x="97" y="20" text-anchor="middle" font-family="Inter, sans-serif" font-size="9" font-weight="800" fill="#ffffff">🟢 SOLUSI 01: CHATBOT RAG</text>
    <text x="97" y="42" text-anchor="middle" font-family="Inter, sans-serif" font-size="9.5" font-weight="700" fill="#14532d">Konsultasi Mandiri Cepat</text>
    <text x="97" y="58" text-anchor="middle" font-family="Inter, sans-serif" font-size="8.5" fill="#166534">Panduan SOP Printer / POS instan</text>
    <text x="97" y="72" text-anchor="middle" font-family="Inter, sans-serif" font-size="8.5" font-weight="700" fill="#15803d">Defleksi 39% tiket berulang</text>
  </g>

  <line x1="122" y1="230" x2="122" y2="255" stroke="#16a34a" stroke-width="2" marker-end="url(#arr-green)"/>

  <!-- Decision: Selesai di RAG? -->
  <g transform="translate(122, 275)">
    <polygon points="0,-20 40,0 0,20 -40,0" fill="#ffffff" stroke="#16a34a" stroke-width="2"/>
    <text x="0" y="4" text-anchor="middle" font-family="Inter, sans-serif" font-size="8.5" font-weight="800" fill="#14532d">Tuntas?</text>
  </g>

  <!-- YA -> Finish RAG -->
  <line x1="162" y1="275" x2="200" y2="275" stroke="#16a34a" stroke-width="1.8"/>
  <path d="M 200 275 L 200 310" fill="none" stroke="#16a34a" stroke-width="1.8" marker-end="url(#arr-green)"/>
  <text x="175" y="268" font-family="Inter, sans-serif" font-size="8.5" font-weight="800" fill="#16a34a">YA</text>

  <g transform="translate(140, 310)">
    <rect width="120" height="35" rx="5" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.2"/>
    <text x="60" y="16" text-anchor="middle" font-family="Inter, sans-serif" font-size="8.5" font-weight="700" fill="#15803d">Selesai Tanpa Tiket</text>
    <text x="60" y="28" text-anchor="middle" font-family="Inter, sans-serif" font-size="8" fill="#166534">Log defleksi tersimpan</text>
  </g>

  <!-- TIDAK -> Step 2 Form Lapor (Lane 1) -->
  <line x1="122" y1="295" x2="122" y2="365" stroke="#475569" stroke-width="1.8" marker-end="url(#arr-slate2)"/>
  <text x="130" y="325" font-family="Inter, sans-serif" font-size="8.5" font-weight="800" fill="#475569">TIDAK</text>

  <!-- STEP 2: Solusi 02 Form Terstruktur (Lane 1) -->
  <g transform="translate(25, 365)">
    <rect width="195" height="80" rx="7" fill="#dcfce7" stroke="#16a34a" stroke-width="2.2" />
    <rect x="8" y="7" width="179" height="18" rx="3" fill="#16a34a" />
    <text x="97" y="20" text-anchor="middle" font-family="Inter, sans-serif" font-size="9" font-weight="800" fill="#ffffff">🟢 SOLUSI 02: FORM TERSTRUKTUR</text>
    <text x="97" y="42" text-anchor="middle" font-family="Inter, sans-serif" font-size="9.5" font-weight="700" fill="#14532d">Buat Tiket di Portal Web</text>
    <text x="97" y="56" text-anchor="middle" font-family="Inter, sans-serif" font-size="8.5" fill="#166534">Wajib kode aset, kategori, &amp; foto</text>
    <text x="97" y="70" text-anchor="middle" font-family="Inter, sans-serif" font-size="8.5" font-weight="700" fill="#15803d">Bebas chat tenggelam di WA</text>
  </g>

  <!-- Hand-off Lane 1 to Lane 2 Engine -->
  <path d="M 220 405 L 352 405 L 352 235" fill="none" stroke="#2563eb" stroke-width="2" marker-end="url(#arr-blue)"/>

  <!-- STEP 3: Solusi 03 TOPSIS (Lane 2) -->
  <g transform="translate(250, 235)">
    <rect width="205" height="95" rx="7" fill="#eff6ff" stroke="#2563eb" stroke-width="2.2" />
    <rect x="8" y="7" width="189" height="18" rx="3" fill="#2563eb" />
    <text x="102" y="20" text-anchor="middle" font-family="Inter, sans-serif" font-size="9" font-weight="800" fill="#ffffff">🟢 SOLUSI 03: PENUGASAN TOPSIS</text>
    <text x="102" y="42" text-anchor="middle" font-family="Inter, sans-serif" font-size="9.5" font-weight="700" fill="#1e40af">Kalkulasi 4 Kriteria Objektif</text>
    <text x="102" y="58" text-anchor="middle" font-family="Inter, sans-serif" font-size="8.5" fill="#1e3a8a">Jarak (C1), Beban (C2), Skill (C3), MTTR (C4)</text>
    <text x="102" y="72" text-anchor="middle" font-family="Inter, sans-serif" font-size="8.5" fill="#1e3a8a">Alokasi beban rata (bebas bias 7.3×)</text>
    <text x="102" y="86" text-anchor="middle" font-family="Inter, sans-serif" font-size="8.5" font-weight="700" fill="#2563eb">Timer MTTA mulai berjalan live</text>
  </g>

  <!-- Hand-off to Admin / Supervisor (Lane 3) -->
  <line x1="455" y1="282" x2="485" y2="282" stroke="#475569" stroke-width="1.8" marker-end="url(#arr-slate2)"/>

  <!-- Admin confirms (Lane 3) -->
  <g transform="translate(485, 260)">
    <rect width="195" height="45" rx="7" fill="#ffffff" stroke="#64748b" stroke-width="1.5" />
    <text x="97" y="20" text-anchor="middle" font-family="Inter, sans-serif" font-size="9.5" font-weight="700" fill="#0f172a">Admin Konfirmasi Penugasan</text>
    <text x="97" y="34" text-anchor="middle" font-family="Inter, sans-serif" font-size="8.5" fill="#64748b">Tiket otomatis ter-dispatch</text>
  </g>

  <!-- Hand-off to Technician (Lane 4) -->
  <path d="M 680 282 L 807 282 L 807 335" fill="none" stroke="#16a34a" stroke-width="2" marker-end="url(#arr-green)"/>

  <!-- STEP 4: Solusi 04 Countdown SLA Live (Lane 4) -->
  <g transform="translate(710, 335)">
    <rect width="195" height="85" rx="7" fill="#dcfce7" stroke="#16a34a" stroke-width="2.2" />
    <rect x="8" y="7" width="179" height="18" rx="3" fill="#16a34a" />
    <text x="97" y="20" text-anchor="middle" font-family="Inter, sans-serif" font-size="9" font-weight="800" fill="#ffffff">🟢 SOLUSI 04: COUNTDOWN SLA LIVE</text>
    <text x="97" y="42" text-anchor="middle" font-family="Inter, sans-serif" font-size="9.5" font-weight="700" fill="#14532d">Penanganan Terpantau Real-Time</text>
    <text x="97" y="58" text-anchor="middle" font-family="Inter, sans-serif" font-size="8.5" fill="#166534">Timer mundur (Hijau, Kuning, Merah)</text>
    <text x="97" y="72" text-anchor="middle" font-family="Inter, sans-serif" font-size="8.5" font-weight="700" fill="#15803d">Early warning alert sebelum 4 jam habis</text>
  </g>

  <line x1="807" y1="420" x2="807" y2="450" stroke="#475569" stroke-width="1.8" marker-end="url(#arr-slate2)"/>

  <!-- Decision: Butuh Part? (Lane 4) -->
  <g transform="translate(807, 470)">
    <polygon points="0,-20 40,0 0,20 -40,0" fill="#ffffff" stroke="#475569" stroke-width="2"/>
    <text x="0" y="4" text-anchor="middle" font-family="Inter, sans-serif" font-size="8.5" font-weight="800" fill="#0f172a">Butuh Part?</text>
  </g>

  <!-- YA -> Lane 5 & Freeze SLA -->
  <line x1="847" y1="470" x2="935" y2="470" stroke="#2563eb" stroke-width="2" marker-end="url(#arr-blue)"/>
  <text x="880" y="462" font-family="Inter, sans-serif" font-size="8.5" font-weight="800" fill="#2563eb">YA</text>

  <!-- STEP 5: Solusi 05 On-Hold Freeze SLA (Lane 5) -->
  <g transform="translate(935, 430)">
    <rect width="195" height="90" rx="7" fill="#eff6ff" stroke="#2563eb" stroke-width="2.2" />
    <rect x="8" y="7" width="179" height="18" rx="3" fill="#2563eb" />
    <text x="97" y="20" text-anchor="middle" font-family="Inter, sans-serif" font-size="9" font-weight="800" fill="#ffffff">🟢 SOLUSI 05: ON-HOLD FREEZE SLA</text>
    <text x="97" y="42" text-anchor="middle" font-family="Inter, sans-serif" font-size="9.5" font-weight="700" fill="#1e40af">Pause Timer Saat Tunggu IR</text>
    <text x="97" y="58" text-anchor="middle" font-family="Inter, sans-serif" font-size="8.5" fill="#1e3a8a">Timer SLA dihentikan sah di sistem</text>
    <text x="97" y="72" text-anchor="middle" font-family="Inter, sans-serif" font-size="8.5" font-weight="700" fill="#2563eb">KPI teknisi aman dari delay purchasing</text>
  </g>

  <!-- Part Arrives & Resume SLA -->
  <path d="M 1032 520 L 1032 570 L 807 570 L 807 600" fill="none" stroke="#16a34a" stroke-width="2" marker-end="url(#arr-green)"/>
  <text x="920" y="563" text-anchor="middle" font-family="Inter, sans-serif" font-size="8.5" fill="#15803d">Part tiba &gt;&gt; Resume Timer &amp; pasang perangkat</text>

  <!-- TIDAK -> Perbaikan Selesai -->
  <line x1="767" y1="470" x2="735" y2="470" stroke="#475569" stroke-width="1.8"/>
  <path d="M 735 470 L 735 600 L 807 600" fill="none" stroke="#475569" stroke-width="1.8"/>
  <text x="745" y="462" font-family="Inter, sans-serif" font-size="8.5" font-weight="800" fill="#475569">TIDAK</text>

  <!-- STEP 6: Upload Bukti & Selesai (Lane 4) -->
  <g transform="translate(710, 600)">
    <rect width="195" height="48" rx="7" fill="#ffffff" stroke="#16a34a" stroke-width="1.8" />
    <text x="97" y="20" text-anchor="middle" font-family="Inter, sans-serif" font-size="9.5" font-weight="700" fill="#14532d">Upload Bukti &amp; Selesaikan</text>
    <text x="97" y="34" text-anchor="middle" font-family="Inter, sans-serif" font-size="8.5" fill="#475569">Lampirkan foto fisik hasil perbaikan</text>
  </g>

  <!-- Verification Hand-off to Outlet (Lane 1) -->
  <path d="M 710 624 L 122 624 L 122 655" fill="none" stroke="#16a34a" stroke-width="2" marker-end="url(#arr-green)"/>

  <!-- STEP 7: Verifikasi Outlet Cabang (Lane 1) -->
  <g transform="translate(25, 655)">
    <rect width="195" height="48" rx="7" fill="#ffffff" stroke="#16a34a" stroke-width="1.8" />
    <text x="97" y="20" text-anchor="middle" font-family="Inter, sans-serif" font-size="9.5" font-weight="700" fill="#14532d">Verifikasi Digital Staf Cabang</text>
    <text x="97" y="34" text-anchor="middle" font-family="Inter, sans-serif" font-size="8.5" fill="#475569">Konfirmasi mesin kasir beroperasi normal</text>
  </g>

  <!-- Hand-off to System Telemetry (Lane 2) -->
  <path d="M 220 679 L 250 679" fill="none" stroke="#2563eb" stroke-width="2" marker-end="url(#arr-blue)"/>

  <!-- STEP 8: Solusi 06 Telemetri Real-Time (Lane 2) -->
  <g transform="translate(250, 640)">
    <rect width="205" height="85" rx="7" fill="#eff6ff" stroke="#2563eb" stroke-width="2.2" />
    <rect x="8" y="7" width="189" height="18" rx="3" fill="#2563eb" />
    <text x="102" y="20" text-anchor="middle" font-family="Inter, sans-serif" font-size="9" font-weight="800" fill="#ffffff">🟢 SOLUSI 06: LAPORAN REAL-TIME</text>
    <text x="102" y="42" text-anchor="middle" font-family="Inter, sans-serif" font-size="9.5" font-weight="700" fill="#1e40af">Telemetri Otomatis Terbit</text>
    <text x="102" y="58" text-anchor="middle" font-family="Inter, sans-serif" font-size="8.5" fill="#1e3a8a">Status tiket "Closed" &amp; rekam MTTR final</text>
    <text x="102" y="72" text-anchor="middle" font-family="Inter, sans-serif" font-size="8.5" font-weight="700" fill="#2563eb">100% Bebas rekapitulasi manual Excel</text>
  </g>

  <!-- STOP NODE -->
  <line x1="352" y1="725" x2="352" y2="760" stroke="#475569" stroke-width="1.8" marker-end="url(#arr-slate2)"/>
  <circle cx="352" cy="775" r="14" fill="#ffffff" stroke="#16a34a" stroke-width="3"/>
  <circle cx="352" cy="775" r="8" fill="#16a34a"/>

  <!-- LEGEND BOX (Bottom Right) -->
  <g transform="translate(565, 715)">
    <rect width="570" height="110" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2" />
    <text x="16" y="20" font-family="Inter, sans-serif" font-size="11" font-weight="800" fill="#0f172a">LEGENDA &amp; SIMBOL ALUR TERUSULKAN:</text>
    
    <rect x="16" y="30" width="18" height="12" rx="2" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>
    <text x="42" y="40" font-family="Inter, sans-serif" font-size="10" font-weight="700" fill="#14532d">Garis Hijau Bold:</text>
    <text x="150" y="40" font-family="Inter, sans-serif" font-size="9.5" fill="#334155">Solusi Terintegrasi — Chatbot RAG, Form terstruktur, Countdown SLA, &amp; Verifikasi digital</text>

    <rect x="16" y="52" width="18" height="12" rx="2" fill="#eff6ff" stroke="#2563eb" stroke-width="1.8"/>
    <text x="42" y="62" font-family="Inter, sans-serif" font-size="10" font-weight="700" fill="#1e40af">Garis Biru Bold:</text>
    <text x="150" y="62" font-family="Inter, sans-serif" font-size="9.5" fill="#334155">Otomasi Engine Sistem — Perhitungan TOPSIS, Pembekuan timer On-Hold, &amp; Telemetri otomatis</text>

    <rect x="16" y="74" width="18" height="12" rx="2" fill="#ffffff" stroke="#64748b" stroke-width="1.5"/>
    <text x="42" y="84" font-family="Inter, sans-serif" font-size="10" font-weight="700" fill="#334155">Garis Abu-abu:</text>
    <text x="150" y="84" font-family="Inter, sans-serif" font-size="9.5" fill="#334155">Aktivitas Koordinasi Standar Lintas Peran</text>
  </g>
</svg>'''

if __name__ == "__main__":
    (OUT_DIR / "conventional-helpdesk-process.svg").write_text(build_conventional_svg(), encoding="utf-8")
    (OUT_DIR / "proposed-helpdesk-process.svg").write_text(build_proposed_svg(), encoding="utf-8")
    print("Exported SVGs successfully created in", OUT_DIR)
