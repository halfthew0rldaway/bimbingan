/* ==========================================================================
   HIMUP Ticketing — panels.js
   Tabel, kartu bukti, simulasi algoritma penugasan teknisi, dan mockup demo
   ========================================================================== */

(function () {
    'use strict';

    window.HIMUP_PANELS = function () {
        const H = window.HIMUP;
        if (!H || !H.D) return;

        const { D, K, C, $, $$, fmt, esc, dur, PRIO_COLOR } = H;

        // ── 1. Technician Profile Summary ─────────────────────────────────────
        const techHolder = $('#tech-profile');
        if (techHolder) {
            const techs = [...D.technicians].sort((a, b) => b.tickets - a.tickets);
            const top = techs[0];
            const bottom = techs[techs.length - 1];
            techHolder.innerHTML = `
                <div class="grid grid-3" style="gap:12px; margin-top:10px">
                    <div class="card is-alert" style="padding:14px 16px">
                        <div style="font-size:11px; color:var(--text-faint); text-transform:uppercase">Teknisi Beban Tertinggi</div>
                        <div style="font-size:18px; font-weight:700; color:var(--accent); margin-top:4px">${esc(top.name)}</div>
                        <div style="font-size:12px; color:var(--text-dim); margin-top:2px">
                            <b>${top.tickets} tiket</b> (${fmt(top.share_pct, 1)}%) · rata-rata ${dur(top.avg_hours)}
                        </div>
                    </div>
                    <div class="card is-info" style="padding:14px 16px">
                        <div style="font-size:11px; color:var(--text-faint); text-transform:uppercase">Teknisi Beban Terendah</div>
                        <div style="font-size:18px; font-weight:700; color:var(--info); margin-top:4px">${esc(bottom.name)}</div>
                        <div style="font-size:12px; color:var(--text-dim); margin-top:2px">
                            <b>${bottom.tickets} tiket</b> (${fmt(bottom.share_pct, 1)}%) · rata-rata ${dur(bottom.avg_hours)}
                        </div>
                    </div>
                    <div class="card is-violet" style="padding:14px 16px">
                        <div style="font-size:11px; color:var(--text-faint); text-transform:uppercase">Selisih Beban Kerja</div>
                        <div style="font-size:18px; font-weight:700; color:var(--violet); margin-top:4px">${fmt(K.workload_ratio, 1)}× lipat</div>
                        <div style="font-size:12px; color:var(--text-dim); margin-top:2px">
                            Simpangan: ±${fmt(K.workload_std, 1)} tiket
                        </div>
                    </div>
                </div>
            `;
        }

        // ── 2. Technician Matrix Table ─────────────────────────────────────────
        const matrixHolder = $('#matrix-holder');
        if (matrixHolder) {
            const techs = [...D.technicians].sort((a, b) => b.tickets - a.tickets);
            let html = `
                <table class="table">
                    <thead>
                        <tr>
                            <th>Teknisi (PIC)</th>
                            <th style="text-align:right">Total Tiket</th>
                            <th style="text-align:right">Porsi</th>
                            <th style="text-align:right">Layer 1</th>
                            <th style="text-align:right">Layer 2 (Visit)</th>
                            <th style="text-align:right">Avg Resolusi</th>
                            <th style="text-align:right">Median</th>
                            <th style="text-align:right">Pelanggaran SLA</th>
                            <th>Kota Terbanyak</th>
                        </tr>
                    </thead>
                    <tbody>
            `;
            techs.forEach((t) => {
                const breachColor = t.breach_pct > 20 ? 'color:var(--p1); font-weight:700' : 'color:var(--text-dim)';
                const topCitiesStr = Array.isArray(t.city_top)
                    ? t.city_top.slice(0, 2).map((c) => `${c.key} (${c.value})`).join(', ')
                    : (t.city_top || 'JAKARTA');
                html += `
                    <tr>
                        <td><b>${esc(t.name)}</b></td>
                        <td style="text-align:right"><b>${t.tickets}</b></td>
                        <td style="text-align:right">${fmt(t.share_pct, 1)}%</td>
                        <td style="text-align:right">${t.layer1}</td>
                        <td style="text-align:right">${t.layer2} <span style="font-size:10.5px; color:var(--text-faint)">(${fmt(t.layer2_pct, 0)}%)</span></td>
                        <td style="text-align:right">${dur(t.avg_hours)}</td>
                        <td style="text-align:right">${dur(t.median_hours)}</td>
                        <td style="text-align:right; ${breachColor}">${t.breached} (${fmt(t.breach_pct, 1)}%)</td>
                        <td><span class="badge" style="background:#f1f5f9; color:var(--text); border:1px solid var(--line-soft); font-size:11px">${esc(topCitiesStr)}</span></td>
                    </tr>
                `;
            });
            html += `</tbody></table>`;
            matrixHolder.innerHTML = html;
        }

        // ── 3. SLA KPI Row ────────────────────────────────────────────────────
        const slaKpiHolder = $('#sla-kpi-row');
        if (slaKpiHolder) {
            let html = '';
            D.sla.forEach((s) => {
                const isOver = s.avg_hours > s.limit_hours;
                const badgeColor = isOver ? 'var(--p1)' : 'var(--ok)';
                html += `
                    <div class="card kpi" style="border-top:3px solid ${PRIO_COLOR[s.priority]}">
                        <div class="kpi-label" style="display:flex; justify-content:space-between">
                            <span>Prioritas ${s.priority}</span>
                            <span style="color:${badgeColor}; font-weight:600">${isOver ? 'OVER SLA' : 'ON TARGET'}</span>
                        </div>
                        <div class="kpi-value" style="font-size:26px">${dur(s.avg_hours)}</div>
                        <div class="kpi-foot">
                            Target SLA: <b>${s.limit_hours} Jam</b><br/>
                            Breached: <b style="color:${isOver ? 'var(--p1)' : 'var(--text)'}">${s.breached} dari ${s.evaluated} (${fmt(s.breach_pct, 1)}%)</b>
                        </div>
                    </div>
                `;
            });
            slaKpiHolder.innerHTML = html;
        }

        // ── 4. SLA Audit Table ────────────────────────────────────────────────
        const slaTableHolder = $('#sla-table-holder');
        if (slaTableHolder) {
            let html = `
                <table class="table">
                    <thead>
                        <tr>
                            <th>Tingkat Prioritas</th>
                            <th>Target SLA</th>
                            <th style="text-align:right">Total Tiket</th>
                            <th style="text-align:right">Dievaluasi</th>
                            <th style="text-align:right">Tepat Waktu</th>
                            <th style="text-align:right">Melanggar (Breach)</th>
                            <th style="text-align:right">% Pelanggaran</th>
                            <th style="text-align:right">Rata-rata Durasi</th>
                            <th style="text-align:right">Median</th>
                            <th style="text-align:right">P90 Durasi</th>
                        </tr>
                    </thead>
                    <tbody>
            `;
            D.sla.forEach((s) => {
                const breachStyle = s.breach_pct > 15 ? 'color:var(--p1); font-weight:700' : 'color:var(--ok)';
                html += `
                    <tr>
                        <td><span class="badge badge-prio" style="border-left:4px solid ${PRIO_COLOR[s.priority]}"><b>${s.priority}</b></span></td>
                        <td><b>${s.limit_hours} Jam</b></td>
                        <td style="text-align:right">${s.total}</td>
                        <td style="text-align:right">${s.evaluated}</td>
                        <td style="text-align:right">${s.within} (${fmt(s.within_pct, 1)}%)</td>
                        <td style="text-align:right; ${breachStyle}">${s.breached}</td>
                        <td style="text-align:right; ${breachStyle}">${fmt(s.breach_pct, 1)}%</td>
                        <td style="text-align:right">${dur(s.avg_hours)}</td>
                        <td style="text-align:right">${dur(s.median_hours)}</td>
                        <td style="text-align:right">${dur(s.p90_hours)}</td>
                    </tr>
                `;
            });
            html += `</tbody></table>`;
            slaTableHolder.innerHTML = html;
        }

        // ── 5. Bottleneck Quotes from Dataset ─────────────────────────────────
        const quotesHolder = $('#bottleneck-quotes');
        if (quotesHolder) {
            let html = '';
            (D.bottlenecks || []).slice(0, 10).forEach((b) => {
                html += `
                    <div class="card" style="padding:11px 14px; border-left:4px solid var(--accent); background:#ffffff; box-shadow:var(--nm-extruded-sm)">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:5px">
                            <div style="font-family:var(--mono); font-size:11px; color:var(--text-faint)">
                                <b>${esc(b.ticket)}</b> · ${esc(b.city)} · <span style="color:${PRIO_COLOR[b.priority] || 'var(--text)'}">${b.priority}</span>
                            </div>
                            <span class="badge is-alert" style="font-size:10px">${dur(b.hours)} (limit: ${b.limit}j)</span>
                        </div>
                        <div style="font-size:12.5px; color:var(--text); line-height:1.45">
                            “${esc(b.note)}”
                        </div>
                    </div>
                `;
            });
            quotesHolder.innerHTML = html;
        }

        // ── 6. RAG Automation Table ───────────────────────────────────────────
        const ragTableHolder = $('#rag-table-holder');
        if (ragTableHolder) {
            let html = `
                <table class="table">
                    <thead>
                        <tr>
                            <th>Detail Kasus Masalah</th>
                            <th>Kategori Induk</th>
                            <th style="text-align:right">Total Tiket</th>
                            <th style="text-align:right">Selesai Tanpa Kunjungan (Remote/Guide)</th>
                            <th style="text-align:right">% Selesai Tanpa Kunjungan</th>
                            <th>Alasan Cocok Dijadikan Panduan Mandiri</th>
                        </tr>
                    </thead>
                    <tbody>
            `;
            const justifications = {
                'Close Bill': 'SOP settlement kasir & void bill memiliki pola jawaban 100% deterministik.',
                'Menu': 'Panduan update harga & sync menu POS kasir via admin panel.',
                'Create User': 'Instruksi pembuatan credential atau form registrasi staf baru.',
                'Email': 'Panduan konfigurasi webmail, reset password, dan setting SMTP outlet.',
                'Modem Internet': 'Prosedur restart perangkat, cek lampu indikator FO, & panduan eskalasi ISP.',
                'Kabel Data/LAN': 'Panduan cek port switch & kabel LAN lepas sebelum dispatch teknisi.',
            };
            (D.rag_candidates || []).forEach((r) => {
                const just = justifications[r.key] || 'Troubleshooting mandiri tingkat awal berbasis dokumen SOP.';
                html += `
                    <tr>
                        <td><b>${esc(r.key)}</b></td>
                        <td>${esc(r.category)}</td>
                        <td style="text-align:right">${r.total}</td>
                        <td style="text-align:right"><b>${r.without_visit}</b></td>
                        <td style="text-align:right; color:var(--ok); font-weight:700">${fmt(r.pct_of_detail, 1)}%</td>
                        <td style="font-size:12px; color:var(--text-dim)">${just}</td>
                    </tr>
                `;
            });
            html += `</tbody></table>`;
            ragTableHolder.innerHTML = html;
        }

        // ── 7. Lifecycle Flow ─────────────────────────────────────────────────
        const flowHolder = $('#lifecycle-flow');
        if (flowHolder) {
            const steps = [
                { num: '01', title: 'Open / Dilaporkan', desc: 'Cabang mengisi formulir web terstruktur beserta foto bukti' },
                { num: '02', title: 'Triage & Penugasan', desc: 'Sistem menyusun urutan teknisi yang paling sesuai' },
                { num: '03', title: 'In Progress', desc: 'Teknisi menerima notifikasi lalu menangani (Remote / Visit)' },
                { num: '04', title: 'On-Hold (Pending)', desc: 'Hitungan waktu dihentikan: menunggu sparepart / IR / vendor' },
                { num: '05', title: 'Resolved', desc: 'Kendala selesai diperbaiki, teknisi melampirkan bukti' },
                { num: '06', title: 'Closed', desc: 'Cabang mengonfirmasi normal, atau tiket ditutup otomatis' },
            ];
            flowHolder.innerHTML = steps.map((s) => `
                <div class="flow-step">
                    <div class="flow-num">Tahap ${s.num}</div>
                    <div class="flow-title">${s.title}</div>
                    <div class="flow-desc">${s.desc}</div>
                </div>
            `).join('');
        }

        // ── 8. Pertimbangan penugasan ─────────────────────────────────────────
        const critCardsHolder = $('#crit-cards');
        if (critCardsHolder) {
            const crits = [
                { id: '1', name: 'Kedekatan wilayah', type: 'Cost', desc: 'Seberapa dekat wilayah teknisi dengan outlet yang melapor.' },
                { id: '2', name: 'Jumlah tiket aktif', type: 'Cost', desc: 'Banyaknya tiket yang sedang dikerjakan, agar tidak menumpuk pada satu orang.' },
                { id: '3', name: 'Kecocokan keahlian', type: 'Benefit', desc: 'Kesesuaian kemampuan teknisi (Layer 1 perangkat lunak / Layer 2 perangkat keras) dengan jenis tiket.' },
                { id: '4', name: 'Kecepatan penyelesaian', type: 'Benefit', desc: 'Rata-rata kecepatan menyelesaikan tiket serupa sebelumnya.' },
            ];
            critCardsHolder.innerHTML = crits.map((c) => `
                <div class="card" style="padding:14px 16px; border-top:3px solid ${c.type === 'Cost' ? 'var(--accent)' : 'var(--ok)'}">
                    <div style="display:flex; justify-content:space-between; align-items:center; gap:8px">
                        <span style="font-weight:700; color:var(--text)">${c.id}. ${c.name}</span>
                        <span class="badge ${c.type === 'Cost' ? 'is-alert' : 'is-ok'}" style="font-size:10px">${c.type === 'Cost' ? 'minimalkan' : 'maksimalkan'}</span>
                    </div>
                    <p style="font-size:12px; color:var(--text-dim); margin-top:8px; line-height:1.45">${c.desc}</p>
                </div>
            `).join('');
        }

        // ── 9. Simulator penugasan teknisi ────────────────────────────────────
        initSimulator();

        function initSimulator() {
            const citySelect = $('#sim-city');
            const detailSelect = $('#sim-detail');
            const layerSelect = $('#sim-layer');
            const prioritySelect = $('#sim-priority');
            const sliderHolder = $('#weight-sliders');
            const weightBar = $('#weight-bar');
            const weightLegend = $('#weight-legend');
            const weightTotal = $('#weight-total');

            if (!citySelect || !detailSelect) return;

            // Populate Dropdowns
            citySelect.innerHTML = D.cities.map((c) => `<option value="${esc(c.key)}">${esc(c.key)} (${c.value} tiket)</option>`).join('');
            detailSelect.innerHTML = D.detail.slice(0, 15).map((d) => `<option value="${esc(d.key)}">${esc(d.key)} (${d.value} tiket)</option>`).join('');

            // Weights State (Default: 30%, 30%, 25%, 15%)
            const weights = {
                c1: 30, // Jarak / Region
                c2: 30, // Workload
                c3: 25, // Skill
                c4: 15, // MTTR
            };

            const critDefs = [
                { key: 'c1', name: '1. Kedekatan wilayah (minimalkan)', color: C.accent },
                { key: 'c2', name: '2. Jumlah tiket aktif (minimalkan)', color: C.info },
                { key: 'c3', name: '3. Kecocokan keahlian (maksimalkan)', color: C.ok },
                { key: 'c4', name: '4. Kecepatan penyelesaian (maksimalkan)', color: C.violet },
            ];

            function renderSliders() {
                if (!sliderHolder) return;
                sliderHolder.innerHTML = critDefs.map((cd) => `
                    <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px">
                        <span style="color:${cd.color}; font-weight:600">${cd.name}</span>
                        <div style="display:flex; align-items:center; gap:8px">
                            <input type="range" class="sim-slider" data-key="${cd.key}" min="5" max="60" value="${weights[cd.key]}" style="width:110px">
                            <span style="font-family:var(--mono); width:32px; text-align:right" id="val-${cd.key}">${weights[cd.key]}%</span>
                        </div>
                    </div>
                `).join('');

                $$('.sim-slider').forEach((slider) => {
                    slider.addEventListener('input', (e) => {
                        weights[e.target.dataset.key] = Number(e.target.value);
                        $(`#val-${e.target.dataset.key}`).textContent = `${e.target.value}%`;
                        updateWeightBar();
                        runTOPSIS();
                    });
                });
                updateWeightBar();
            }

            function updateWeightBar() {
                const total = weights.c1 + weights.c2 + weights.c3 + weights.c4;
                if (weightTotal) {
                    weightTotal.textContent = `Σ = ${total}%`;
                    weightTotal.style.color = total === 100 ? 'var(--ok)' : 'var(--p1)';
                }
                if (weightBar) {
                    weightBar.innerHTML = critDefs.map((cd) => {
                        const pct = (weights[cd.key] / total) * 100;
                        return `<div style="width:${pct}%; background:${cd.color}; height:8px" title="${cd.name}: ${pct.toFixed(0)}%"></div>`;
                    }).join('');
                }
                if (weightLegend) {
                    weightLegend.innerHTML = critDefs.map((cd) => `
                        <span style="display:inline-flex; align-items:center; gap:4px; font-size:11px; margin-right:10px">
                            <span style="display:inline-block; width:8px; height:8px; border-radius:2px; background:${cd.color}"></span>
                            ${cd.name.split(':')[0]} (${weights[cd.key]}%)
                        </span>
                    `).join('');
                }
            }

            renderSliders();

            [citySelect, detailSelect, layerSelect, prioritySelect].forEach((el) => {
                if (el) el.addEventListener('change', runTOPSIS);
            });

            function runTOPSIS() {
                const targetCity = citySelect.value;
                const targetDetail = detailSelect.value;
                const targetLayer = layerSelect.value;

                // Normalize weights so sum is 1.0
                const wSum = weights.c1 + weights.c2 + weights.c3 + weights.c4;
                const W = {
                    c1: weights.c1 / wSum,
                    c2: weights.c2 / wSum,
                    c3: weights.c3 / wSum,
                    c4: weights.c4 / wSum,
                };

                // Evaluasi 6 teknisi
                const techs = D.technicians;
                const rawMatrix = techs.map((t) => {
                    // C1: Distance Penalty (Cost - smaller is better)
                    // If technician frequently visits target city, distance penalty is low (1)
                    // If target city is Jakarta and tech is in Jakarta, distance penalty is 2
                    // If target city is outside and tech rarely visits, penalty is 8-10
                    const cityFreq = (D.pic_city2 && D.pic_city2[t.name] && D.pic_city2[t.name][targetCity]) || 0;
                    let c1_dist = cityFreq > 10 ? 1.0 : cityFreq > 2 ? 3.0 : (targetCity === 'JAKARTA' ? 4.0 : 9.0);

                    // C2: Workload (Cost - smaller active tickets is better)
                    // Simulated active queue based on total tickets share
                    const c2_load = Math.max(1, Math.round(t.tickets / 18));

                    // C3: Skill Match (Benefit - higher is better)
                    // If ticket requires Layer 2 / Hardware and tech has high Layer 2 experience
                    let c3_skill = 5.0;
                    if (targetLayer === 'Layer 2') {
                        c3_skill = (t.layer2_pct / 10) + 3.0; // scale 4 - 9
                    } else {
                        c3_skill = (t.layer1 / 70) + 4.0;
                    }
                    // Bonus if tech previously handled this exact detail
                    if (t.details && t.details[targetDetail]) {
                        c3_skill += 2.0;
                    }

                    // C4: Historical MTTR Score (Benefit - faster avg_hours is higher score)
                    // Inverse of average hours: score = 50 / avg_hours
                    const c4_mttr = Math.max(1.0, Math.min(10.0, 60.0 / (t.avg_hours || 20.0)));

                    return { tech: t, c1: c1_dist, c2: c2_load, c3: c3_skill, c4: c4_mttr };
                });

                // Vector Normalization: r_ij = x_ij / sqrt(sum(x_ij^2))
                const sqSum = { c1: 0, c2: 0, c3: 0, c4: 0 };
                rawMatrix.forEach((r) => {
                    sqSum.c1 += r.c1 * r.c1;
                    sqSum.c2 += r.c2 * r.c2;
                    sqSum.c3 += r.c3 * r.c3;
                    sqSum.c4 += r.c4 * r.c4;
                });
                const normRoot = {
                    c1: Math.sqrt(sqSum.c1),
                    c2: Math.sqrt(sqSum.c2),
                    c3: Math.sqrt(sqSum.c3),
                    c4: Math.sqrt(sqSum.c4),
                };

                // Weighted Normalized Matrix: v_ij = w_j * r_ij
                const weighted = rawMatrix.map((r) => ({
                    tech: r.tech,
                    raw: r,
                    v1: W.c1 * (r.c1 / normRoot.c1),
                    v2: W.c2 * (r.c2 / normRoot.c2),
                    v3: W.c3 * (r.c3 / normRoot.c3),
                    v4: W.c4 * (r.c4 / normRoot.c4),
                }));

                // Determine Ideal Solutions:
                // C1 (Cost): A+ = min, A- = max
                // C2 (Cost): A+ = min, A- = max
                // C3 (Benefit): A+ = max, A- = min
                // C4 (Benefit): A+ = max, A- = min
                const v1_arr = weighted.map((w) => w.v1);
                const v2_arr = weighted.map((w) => w.v2);
                const v3_arr = weighted.map((w) => w.v3);
                const v4_arr = weighted.map((w) => w.v4);

                const A_plus = {
                    v1: Math.min(...v1_arr),
                    v2: Math.min(...v2_arr),
                    v3: Math.max(...v3_arr),
                    v4: Math.max(...v4_arr),
                };
                const A_minus = {
                    v1: Math.max(...v1_arr),
                    v2: Math.max(...v2_arr),
                    v3: Math.min(...v3_arr),
                    v4: Math.min(...v4_arr),
                };

                // Calculate Euclidean Distances D+ and D- and Closeness Vi
                const scored = weighted.map((w) => {
                    const d_plus = Math.sqrt(
                        Math.pow(w.v1 - A_plus.v1, 2) +
                        Math.pow(w.v2 - A_plus.v2, 2) +
                        Math.pow(w.v3 - A_plus.v3, 2) +
                        Math.pow(w.v4 - A_plus.v4, 2)
                    );
                    const d_minus = Math.sqrt(
                        Math.pow(w.v1 - A_minus.v1, 2) +
                        Math.pow(w.v2 - A_minus.v2, 2) +
                        Math.pow(w.v3 - A_minus.v3, 2) +
                        Math.pow(w.v4 - A_minus.v4, 2)
                    );
                    const Vi = d_minus / (d_plus + d_minus);
                    return {
                        tech: w.tech,
                        raw: w.raw,
                        d_plus,
                        d_minus,
                        score: Vi,
                    };
                });

                scored.sort((a, b) => b.score - a.score);

                // Render Ranking List
                const resultsHolder = $('#sim-results');
                const summaryHolder = $('#sim-summary');
                const critTableHolder = $('#crit-table-holder');

                if (summaryHolder && scored[0]) {
                    summaryHolder.innerHTML = `Rekomendasi Utama: <b style="color:var(--ok)">${esc(scored[0].tech.name)}</b> (Skor Preferensi: ${scored[0].score.toFixed(3)})`;
                }

                if (critTableHolder) {
                    let tHtml = `
                        <table class="table" style="font-size:11.5px">
                            <thead>
                                <tr>
                                    <th>Kandidat Teknisi</th>
                                    <th style="text-align:right">1. Kedekatan wilayah</th>
                                    <th style="text-align:right">2. Tiket aktif</th>
                                    <th style="text-align:right">3. Kecocokan keahlian</th>
                                    <th style="text-align:right">4. Kecepatan</th>
                                    <th style="text-align:right; color:var(--ok)">D+ (Jarak Ideal +)</th>
                                    <th style="text-align:right; color:var(--accent)">D- (Jarak Ideal -)</th>
                                    <th style="text-align:right; font-weight:700">Skor Preferensi (Vi)</th>
                                    <th style="text-align:center">Ranking</th>
                                </tr>
                            </thead>
                            <tbody>
                    `;
                    scored.forEach((item, idx) => {
                        const isWinner = idx === 0;
                        tHtml += `
                            <tr style="${isWinner ? 'background:rgba(62,207,142,0.06); font-weight:600' : ''}">
                                <td><b>${esc(item.tech.name)}</b></td>
                                <td style="text-align:right; font-family:var(--mono)">${item.raw.c1.toFixed(1)}</td>
                                <td style="text-align:right; font-family:var(--mono)">${item.raw.c2} tkt</td>
                                <td style="text-align:right; font-family:var(--mono)">${item.raw.c3.toFixed(1)}</td>
                                <td style="text-align:right; font-family:var(--mono)">${item.raw.c4.toFixed(1)}</td>
                                <td style="text-align:right; font-family:var(--mono); color:var(--ok)">${item.d_plus.toFixed(4)}</td>
                                <td style="text-align:right; font-family:var(--mono); color:var(--accent)">${item.d_minus.toFixed(4)}</td>
                                <td style="text-align:right; font-family:var(--mono); font-size:12.5px; font-weight:700; color:${isWinner ? 'var(--ok)' : 'var(--text)'}">
                                    ${item.score.toFixed(4)}
                                </td>
                                <td style="text-align:center">
                                    <span class="badge ${isWinner ? 'is-ok' : ''}" style="font-size:10px">#${idx + 1}</span>
                                </td>
                            </tr>
                        `;
                    });
                    tHtml += `</tbody></table>`;
                    critTableHolder.innerHTML = tHtml;
                }

                if (resultsHolder) {
                    resultsHolder.innerHTML = scored.map((item, idx) => {
                        const isWinner = idx === 0;
                        const rankBadge = isWinner
                            ? `<span class="badge is-ok" style="font-size:10.5px">REKOMENDASI UTAMA</span>`
                            : `<span style="font-family:var(--mono); color:var(--text-faint); font-size:12px">Rank #${idx + 1}</span>`;

                        const borderStyle = isWinner
                            ? 'border-left:4px solid var(--ok); background:rgba(62,207,142,0.06)'
                            : 'border-left:4px solid var(--line)';

                        return `
                            <div class="card" style="padding:12px 14px; margin-bottom:8px; ${borderStyle}">
                                <div style="display:flex; justify-content:space-between; align-items:center">
                                    <div style="display:flex; align-items:center; gap:10px">
                                        <span style="font-size:16px; font-weight:800; font-family:var(--mono); color:${isWinner ? 'var(--ok)' : 'var(--text-dim)'}">#${idx + 1}</span>
                                        <div>
                                            <div style="font-weight:700; font-size:14px; color:${isWinner ? 'var(--text)' : 'var(--text-dim)'}">${esc(item.tech.name)}</div>
                                            <div style="font-size:11.5px; color:var(--text-faint); margin-top:2px">
                                                Tiket aktif: ~${item.raw.c2} · Jarak: ${item.raw.c1} · Keahlian: ${item.raw.c3.toFixed(1)}/10 · Kecepatan: ${item.raw.c4.toFixed(1)}
                                            </div>
                                        </div>
                                    </div>
                                    <div style="text-align:right">
                                        <div style="font-family:var(--mono); font-size:17px; font-weight:800; color:${isWinner ? 'var(--ok)' : 'var(--accent)'}">${(item.score * 100).toFixed(1)}%</div>
                                        <div style="margin-top:2px">${rankBadge}</div>
                                    </div>
                                </div>
                            </div>
                        `;
                    }).join('');
                }
            }

            runTOPSIS();
        }

        // ── 10. Mock Demo Panel (Wednesday Demo Prototype) ────────────────────
        initMockDemo();

        function initMockDemo() {
            const catHolder = $('#mock-categories');
            const detHolder = $('#mock-details');
            const rankHolder = $('#mock-rank');
            const chatHolder = $('#mock-chat');

            if (!catHolder) return;

            const cats = ['Software & Apps', 'Hardware & Device', 'Network'];
            const detailsMap = {
                'Software & Apps': ['Close Bill (Duty Meal)', 'Menu Sync POS', 'Create User Kasir'],
                'Hardware & Device': ['Printer Bixolon DX220', 'CCTV Offline', 'KDS Display Rusak'],
                'Network': ['Modem Internet Los', 'Kabel LAN Switch', 'Access Point Terputus'],
            };

            let selectedCat = 'Hardware & Device';
            let selectedDet = 'Printer Bixolon DX220';

            function renderMockControls() {
                catHolder.innerHTML = cats.map((c) => `
                    <button class="badge ${c === selectedCat ? 'is-ok' : ''}" style="cursor:pointer; font-size:11px; padding:5px 9px" data-mock-cat="${esc(c)}">
                        ${esc(c)}
                    </button>
                `).join('');

                const dets = detailsMap[selectedCat] || [];
                detHolder.innerHTML = dets.map((d) => `
                    <button class="badge ${d === selectedDet ? 'is-alert' : ''}" style="cursor:pointer; font-size:11px; padding:5px 9px" data-mock-det="${esc(d)}">
                        ${esc(d)}
                    </button>
                `).join('');

                $$('[data-mock-cat]').forEach((b) => b.addEventListener('click', (e) => {
                    selectedCat = e.target.dataset.mockCat;
                    selectedDet = (detailsMap[selectedCat] || [])[0];
                    renderMockControls();
                    updateMockOutput();
                }));

                $$('[data-mock-det]').forEach((b) => b.addEventListener('click', (e) => {
                    selectedDet = e.target.dataset.mockDet;
                    renderMockControls();
                    updateMockOutput();
                }));
            }

            function updateMockOutput() {
                // Mock Recommendation
                if (rankHolder) {
                    const isHard = selectedCat === 'Hardware & Device';
                    const recName = isHard ? 'Faisal Anwar' : 'Sony Dewantara';
                    const altName = isHard ? 'Yuri Pradana' : 'Willy Surya Putra';
                    rankHolder.innerHTML = `
                        <div class="card" style="padding:10px 12px; border-left:4px solid var(--ok); background:#dcfce7; border-color:#bbf7d0">
                            <div style="display:flex; justify-content:space-between; align-items:center">
                                <div>
                                    <span class="badge is-ok" style="font-size:9.5px">REKOMENDASI #1</span>
                                    <b style="margin-left:6px; font-size:13px">${recName}</b>
                                    <div style="font-size:11px; color:var(--text-faint); margin-top:2px">Cocok untuk ${selectedDet} · Workload: 4 tiket</div>
                                </div>
                                <span style="font-family:var(--mono); font-weight:700; color:var(--ok)">91.4%</span>
                            </div>
                        </div>
                        <div class="card" style="padding:10px 12px; margin-top:6px; border-left:4px solid var(--line); background:#ffffff">
                            <div style="display:flex; justify-content:space-between; align-items:center">
                                <div>
                                    <span style="font-size:10px; color:var(--text-faint)">OPSI CADANGAN #2</span>
                                    <b style="margin-left:6px; font-size:13px">${altName}</b>
                                    <div style="font-size:11px; color:var(--text-faint); margin-top:2px">Jarak dekat · Workload: 6 tiket</div>
                                </div>
                                <span style="font-family:var(--mono); font-weight:700; color:var(--dim)">78.2%</span>
                            </div>
                        </div>
                    `;
                }

                // Mock RAG Chatbot
                if (chatHolder) {
                    const ragSolutions = {
                        'Close Bill (Duty Meal)': 'Panduan: Masuk ke Menu Kasir → Pilih Transaksi → Otorisasi Supervisor → Pilih Metode Duty Meal → Cetak Struk Void.',
                        'Menu Sync POS': 'Panduan: Buka Admin Backoffice → Update Master Menu → Klik "Publish ke Cabang" → Di POS klik "Sinkronisasi Data".',
                        'Create User Kasir': 'Panduan: Admin Store buka menu User Management → Tambah User → Masukkan NIK kasir → Berikan hak akses Kasir Shift 1.',
                        'Printer Bixolon DX220': 'Troubleshooting Awal: 1) Cek kabel power & kabel sensor konektor. 2) Pastikan tuas roll kertas tertutup rapat. 3) Tekan Feed 3 detik untuk cetak self-test print.',
                        'CCTV Offline': 'Troubleshooting: Periksa adaptor DVR, pastikan lampu link port switch menyala, lalu ping IP DVR cabang via gateway lokal.',
                        'KDS Display Rusak': 'Troubleshooting: Periksa konektor HDMI/VGA ke monitor kitchen, restart aplikasi KDS service di PC client.',
                        'Modem Internet Los': 'Troubleshooting: Jika lampu PON berkedip merah (LOS), hubungi call center provider (Indihome/Biznet). Jika hijau, restart modem 3 menit.',
                        'Kabel LAN Switch': 'Troubleshooting: Pastikan klip RJ45 tidak patah. Coba pindahkan kabel ke port switch yang masih kosong.',
                        'Access Point Terputus': 'Troubleshooting: Cek adaptor PoE injector AP, pastikan kabel LAN dari router ke port WAN AP terpasang kencang.',
                    };
                    const sol = ragSolutions[selectedDet] || 'SOP troubleshooting standar tersedia di dokumen internal IT.';

                    chatHolder.innerHTML = `
                        <div style="background:#f1f5f9; padding:10px 12px; border-radius:8px; border:1px solid var(--line-soft)">
                            <b style="color:var(--text-dim)">Staf Cabang:</b> "Halo IT, ${selectedDet} di outlet kami bermasalah."
                        </div>
                        <div style="background:#ffedd5; border-left:4px solid var(--accent); padding:10px 12px; border-radius:8px; border-top:1px solid #fed7aa; border-right:1px solid #fed7aa; border-bottom:1px solid #fed7aa">
                            <b style="color:var(--accent)">Panduan mandiri HIMUP:</b>
                            <p style="margin:4px 0 0 0; color:var(--text); line-height:1.5">${sol}</p>
                            <div style="margin-top:6px; font-size:11px; color:var(--ok); font-weight:600">
                                ✔ <i>Jika panduan ini menyelesaikan kendala, tiket tidak perlu dibuat. Beban tim IT berkurang.</i>
                            </div>
                        </div>
                    `;
                }
            }

            renderMockControls();
            updateMockOutput();
        }

        // ── 11. Ringkasan masalah → solusi ────────────────────────────────────
        const mappingHolder = $('#mapping-holder');
        if (mappingHolder) {
            mappingHolder.innerHTML = `
                <table class="table">
                    <thead>
                        <tr>
                            <th>Masalah pada proses sekarang</th>
                            <th>Bukti dari 788 tiket</th>
                            <th>Yang diusulkan</th>
                            <th>Hasil yang diharapkan</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><b>Penugasan teknisi tanpa aturan</b></td>
                            <td>Sony menangani 190 tiket (24,1%), Taqiy hanya 26 tiket (3,3%)</td>
                            <td><b>Penugasan otomatis</b> berdasarkan wilayah, jumlah tiket aktif, dan keahlian</td>
                            <td>Beban teknisi lebih merata, tidak ada yang menumpuk atau menganggur</td>
                        </tr>
                        <tr>
                            <td><b>Batas waktu sering terlewat</b></td>
                            <td>P2 rata-rata <b>21,2 jam</b> padahal target 4 jam. <b>23,4%</b> tiket P2 melewati batas</td>
                            <td><b>Penghitung waktu berjalan</b> dengan penanda warna dan pengingat otomatis</td>
                            <td>Keterlambatan terlihat sebelum batas waktu habis</td>
                        </tr>
                        <tr>
                            <td><b>Keluhan berulang selalu ditangani manual</b></td>
                            <td><b>173 tiket Close Bill</b> dan <b>140 tiket Printer</b> (lebih dari 39% total)</td>
                            <td><b>Panduan mandiri</b> yang berisi langkah penyelesaian dari SOP cabang</td>
                            <td>Sebagian keluhan selesai tanpa masuk antrean helpdesk</td>
                        </tr>
                        <tr>
                            <td><b>Waktu tunggu tidak tercatat</b></td>
                            <td>77 tiket tertunda lama karena menunggu proses IR atau sparepart</td>
                            <td><b>Status On-Hold</b> yang menghentikan hitungan waktu sementara</td>
                            <td>Waktu tunggu terpisah dari waktu pengerjaan teknisi</td>
                        </tr>
                    </tbody>
                </table>
            `;
        }
    };

    if (document.readyState !== 'loading' && window.HIMUP) {
        window.HIMUP_PANELS();
    }
})();
