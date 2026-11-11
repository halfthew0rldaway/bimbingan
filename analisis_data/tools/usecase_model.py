#!/usr/bin/env python3
"""
Single source of truth (SSoT) for the AS-IS / TO-BE use-case models.

Every use case, actor, association, bottleneck and its evidence are declared
here ONCE. generate_diagrams.py renders them to SVG, so the diagram can never
drift away from the written thesis text.

Evidence columns are computed from docs/cleaned_data/cleaned_tickets.csv
(788 real tickets). Run tools/verify_usecase_data.py to prove each `evidence`
number still matches the dataset.

Colour convention (matches assets/style.css tokens):
  * Legacy / AS-IS      : red family      (--p1 #dc2626)
  * Bottleneck step     : solid red spine (#dc2626) + pale pin (#fee2e2)
  * Neutral step        : slate          (--line #cbd5e1 / --text-dim #475569)
  * Proposed / TO-BE    : green family    (--ok #16a34a)
  * System actor (auto) : blue family     (--info #2563eb)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

ActorKind = Literal["human", "system"]
Relation = Literal["assoc", "include", "extend"]


@dataclass(frozen=True)
class Actor:
    key: str
    name: str
    role: str
    kind: ActorKind = "human"
    lane: int = 0          # explicit vertical lane on the left rail


@dataclass(frozen=True)
class UseCase:
    key: str
    code: str
    name: str
    actor: str                 # primary actor key
    order: int                 # vertical position (spine order)
    bottleneck: str | None = None   # "B1".."B4" when this step is a bottleneck
    b_title: str = ""               # short bottleneck label
    b_evidence: str = ""            # hard number from the dataset
    b_cause: str = ""               # root cause
    solution: str | None = None     # "S1".."S7" for TO-BE rows
    s_title: str = ""
    s_evidence: str = ""
    # Secondary associations: (actor_key, relation)
    links: tuple[tuple[str, Relation], ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class Model:
    title: str
    boundary_label: str
    actors: tuple[Actor, ...]
    usecases: tuple[UseCase, ...]


# ═════════════════════════════════════════════════════════════════════════════
#  AS-IS — Conventional process (WhatsApp group + manual spreadsheet)
#  4 bottlenecks (B1..B4) are the ones empirically provable from 788 tickets.
# ═════════════════════════════════════════════════════════════════════════════

AS_IS = Model(
    title="USE CASE PROSES KONVENSIONAL (AS-IS)",
    boundary_label="SISTEM KONVENSIONAL: GRUP WHATSAPP & SPREADSHEET MANUAL",
    actors=(
        Actor("staf", "Staf Outlet", "Cabang Pelapor", lane=0),
        Actor("admin", "Admin Helpdesk", "IT Support Coordinator", lane=1),
        Actor("teknisi", "Teknisi Lapangan", "PIC Layer 1 / Layer 2", lane=3),
        Actor("purch", "Purchasing / Central", "Vendor & Logistik Sparepart", lane=5),
    ),
    usecases=(
        UseCase(
            key="uc01", code="UC-01", name="Kirim Laporan via Chat Bebas",
            actor="staf", order=0,
            bottleneck="B1",
            b_title="BOTTLENECK B1 - Laporan Tak Terstruktur & Chat Tenggelam",
            b_evidence="0% field terstruktur (kode aset, kategori, urgensi) dari 788 tiket",
            b_cause="Pesan teks/foto bebas di grup; tertimbun ratusan chat saat jam sibuk.",
            links=(("admin", "assoc"),),
        ),
        UseCase(
            key="uc02", code="UC-02", name="Triage & Baca Chat Manual",
            actor="admin", order=1,
            b_title="",
            links=(("staf", "assoc"),),
        ),
        UseCase(
            key="uc03", code="UC-03", name="Tunjuk Teknisi via Tag (@) Subjektif",
            actor="admin", order=2,
            bottleneck="B2",
            b_title="BOTTLENECK B2 - Disparitas Beban Kerja 7,3x",
            b_evidence="Sony 190 tiket vs Taqiy 26 tiket (Koef. Variasi 41,3%)",
            b_cause="Penunjukan bergantung siapa yang aktif membalas chat, tanpa metrik beban.",
            links=(("teknisi", "assoc"),),
        ),
        UseCase(
            key="uc04", code="UC-04", name="Eksekusi Tangani (Visit / Remote)",
            actor="teknisi", order=3,
            bottleneck="B3",
            b_title="BOTTLENECK B3 - Pelanggaran SLA Tanpa Timer Live",
            b_evidence="119 dari 788 tiket (15,1%) lewat SLA; P2 21,3% (limit 4 jam, aktual 21,2 jam)",
            b_cause="Tidak ada countdown/early-warning; SLA baru dihitung retrospektif di Excel.",
            links=(("admin", "assoc"),),
        ),
        UseCase(
            key="uc05", code="UC-05", name="Tunggu Approval IR / Kirim Sparepart",
            actor="purch", order=4,
            bottleneck="B4",
            b_title="BOTTLENECK B4 - Status Pending Gelap & Penalti SLA Semu",
            b_evidence="77 tiket (9,8%) tertahan; 25.246 jam hold menumpuk (median 9,5 jam, p90 192 jam)",
            b_cause="Menunggu IR purchasing, pengiriman central, atau handoff L1 ke L2 tanpa pencatatan formal.",
            links=(("teknisi", "assoc"),),
        ),
        UseCase(
            key="uc06", code="UC-06", name="Rekapitulasi Manual ke Spreadsheet",
            actor="admin", order=5,
            b_title="",
            b_cause="",
            links=(),
        ),
    ),
)


# ═════════════════════════════════════════════════════════════════════════════
#  TO-BE — Proposed HIMUP Intelligent Web Ticketing
#  S1..S7 map 1:1 onto the AS-IS bottlenecks + the reporting weakness.
# ═════════════════════════════════════════════════════════════════════════════

TO_BE = Model(
    title="USE CASE SISTEM TERUSULKAN (TO-BE)",
    boundary_label="SISTEM TERUSULKAN: HIMUP INTELLIGENT WEB TICKETING",
    actors=(
        Actor("staf", "Staf Outlet", "Cabang Pelapor", lane=0),
        Actor("engine", "Engine Cerdas", "AI RAG & TOPSIS", kind="system", lane=2),
        Actor("teknisi", "Teknisi Lapangan", "PIC Layer 1 / Layer 2", lane=3),
        Actor("purch", "Purchasing / Vendor", "Central Logistics", lane=5),
        Actor("admin", "Admin Helpdesk", "IT Supervisor", lane=6),
    ),
    usecases=(
        UseCase(
            key="uc10", code="UC-10", name="Konsultasi Troubleshooting Mandiri (RAG)",
            actor="staf", order=0,
            solution="S1",
            s_title="SOLUSI S1 - Defleksi AI RAG + Data Terstruktur",
            s_evidence="72,7% tiket selesai tanpa kunjungan; Close Bill (173) & Printer (140) dipandu instan",
            links=(("engine", "include"),),
        ),
        UseCase(
            key="uc11", code="UC-11", name="Buat Tiket Terstruktur + Foto Bukti",
            actor="staf", order=1,
            s_title="SOLUSI S1 - Validasi Form Wajib (Kode Aset, Kategori, Urgensi)",
            s_evidence="Setiap tiket punya MTTA & kategori yang terukur sejak detik nol",
            links=(("engine", "include"),),
        ),
        UseCase(
            key="uc12", code="UC-12", name="Deployment Otomatis Teknisi (TOPSIS)",
            actor="engine", order=2,
            solution="S2",
            s_title="SOLUSI S2 - Workload Balancing 4 Kriteria Objektif",
            s_evidence="Menggantikan penunjukan subjektif; target menekan Koef. Variasi dari 41,3%",
            links=(("admin", "assoc"), ("teknisi", "assoc")),
        ),
        UseCase(
            key="uc13", code="UC-13", name="Pantau Countdown SLA Live + Alert Dini",
            actor="teknisi", order=3,
            solution="S3",
            s_title="SOLUSI S3 - Early Warning System P1-P4",
            s_evidence="Eskalasi otomatis sebelum batas SLA habis; menekan 119 tiket terlambat",
            links=(("admin", "assoc"),),
        ),
        UseCase(
            key="uc14", code="UC-14", name="Freeze Timer SLA Sah (Status On-Hold)",
            actor="teknisi", order=4,
            solution="S4",
            s_title="SOLUSI S4 - Pembekuan Timer untuk Tunggu Pihak Ketiga",
            s_evidence="Memisahkan 25.246 jam hold dari MTTR asli teknisi",
            links=(("purch", "assoc"), ("admin", "assoc")),
        ),
        UseCase(
            key="uc15", code="UC-15", name="Verifikasi Digital & Tutup Tiket",
            actor="teknisi", order=5,
            s_title="SOLUSI S5 - Foto Bukti Resolusi + Konfirmasi Staf Cabang",
            s_evidence="Menutup siklus tiket tanpa rekapitulasi ulang",
            links=(("staf", "assoc"),),
        ),
        UseCase(
            key="uc16", code="UC-16", name="Dashboard Analitik & Eskalasi Real-Time",
            actor="admin", order=6,
            solution="S6",
            s_title="SOLUSI S6 - Telemetri Real-Time, Rekap Excel Dihilangkan",
            s_evidence="Menghapus human error & formula rusak (Err:509) pada sheet manual",
            links=(("purch", "assoc"),),
        ),
    ),
)


# ── Mapping table rendered as the comparison diagram (AS-IS -> TO-BE) ────────
MAPPING = (
    # (as_is_code, as_is_label, bottleneck, to_be_code, to_be_label, resolution)
    ("UC-01", "Chat bebas tanpa format", "B1",
     "UC-10 / UC-11", "Form terstruktur + AI RAG", "Eliminasi B1"),
    ("UC-02", "Triage baca chat manual", "-",
     "UC-12", "Deployment TOPSIS otomatis", "Otomasi"),
    ("UC-03", "Tag (@) teknisi subjektif", "B2",
     "UC-12", "Skor 4 kriteria objektif", "Eliminasi B2"),
    ("UC-04", "Eksekusi tanpa timer SLA", "B3",
     "UC-13", "Countdown SLA + alert dini", "Eliminasi B3"),
    ("UC-05", "Tunggu IR / kirim central", "B4",
     "UC-14", "Freeze timer sah saat on-hold", "Eliminasi B4"),
    ("UC-06", "Rekap manual ke Excel", "-",
     "UC-15 / UC-16", "Verifikasi digital + dashboard", "Otomasi & integrasi"),
)


def bottleneck_count(model: Model) -> int:
    return sum(1 for uc in model.usecases if uc.bottleneck)


def solution_count(model: Model) -> int:
    return sum(1 for uc in model.usecases if uc.solution)