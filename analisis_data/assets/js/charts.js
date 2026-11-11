/* ==========================================================================
   HIMUP Ticketing — charts.js
   Modern Data Visualization System (Clean, High-Contrast, No Clutter)
   - Zero crooked leader lines on donuts (clean center metric + modern legends)
   - Refined background tracks on bar charts for polished UI look
   - Distinct, accessible color palette (P1: Red, P2: Orange, P3: Royal Blue, P4: Green)
   ========================================================================== */

(function () {
    'use strict';

    window.HIMUP_CHARTS = function () {
        const H = window.HIMUP;
        if (!H || !H.D) return;

        const { D, K, C, make, fmt, dur, tip, axisCommon, PALETTE, PRIO_COLOR } = H;

        // ── 1. Category Distribution (Progress-Gauge Style) ───────────────────
        make('chart-category', {
            tooltip: {
                ...tip(),
                formatter: (p) => `<b>${p.name}</b><br/>Jumlah Tiket: <b>${p.value}</b> (${fmt((p.value / K.total) * 100, 1)}%)`,
            },
            grid: { left: 135, right: 55, top: 12, bottom: 20 },
            xAxis: { ...axisCommon, type: 'value' },
            yAxis: {
                ...axisCommon,
                type: 'category',
                data: D.category.map((c) => c.key),
                axisLabel: { ...axisCommon.axisLabel, fontSize: 11.5, color: '#1e293b', fontWeight: '600' },
            },
            series: [{
                type: 'bar',
                showBackground: true,
                backgroundStyle: { color: '#e2e8f0', borderRadius: [0, 6, 6, 0] },
                data: D.category.map((c, i) => ({
                    value: c.value,
                    itemStyle: {
                        color: PALETTE[i % PALETTE.length],
                        borderRadius: [0, 6, 6, 0],
                    },
                })),
                barWidth: 14,
                label: {
                    show: true,
                    position: 'right',
                    color: '#334155',
                    fontSize: 11,
                    fontWeight: '700',
                    formatter: (p) => `${p.value} (${fmt((p.value / K.total) * 100, 1)}%)`,
                },
            }],
        });

        // ── 2. Priority Ring (Modern Donut with Center Stat & Clean Legend) ───
        make('chart-priority-ring', {
            tooltip: {
                ...tip(),
                formatter: (p) => {
                    const slaDesc = {
                        P1: 'Kritis (Lumpuh Total) · SLA 2 Jam',
                        P2: 'Tinggi (Gangguan Parah) · SLA 4 Jam',
                        P3: 'Sedang (Operasional Parsial) · SLA 8 Jam',
                        P4: 'Rendah (Permintaan Layanan) · SLA 48 Jam',
                    };
                    return `<div style="font-weight:700;color:${p.color};font-size:13px">${p.name} — ${slaDesc[p.name] || ''}</div>
                            <div style="font-size:14px;font-weight:800;margin-top:4px;color:#0f172a">
                                ${p.value} tiket <span style="font-size:11.5px;color:#64748b;font-weight:600">(${fmt(p.percent, 1)}%)</span>
                            </div>`;
                },
            },
            title: {
                text: `${K.total}`,
                subtext: 'TOTAL TIKET',
                left: 'center',
                top: '36%',
                textStyle: { fontSize: 24, fontWeight: '800', color: '#0f172a', fontFamily: 'Inter, sans-serif' },
                subtextStyle: { fontSize: 10, fontWeight: '700', color: '#64748b', letterSpacing: 1.2, fontFamily: 'Inter, sans-serif' },
            },
            legend: {
                bottom: 2,
                left: 'center',
                itemGap: 14,
                itemWidth: 10,
                itemHeight: 10,
                icon: 'circle',
                textStyle: { color: '#334155', fontSize: 11.5, fontWeight: '600', fontFamily: 'Inter, sans-serif' },
                formatter: (name) => {
                    const item = D.priority.find((p) => p.key === name);
                    const pct = item ? ((item.value / K.total) * 100).toFixed(1) : 0;
                    return `${name}: ${item ? item.value : ''} (${pct}%)`;
                },
            },
            series: [{
                type: 'pie',
                radius: ['58%', '80%'],
                center: ['50%', '48%'],
                avoidLabelOverlap: false,
                itemStyle: {
                    borderRadius: 4,
                    borderColor: '#f1f5fa',
                    borderWidth: 3,
                },
                label: { show: false },
                emphasis: {
                    scale: true,
                    scaleSize: 5,
                    itemStyle: { shadowBlur: 8, shadowColor: 'rgba(0,0,0,0.15)' },
                },
                data: D.priority.map((p) => ({
                    name: p.key,
                    value: p.value,
                    itemStyle: { color: PRIO_COLOR[p.key] || C.accent },
                })),
            }],
        });

        // ── 3. Technician Workload Imbalance (Stacked Bar) ────────────────────
        const techsSorted = [...D.technicians].sort((a, b) => b.tickets - a.tickets);
        make('chart-workload', {
            tooltip: {
                ...tip(),
                trigger: 'axis',
                axisPointer: { type: 'shadow' },
                formatter: (params) => {
                    const tech = techsSorted[params[0].dataIndex];
                    return `<div style="font-weight:700;margin-bottom:4px;color:#0f172a">${tech.name}</div>
                            Total Tiket: <b>${tech.tickets}</b> (${fmt(tech.share_pct, 1)}% dari total)<br/>
                            Layer 1: <b>${tech.layer1}</b> · Layer 2: <b>${tech.layer2}</b> (${fmt(tech.layer2_pct, 1)}%)<br/>
                            Rata-rata Resolusi: <b>${dur(tech.avg_hours)}</b> (Median: ${dur(tech.median_hours)})<br/>
                            SLA Breached: <b style="color:${C.p1}">${tech.breached} tiket (${fmt(tech.breach_pct, 1)}%)</b>`;
                },
            },
            legend: {
                top: 0,
                icon: 'circle',
                textStyle: { color: '#334155', fontSize: 11.5, fontWeight: '600' },
                itemWidth: 10,
                itemHeight: 10,
            },
            grid: { left: 140, right: 45, top: 35, bottom: 25 },
            xAxis: { ...axisCommon, type: 'value', name: 'Tiket' },
            yAxis: {
                ...axisCommon,
                type: 'category',
                data: techsSorted.map((t) => t.name).reverse(),
                axisLabel: { ...axisCommon.axisLabel, fontSize: 11.5, color: '#1e293b', fontWeight: '600' },
            },
            series: [
                {
                    name: 'Layer 1 (Remote/Guide)',
                    type: 'bar',
                    stack: 'total',
                    barWidth: 18,
                    itemStyle: { color: '#2563eb' },
                    data: techsSorted.map((t) => t.layer1).reverse(),
                },
                {
                    name: 'Layer 2 (Visit/Hardware)',
                    type: 'bar',
                    stack: 'total',
                    barWidth: 18,
                    itemStyle: { color: '#ea580c', borderRadius: [0, 5, 5, 0] },
                    data: techsSorted.map((t) => t.layer2).reverse(),
                    label: {
                        show: true,
                        position: 'right',
                        color: '#0f172a',
                        fontWeight: '700',
                        fontSize: 11,
                        formatter: (p) => {
                            const t = techsSorted.slice().reverse()[p.dataIndex];
                            return `${t.tickets} (${fmt(t.share_pct, 0)}%)`;
                        },
                    },
                },
            ],
        });

        // ── 4. Workload vs MTTR Scatter Plot ──────────────────────────────────
        make('chart-workload-mttr', {
            tooltip: {
                ...tip(),
                formatter: (p) => `<b>${p.data.name}</b><br/>Volume: <b>${p.value[0]} tiket</b><br/>Rata-rata Resolusi: <b>${dur(p.value[1])}</b>`,
            },
            grid: { left: 55, right: 35, top: 30, bottom: 40 },
            xAxis: { ...axisCommon, type: 'value', name: 'Volume Beban (Tiket)', min: 0 },
            yAxis: { ...axisCommon, type: 'value', name: 'Avg Resolusi (Jam)' },
            series: [{
                type: 'scatter',
                symbolSize: 22,
                data: techsSorted.map((t) => ({
                    name: t.name,
                    value: [t.tickets, t.avg_hours],
                    itemStyle: {
                        color: t.breach_pct > 20 ? '#dc2626' : '#2563eb',
                        borderColor: '#ffffff',
                        borderWidth: 2,
                    },
                })),
                label: {
                    show: true,
                    formatter: (p) => p.data.name.split(' ')[0],
                    position: 'top',
                    color: '#334155',
                    fontWeight: '600',
                    fontSize: 10.5,
                },
            }],
        });

        // ── 5. City vs Tech Distribution (Semua Layer) ────────────────────────
        const topCities = D.cities.slice(0, 6).map((c) => c.key);
        const picNames = techsSorted.map((t) => t.name);
        make('chart-city-tech', {
            tooltip: { ...tip(), trigger: 'axis', axisPointer: { type: 'shadow' } },
            legend: { top: 0, icon: 'circle', textStyle: { color: '#334155', fontSize: 10.5, fontWeight: '600' } },
            grid: { left: 105, right: 30, top: 35, bottom: 25 },
            xAxis: { ...axisCommon, type: 'value', name: 'Tiket' },
            yAxis: {
                ...axisCommon,
                type: 'category',
                data: topCities.slice().reverse(),
                axisLabel: { color: '#1e293b', fontWeight: '600', fontSize: 11 },
            },
            series: picNames.map((pic, idx) => {
                const techObj = techsSorted.find((t) => t.name === pic);
                const cityMap = {};
                if (techObj && Array.isArray(techObj.city_top)) {
                    techObj.city_top.forEach((item) => {
                        cityMap[item.key] = item.value;
                    });
                }
                return {
                    name: pic.split(' ')[0],
                    type: 'bar',
                    stack: 'city',
                    barWidth: 14,
                    itemStyle: { color: PALETTE[idx % PALETTE.length] },
                    data: topCities.slice().reverse().map((city) => cityMap[city] || 0),
                };
            }),
        });

        // ── 6. SLA Benchmark vs Actual Hours ──────────────────────────────────
        make('chart-sla-compare', {
            tooltip: {
                ...tip(),
                trigger: 'axis',
                axisPointer: { type: 'shadow' },
                formatter: (p) => {
                    const prio = p[0].name;
                    const s = D.sla.find((x) => x.priority === prio);
                    return `<b>Prioritas ${prio}</b><br/>
                            Target SLA: <b>${s.limit_hours} Jam</b><br/>
                            Realisasi Rata-rata: <b style="color:${C.p1}">${dur(s.avg_hours)}</b><br/>
                            Realisasi Median: <b>${dur(s.median_hours)}</b><br/>
                            Pelanggaran: <b style="color:${C.p1}">${s.breached} dari ${s.evaluated} tiket (${fmt(s.breach_pct, 1)}%)</b>`;
                },
            },
            legend: { top: 0, icon: 'circle', textStyle: { color: '#334155', fontSize: 11.5, fontWeight: '600' } },
            grid: { left: 60, right: 30, top: 40, bottom: 30 },
            xAxis: {
                ...axisCommon,
                type: 'category',
                data: D.sla.map((s) => s.priority),
                axisLabel: { ...axisCommon.axisLabel, color: '#0f172a', fontWeight: '700', fontSize: 12.5 },
            },
            yAxis: { ...axisCommon, type: 'value', name: 'Durasi (Jam)' },
            series: [
                {
                    name: 'Target SLA Standar',
                    type: 'bar',
                    barWidth: 18,
                    itemStyle: { color: '#94a3b8', borderRadius: [4, 4, 0, 0] },
                    data: D.sla.map((s) => s.limit_hours),
                },
                {
                    name: 'Realisasi Rata-rata',
                    type: 'bar',
                    barWidth: 18,
                    itemStyle: { color: '#dc2626', borderRadius: [4, 4, 0, 0] },
                    data: D.sla.map((s) => s.avg_hours),
                    label: {
                        show: true,
                        position: 'top',
                        color: '#dc2626',
                        fontWeight: '700',
                        fontSize: 10.5,
                        formatter: (p) => dur(p.value),
                    },
                },
            ],
        });

        // ── 7. SLA Breach Donut (No ugly leader lines) ────────────────────────
        make('chart-sla-box', {
            tooltip: tip(),
            title: {
                text: `${fmt(K.sla_breach_pct, 1)}%`,
                subtext: 'MELANGGAR SLA',
                left: 'center',
                top: '36%',
                textStyle: { fontSize: 22, fontWeight: '800', color: '#dc2626', fontFamily: 'Inter, sans-serif' },
                subtextStyle: { fontSize: 10, fontWeight: '700', color: '#64748b', letterSpacing: 1, fontFamily: 'Inter, sans-serif' },
            },
            legend: {
                bottom: 2,
                icon: 'circle',
                textStyle: { color: '#334155', fontSize: 11, fontWeight: '600' },
                itemWidth: 10,
                itemHeight: 10,
            },
            series: [{
                type: 'pie',
                radius: ['58%', '80%'],
                center: ['50%', '48%'],
                avoidLabelOverlap: false,
                itemStyle: { borderRadius: 4, borderColor: '#f1f5fa', borderWidth: 3 },
                label: { show: false },
                data: [
                    { name: `Tepat Waktu (${K.sla_evaluated - K.sla_breached})`, value: K.sla_evaluated - K.sla_breached, itemStyle: { color: '#16a34a' } },
                    { name: `Melanggar SLA (${K.sla_breached})`, value: K.sla_breached, itemStyle: { color: '#dc2626' } },
                ],
            }],
        });

        // ── 8. Solving Methods Donut ──────────────────────────────────────────
        make('chart-method', {
            tooltip: tip(),
            title: {
                text: '51%',
                subtext: 'REMOTE',
                left: 'center',
                top: '36%',
                textStyle: { fontSize: 22, fontWeight: '800', color: '#2563eb', fontFamily: 'Inter, sans-serif' },
                subtextStyle: { fontSize: 10, fontWeight: '700', color: '#64748b', letterSpacing: 1, fontFamily: 'Inter, sans-serif' },
            },
            legend: {
                bottom: 0,
                icon: 'circle',
                textStyle: { color: '#334155', fontSize: 10.5, fontWeight: '500' },
                itemWidth: 8,
                itemHeight: 8,
                itemGap: 10,
            },
            series: [{
                type: 'pie',
                radius: ['58%', '80%'],
                center: ['50%', '46%'],
                avoidLabelOverlap: false,
                itemStyle: { borderRadius: 4, borderColor: '#f1f5fa', borderWidth: 3 },
                label: { show: false },
                data: D.solving.map((s, i) => ({
                    name: `${s.key}: ${s.value}`,
                    value: s.value,
                    itemStyle: { color: PALETTE[i % PALETTE.length] },
                })),
            }],
        });

        // ── 9. Hold Tickets Impact (Vertical Bar) ─────────────────────────────
        make('chart-hold', {
            tooltip: tip(),
            grid: { left: 55, right: 30, top: 25, bottom: 25 },
            xAxis: {
                ...axisCommon,
                type: 'category',
                data: ['Kasus Normal', 'Kasus On-Hold (IR/Vendor)'],
                axisLabel: { color: '#0f172a', fontWeight: '700', fontSize: 11.5 },
            },
            yAxis: { ...axisCommon, type: 'value', name: '% Breach SLA' },
            series: [{
                type: 'bar',
                showBackground: true,
                backgroundStyle: { color: '#e2e8f0', borderRadius: [6, 6, 0, 0] },
                barWidth: 26,
                data: [
                    { value: 12.8, itemStyle: { color: '#2563eb', borderRadius: [6, 6, 0, 0] } },
                    { value: (K.hold_breached / K.hold_tickets) * 100, itemStyle: { color: '#dc2626', borderRadius: [6, 6, 0, 0] } },
                ],
                label: {
                    show: true,
                    position: 'top',
                    color: '#0f172a',
                    fontWeight: '800',
                    formatter: (p) => `${fmt(p.value, 1)}%`,
                },
            }],
        });

        // ── 10. Solving Duration by Method (Horizontal Gauge) ─────────────────
        make('chart-solving', {
            tooltip: tip(),
            grid: { left: 130, right: 45, top: 12, bottom: 20 },
            xAxis: { ...axisCommon, type: 'value', name: 'Jam' },
            yAxis: {
                ...axisCommon,
                type: 'category',
                data: D.method_stats.map((m) => m.key),
                axisLabel: { ...axisCommon.axisLabel, color: '#1e293b', fontWeight: '600', fontSize: 11.5 },
            },
            series: [{
                type: 'bar',
                showBackground: true,
                backgroundStyle: { color: '#e2e8f0', borderRadius: [0, 6, 6, 0] },
                data: D.method_stats.map((m, i) => ({
                    value: m.avg_hours,
                    itemStyle: { color: PALETTE[i % PALETTE.length], borderRadius: [0, 6, 6, 0] },
                })),
                barWidth: 14,
                label: {
                    show: true,
                    position: 'right',
                    color: '#334155',
                    fontWeight: '700',
                    fontSize: 10.5,
                    formatter: (p) => dur(p.value),
                },
            }],
        });

        // ── 11. RAG Deflection Candidates (Green Gauge) ───────────────────────
        const ragCats = D.rag_candidates.slice(0, 8);
        make('chart-rag', {
            tooltip: {
                ...tip(),
                formatter: (p) => {
                    const r = ragCats[p.dataIndex];
                    return `<b>${r.key}</b> (${r.category})<br/>
                            Total Kasus: <b>${r.total}</b><br/>
                            Selesai Non-Visit: <b>${r.without_visit} (${fmt(r.pct_of_detail, 1)}%)</b><br/>
                            <i>Kasus berulang deterministik tanpa perlu kedatangan fisik.</i>`;
                },
            },
            grid: { left: 140, right: 45, top: 15, bottom: 20 },
            xAxis: { ...axisCommon, type: 'value', name: 'Tiket Non-Visit' },
            yAxis: {
                ...axisCommon,
                type: 'category',
                data: ragCats.map((r) => r.key).reverse(),
                axisLabel: { ...axisCommon.axisLabel, color: '#1e293b', fontWeight: '600', fontSize: 11 },
            },
            series: [{
                type: 'bar',
                showBackground: true,
                backgroundStyle: { color: '#e2e8f0', borderRadius: [0, 6, 6, 0] },
                barWidth: 14,
                data: ragCats.map((r) => ({
                    value: r.without_visit,
                    itemStyle: { color: '#16a34a', borderRadius: [0, 6, 6, 0] },
                })).reverse(),
                label: {
                    show: true,
                    position: 'right',
                    color: '#15803d',
                    fontWeight: '700',
                    fontSize: 10.5,
                    formatter: (p) => `${p.value} (${fmt(ragCats.slice().reverse()[p.dataIndex].pct_of_detail, 0)}%)`,
                },
            }],
        });

        // ── 12. Layer 1 vs Layer 2 (Donut with Center Stat) ───────────────────
        make('chart-layer', {
            tooltip: tip(),
            title: {
                text: '76.4%',
                subtext: 'LAYER 1 (REMOTE)',
                left: 'center',
                top: '36%',
                textStyle: { fontSize: 20, fontWeight: '800', color: '#2563eb', fontFamily: 'Inter, sans-serif' },
                subtextStyle: { fontSize: 9.5, fontWeight: '700', color: '#64748b', letterSpacing: 0.8, fontFamily: 'Inter, sans-serif' },
            },
            legend: {
                bottom: 2,
                icon: 'circle',
                textStyle: { color: '#334155', fontSize: 11, fontWeight: '600' },
                itemWidth: 10,
                itemHeight: 10,
            },
            series: [{
                type: 'pie',
                radius: ['58%', '80%'],
                center: ['50%', '48%'],
                avoidLabelOverlap: false,
                itemStyle: { borderRadius: 4, borderColor: '#f1f5fa', borderWidth: 3 },
                label: { show: false },
                data: [
                    { name: `Layer 1 Remote (${K.layer1})`, value: K.layer1, itemStyle: { color: '#2563eb' } },
                    { name: `Layer 2 Visit (${K.layer2})`, value: K.layer2, itemStyle: { color: '#ea580c' } },
                ],
            }],
        });

        // ── 13. Status Resolved vs In Progress ────────────────────────────────
        make('chart-status', {
            tooltip: tip(),
            title: {
                text: '96.1%',
                subtext: 'SELESAI',
                left: 'center',
                top: '36%',
                textStyle: { fontSize: 20, fontWeight: '800', color: '#16a34a', fontFamily: 'Inter, sans-serif' },
                subtextStyle: { fontSize: 9.5, fontWeight: '700', color: '#64748b', letterSpacing: 0.8, fontFamily: 'Inter, sans-serif' },
            },
            legend: {
                bottom: 2,
                icon: 'circle',
                textStyle: { color: '#334155', fontSize: 11, fontWeight: '600' },
                itemWidth: 10,
                itemHeight: 10,
            },
            series: [{
                type: 'pie',
                radius: ['58%', '80%'],
                center: ['50%', '48%'],
                avoidLabelOverlap: false,
                itemStyle: { borderRadius: 4, borderColor: '#f1f5fa', borderWidth: 3 },
                label: { show: false },
                data: [
                    { name: `Resolved (${K.resolved})`, value: K.resolved, itemStyle: { color: '#16a34a' } },
                    { name: `In Progress (${K.in_progress})`, value: K.in_progress, itemStyle: { color: '#d97706' } },
                ],
            }],
        });

        // ── 14. Top Detail Categories ─────────────────────────────────────────
        const top10Details = D.detail.slice(0, 10);
        make('chart-detail', {
            tooltip: tip(),
            grid: { left: 145, right: 45, top: 12, bottom: 20 },
            xAxis: { ...axisCommon, type: 'value' },
            yAxis: {
                ...axisCommon,
                type: 'category',
                data: top10Details.map((d) => d.key).reverse(),
                axisLabel: { ...axisCommon.axisLabel, color: '#1e293b', fontWeight: '600', fontSize: 11 },
            },
            series: [{
                type: 'bar',
                showBackground: true,
                backgroundStyle: { color: '#e2e8f0', borderRadius: [0, 5, 5, 0] },
                barWidth: 13,
                data: top10Details.map((d, i) => ({
                    value: d.value,
                    itemStyle: { color: PALETTE[i % PALETTE.length], borderRadius: [0, 5, 5, 0] },
                })).reverse(),
                label: {
                    show: true,
                    position: 'right',
                    color: '#334155',
                    fontWeight: '600',
                    fontSize: 10.5,
                    formatter: (p) => `${p.value} (${fmt((p.value / K.total) * 100, 1)}%)`,
                },
            }],
        });

        // ── 15. Priority vs Method (Clean Stacked Bar) ────────────────────────
        make('chart-prio-method', {
            tooltip: { ...tip(), trigger: 'axis', axisPointer: { type: 'shadow' } },
            legend: { top: 0, icon: 'circle', textStyle: { color: '#334155', fontSize: 10.5, fontWeight: '600' } },
            grid: { left: 45, right: 20, top: 35, bottom: 25 },
            xAxis: {
                ...axisCommon,
                type: 'category',
                data: ['P1', 'P2', 'P3', 'P4'],
                axisLabel: { color: '#0f172a', fontWeight: '700', fontSize: 12 },
            },
            yAxis: { ...axisCommon, type: 'value' },
            series: ['Remote', 'Guide', 'Visit', 'Service Mandiri', 'Service Vendor'].map((m, i) => ({
                name: m,
                type: 'bar',
                stack: 'pm',
                barWidth: 22,
                itemStyle: { color: PALETTE[i % PALETTE.length] },
                data: D.prio_method.map((p) => p[m] || 0),
            })),
        });

        // Resize handler for all charts
        window.addEventListener('resize', () => {
            Object.values(H.charts).forEach((c) => c && c.resize && c.resize());
        });

        // Chart di dalam <details> yang tertutup punya lebar 0 saat dibuat.
        // Paksa hitung ulang ukuran ketika panelnya dibuka.
        document.querySelectorAll('details.aside-diagram').forEach((el) => {
            el.addEventListener('toggle', () => {
                if (!el.open) return;
                requestAnimationFrame(() => {
                    Object.values(H.charts).forEach((c) => c && c.resize && c.resize());
                });
            });
        });
    };

    if (document.readyState !== 'loading' && window.HIMUP) {
        window.HIMUP_CHARTS();
    }
})();
