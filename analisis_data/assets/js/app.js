/* ==========================================================================
   HIMUP Ticketing — Sajian Analisis Data Tiket
   Semua angka berasal dari window.HIMUP_DATA (digenerate oleh
   tools/build_data.py dari cleaned_tickets.csv). Tidak ada angka hardcode
   selain label/satuan.
   ========================================================================== */

(function () {
    'use strict';

    const D = window.HIMUP_DATA;
    if (!D) {
        document.body.insertAdjacentHTML(
            'afterbegin',
            '<div style="padding:24px;font-family:monospace;color:#ff7a1a">' +
            'assets/data.js tidak termuat. Jalankan: python3 tools/build_data.py</div>'
        );
        return;
    }

    const K = D.kpis;

    // ── Palette (Solid Neumorphic Light System) ─────────────────────────
    const C = {
        text: '#0f172a',
        dim: '#334155',
        faint: '#64748b',
        line: '#cbd5e1',
        lineSoft: '#e2e8f0',
        accent: '#ea580c',
        accent2: '#0284c7',
        p1: '#dc2626',
        p2: '#ea580c',
        p3: '#2563eb',
        p4: '#16a34a',
        ok: '#16a34a',
        info: '#2563eb',
        violet: '#7c3aed',
        teal: '#0d9488',
    };

    const PRIO_COLOR = { P1: C.p1, P2: C.p2, P3: C.p3, P4: C.p4 };
    const PALETTE = ['#2563eb', '#ea580c', '#16a34a', '#7c3aed', '#0284c7', '#d97706', '#db2777', '#475569'];

    // ── Helpers ────────────────────────────────────────────────────────────
    const $ = (sel) => document.querySelector(sel);
    const $$ = (sel) => Array.from(document.querySelectorAll(sel));
    const fmt = (n, d = 0) =>
        n === null || n === undefined || Number.isNaN(n)
            ? '—'
            : Number(n).toLocaleString('id-ID', { minimumFractionDigits: d, maximumFractionDigits: d });

    const esc = (s) =>
        String(s).replace(/[&<>"']/g, (c) =>
            ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c])
        );

    /** Format durasi jam → "21,2 jam" / "5,1 hari" */
    const dur = (h) => {
        if (h === null || h === undefined) return '—';
        if (h < 1) return `${fmt(h * 60, 0)} mnt`;
        if (h < 48) return `${fmt(h, 1)} jam`;
        return `${fmt(h / 24, 1)} hari`;
    };

    /** Tooltip HTML standar untuk semua chart (Solid White Surface) */
    const tip = (extra = '') => ({
        backgroundColor: '#ffffff',
        borderColor: '#cbd5e1',
        borderWidth: 1,
        padding: [9, 12],
        textStyle: { color: '#0f172a', fontSize: 12, fontFamily: 'Inter, sans-serif' },
        extraCssText: 'border-radius:8px;box-shadow:4px 4px 14px rgba(180, 195, 215, 0.45);' + extra,
    });

    const axisCommon = {
        axisLine: { lineStyle: { color: '#cbd5e1' } },
        axisTick: { show: false },
        axisLabel: { color: '#64748b', fontSize: 11, fontFamily: 'Inter, sans-serif' },
        splitLine: { lineStyle: { color: '#f1f5f9' } },
    };

    const charts = {};
    function make(id, option) {
        const el = document.getElementById(id);
        if (!el) return null;
        const chart = echarts.init(el, null, { renderer: 'canvas' });
        chart.setOption(option);
        charts[id] = chart;
        return chart;
    }

    // ── 1. Animated counters ───────────────────────────────────────────────
    const getPath = (obj, path) => path.split('.').reduce((o, k) => (o == null ? o : o[k]), obj);

    function animateCount(el) {
        const path = el.dataset.count;
        const decimals = Number(el.dataset.decimals || 0);
        const target = getPath(D, path);
        if (target === undefined || target === null) {
            el.textContent = '—';
            return;
        }
        const obj = { v: 0 };
        gsap.to(obj, {
            v: target,
            duration: 1.25,
            ease: 'power2.out',
            onUpdate: () => {
                el.textContent = fmt(obj.v, decimals);
            },
            onComplete: () => {
                el.textContent = fmt(target, decimals);
            },
        });
    }

    // ── 2. Scroll reveal + nav ─────────────────────────────────────────────
    function initReveal() {
        const io = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (!entry.isIntersecting) return;
                    entry.target.classList.add('in');
                    io.unobserve(entry.target);
                });
            },
            { threshold: 0.08, rootMargin: '0px 0px -40px 0px' }
        );
        $$('.reveal').forEach((el) => io.observe(el));

        // counters start when visible
        const cio = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (!entry.isIntersecting) return;
                    animateCount(entry.target);
                    cio.unobserve(entry.target);
                });
            },
            { threshold: 0.4 }
        );
        $$('[data-count]').forEach((el) => cio.observe(el));
    }

    function initNav() {
        const nav = $('#topnav');
        if (!nav) return;
        const buttons = Array.from(nav.querySelectorAll('button'));

        buttons.forEach((btn) => {
            btn.addEventListener('click', () => {
                const target = document.getElementById(btn.dataset.target);
                if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            });
        });

        const sections = buttons
            .map((b) => document.getElementById(b.dataset.target))
            .filter(Boolean);

        const sio = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (!entry.isIntersecting) return;
                    buttons.forEach((b) =>
                        b.classList.toggle('active', b.dataset.target === entry.target.id)
                    );
                });
            },
            { rootMargin: '-45% 0px -50% 0px' }
        );
        sections.forEach((s) => sio.observe(s));
    }

    function initScrollProgress() {
        const bar = $('#scroll-progress');
        if (!bar) return;
        const update = () => {
            const h = document.documentElement;
            const max = h.scrollHeight - h.clientHeight;
            bar.style.width = (max > 0 ? (h.scrollTop / max) * 100 : 0) + '%';
        };
        document.addEventListener('scroll', update, { passive: true });
        update();
    }

    // ── 3. Populate text placeholders ──────────────────────────────────────
    function initText() {
        $$('.js-ticket-count').forEach((el) => (el.textContent = fmt(K.total)));

        const techs = [...D.technicians].sort((a, b) => b.tickets - a.tickets);
        const top = techs[0];
        const bottom = techs[techs.length - 1];
        $$('[data-tech-max]').forEach((el) => (el.textContent = fmt(top.tickets)));
        $$('[data-tech-min]').forEach((el) => (el.textContent = fmt(bottom.tickets)));

        const topTwo = (top.tickets + techs[1].tickets) / K.total * 100;
        $$('.js-top-two-share').forEach((el) => (el.textContent = fmt(topTwo, 0) + '%'));
        $$('.js-bottom-share').forEach((el) => (el.textContent = fmt(bottom.share_pct, 0) + '%'));

        // visit percentage (dipakai di section RAG)
        D.kpis.visit_pct = +(100 * D.kpis.visit / K.total).toFixed(2);

        const src = $('#footer-source');
        if (src) src.textContent = D.generated_from;
    }

    // ── Expose helpers for charts.js ───────────────────────────────────────
    window.HIMUP = {
        D, K, C, $, $$, fmt, esc, dur, tip, axisCommon,
        PALETTE, PRIO_COLOR, charts, make, getPath, animateCount,
    };

    // ── Boot ───────────────────────────────────────────────────────────────
    function boot() {
        initText();
        initReveal();
        initNav();
        initScrollProgress();
        if (window.HIMUP_CHARTS) window.HIMUP_CHARTS();
        if (window.HIMUP_PANELS) window.HIMUP_PANELS();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', boot);
    } else {
        boot();
    }
})();