#!/usr/bin/env python3
"""
Generate docs/presentation/assets/data.js from the cleaned dataset.

Source of truth (read-only, never modified):
  - docs/cleaned_data/cleaned_tickets.csv
  - docs/cleaned_data/ticket_analytics_summary.json

Every number shown in the dashboard is computed here from the 788 real tickets.
Nothing is hardcoded in the HTML. Re-run after cleaning data changes:

    python3 docs/presentation/tools/build_data.py
"""

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]          # docs/
CSV_PATH = ROOT / "cleaned_data" / "cleaned_tickets.csv"
SUMMARY_PATH = ROOT / "cleaned_data" / "ticket_analytics_summary.json"
OUT_PATH = ROOT / "presentation" / "assets" / "data.js"


def fnum(value):
    """Parse a numeric cell, return None when empty/invalid."""
    if value is None:
        return None
    value = str(value).strip()
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def median(values):
    values = sorted(values)
    n = len(values)
    if n == 0:
        return None
    mid = n // 2
    return round(values[mid] if n % 2 else (values[mid - 1] + values[mid]) / 2, 2)


def mean(values):
    return round(sum(values) / len(values), 2) if values else None


def main():
    with CSV_PATH.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))

    summary = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))
    total = len(rows)

    def norm(value):
        return (value or "").strip()

    # ── Attach derived numeric fields ────────────────────────────────────────
    for r in rows:
        r["_hours"] = fnum(r["total_resolution_hours"])
        r["_limit"] = fnum(r["sla_limit_hours"])
        r["_breach"] = norm(r["is_sla_breached"]).upper() == "YES"

    # ── Core distributions ───────────────────────────────────────────────────
    def counter(field, exclude_empty=True):
        c = Counter(norm(r[field]) for r in rows)
        if exclude_empty:
            c.pop("", None)
        return c.most_common()

    priority = [{"key": k, "value": v} for k, v in
                sorted(counter("priority"), key=lambda x: x[0])]
    category = [{"key": k, "value": v} for k, v in
                sorted(counter("category"), key=lambda x: -x[1])]
    layer = [{"key": k, "value": v} for k, v in
             sorted(counter("assigned_layer"), key=lambda x: -x[1])]
    solving = [{"key": k, "value": v} for k, v in
               sorted(counter("solving_method"), key=lambda x: -x[1])]
    status = [{"key": k, "value": v} for k, v in
              sorted(counter("status"), key=lambda x: -x[1])]
    detail = [{"key": k, "value": v} for k, v in counter("category_detail")]
    cities = [{"key": k, "value": v} for k, v in counter("city_region")]

    # ── SLA per priority ────────────────────────────────────────────────────
    sla = []
    for p in ["P1", "P2", "P3", "P4"]:
        info = summary["sla_performance"][p]
        rows_p = [r for r in rows if norm(r["priority"]) == p]
        hours = [r["_hours"] for r in rows_p if r["_hours"] is not None]
        limit = info["sla_limit_hours"]
        within = sum(1 for h in hours if h <= limit)
        sla.append({
            "priority": p,
            "total": len(rows_p),
            "evaluated": info["evaluated"],
            "breached": info["breached"],
            "breach_pct": info["breach_percentage"],
            "avg_hours": info["avg_resolution_hours"],
            "median_hours": median(hours),
            "p90_hours": round(sorted(hours)[int(0.9 * (len(hours) - 1))], 2) if hours else None,
            "limit_hours": limit,
            "within": within,
            "within_pct": round(100 * within / len(hours), 2) if hours else None,
        })

    sla_total_breached = sum(s["breached"] for s in sla)
    sla_total_evaluated = sum(s["evaluated"] for s in sla)

    # ── Technician workload + profile (C2 / C3 / C4 material) ───────────────
    TECH = [k for k, _ in summary["technician_workload"].items()]
    technicians = []
    for name in TECH:
        rs = [r for r in rows if norm(r["assigned_pic"]) == name]
        hours = [r["_hours"] for r in rs if r["_hours"] is not None]
        l2 = sum(1 for r in rs if norm(r["assigned_layer"]) == "Layer 2")
        breached = sum(1 for r in rs if r["_breach"])
        technicians.append({
            "name": name,
            "tickets": len(rs),
            "share_pct": round(100 * len(rs) / total, 2),
            "layer1": len(rs) - l2,
            "layer2": l2,
            "layer2_pct": round(100 * l2 / len(rs), 2) if rs else None,
            "avg_hours": mean(hours),
            "median_hours": median(hours),
            "breached": breached,
            "breach_pct": round(100 * breached / len(hours), 2) if hours else None,
            "categories": [{"key": k, "value": v} for k, v in
                           sorted(Counter(norm(r["category"]) for r in rs).items(),
                                  key=lambda x: -x[1])],
            "methods": [{"key": k, "value": v} for k, v in
                        sorted(Counter(norm(r["solving_method"]) for r in rs).items(),
                               key=lambda x: -x[1]) if k],
            "details": [{"key": k, "value": v} for k, v in
                        Counter(norm(r["category_detail"]) for r in rs).most_common(8) if k],
            "city_top": [{"key": k, "value": v} for k, v in
                         Counter(norm(r["city_region"]) for r in rs).most_common(5) if k],
        })

    workload_values = [t["tickets"] for t in technicians]
    wl_mean = sum(workload_values) / len(workload_values)
    wl_std = (sum((v - wl_mean) ** 2 for v in workload_values) / len(workload_values)) ** 0.5
    # Coefficient of variation = relative spread of the workload (imbalance index)
    workload_cv = round(100 * wl_std / wl_mean, 2)

    # ── Layer 2 real assignment matrix (who is actually SPOF-ish) ───────────
    city_layer2 = Counter(norm(r["city_region"]) for r in rows
                          if norm(r["assigned_layer"]) == "Layer 2")
    pic_city2 = defaultdict(Counter)
    for r in rows:
        if norm(r["assigned_layer"]) == "Layer 2":
            pic_city2[norm(r["assigned_pic"]) or "Unassigned"][norm(r["city_region"])] += 1

    # ── Bottleneck evidence (real free-text notes) ──────────────────────────
    bottlenecks = []
    for r in rows:
        note = norm(r["bottleneck_notes"])
        if not note:
            continue
        bottlenecks.append({
            "ticket": norm(r["ticket_number"]),
            "note": note,
            "city": norm(r["city_region"]),
            "category": norm(r["category_detail"]),
            "priority": norm(r["priority"]),
            "hours": r["_hours"],
            "limit": r["_limit"],
        })
    bottlenecks.sort(key=lambda x: -(x["hours"] or 0))

    hold_rows = [r for r in rows if (fnum(r["hold_hours"]) or 0) > 0]
    hold_breached = sum(1 for r in hold_rows if r["_breach"])

    # ── RAG potential: tickets solved without any on-site visit ─────────────
    RAG_METHODS = {"Remote", "Guide", "Service Mandiri"}
    rag_rows = [r for r in rows if norm(r["solving_method"]) in RAG_METHODS]
    rag_detail = Counter(norm(r["category_detail"]) for r in rag_rows)
    detail_totals = Counter(norm(r["category_detail"]) for r in rows)
    rag_candidates = []
    for name, count in rag_detail.most_common(12):
        if not name:
            continue
        rag_candidates.append({
            "key": name,
            "category": next((norm(r["category"]) for r in rag_rows
                              if norm(r["category_detail"]) == name), ""),
            "without_visit": count,
            "total": detail_totals[name],
            "pct_of_detail": round(100 * count / detail_totals[name], 2),
        })

    # MTTR per solving method (median = representative, mean shown as outlier signal)
    method_stats = []
    by_method = defaultdict(list)
    for r in rows:
        if r["_hours"] is not None and norm(r["solving_method"]):
            by_method[norm(r["solving_method"])].append(r["_hours"])
    for name, values in sorted(by_method.items(), key=lambda x: -len(x[1])):
        method_stats.append({
            "key": name,
            "count": len(values),
            "median_hours": median(values),
            "avg_hours": mean(values),
        })

    # ── Monthly timeline (dates are free-text, parse only well-formed ones) ─
    monthly = Counter()
    for r in rows:
        stamp = norm(r["timestamp"])
        if not stamp:
            continue
        head = stamp.split(" ")[0]
        parts = head.split("/")
        if len(parts) != 3:
            continue
        month, day, year = parts
        if not all(p.isdigit() for p in parts) or len(year) != 4:
            continue
        monthly[f"{year}-{int(month):02d}"] += 1
    timeline = [{"key": k, "value": v} for k, v in sorted(monthly.items())]

    # ── Priority × method matrix ────────────────────────────────────────────
    prio_method = []
    for p in ["P1", "P2", "P3", "P4"]:
        row = {"priority": p}
        for m in ["Remote", "Guide", "Visit", "Service Mandiri",
                  "Internal Request", "Service Vendor", "Kirim Hardware"]:
            row[m] = sum(1 for r in rows
                         if norm(r["priority"]) == p and norm(r["solving_method"]) == m)
        prio_method.append(row)

    data = {
        "generated_from": "docs/cleaned_data/cleaned_tickets.csv",
        "ticket_count": total,
        "kpis": {
            "total": total,
            "resolved": sum(1 for r in rows if norm(r["status"]) == "Resolved"),
            "in_progress": sum(1 for r in rows if norm(r["status"]) == "In Progress"),
            "sla_breached": sla_total_breached,
            "sla_evaluated": sla_total_evaluated,
            "sla_breach_pct": round(100 * sla_total_breached / sla_total_evaluated, 2),
            "remote_pct": round(100 * sum(1 for r in rows
                                          if norm(r["solving_method"]) == "Remote") / total, 2),
            "guide_pct": round(100 * sum(1 for r in rows
                                         if norm(r["solving_method"]) == "Guide") / total, 2),
            "no_visit_pct": round(100 * len(rag_rows) / total, 2),
            "no_visit": len(rag_rows),
            "visit": sum(1 for r in rows if norm(r["solving_method"]) == "Visit"),
            "layer1": sum(1 for r in rows if norm(r["assigned_layer"]) == "Layer 1"),
            "layer2": sum(1 for r in rows if norm(r["assigned_layer"]) == "Layer 2"),
            "hold_tickets": len(hold_rows),
            "hold_breached": hold_breached,
            "workload_mean": round(wl_mean, 2),
            "workload_std": round(wl_std, 2),
            "workload_cv": workload_cv,
            "workload_ratio": round(max(workload_values) / min(workload_values), 2),
        },
        "priority": priority,
        "category": category,
        "layer": layer,
        "solving": solving,
        "status": status,
        "detail": detail,
        "cities": cities,
        "sla": sla,
        "technicians": technicians,
        "city_layer2": [{"key": k, "value": v} for k, v in city_layer2.most_common() if k],
        "pic_city2": {k: [{"key": c, "value": n} for c, n in v.most_common() if c]
                      for k, v in pic_city2.items()},
        "bottlenecks": bottlenecks,
        "rag_candidates": rag_candidates,
        "method_stats": method_stats,
        "timeline": timeline,
        "prio_method": prio_method,
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    OUT_PATH.write_text(
        "/* AUTO-GENERATED by docs/presentation/tools/build_data.py\n"
        "   Source: docs/cleaned_data/cleaned_tickets.csv (788 ticket riil)\n"
        "   Jangan edit manual — jalankan ulang script-nya. */\n"
        f"window.HIMUP_DATA = {payload};\n",
        encoding="utf-8",
    )
    print(f"OK  {OUT_PATH}  ({OUT_PATH.stat().st_size / 1024:.1f} KB)")
    print(f"    tickets={total} breached={sla_total_breached}/{sla_total_evaluated} "
          f"workload_cv={workload_cv}% ratio={round(max(workload_values) / min(workload_values), 2)}x")


if __name__ == "__main__":
    main()