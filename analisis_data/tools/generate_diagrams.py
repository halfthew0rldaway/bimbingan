#!/usr/bin/env python3
"""
Render UML 2.5 use-case diagrams (AS-IS + TO-BE) and the mapping table as
vector SVG into docs/presentation/assets/.

Design rules enforced by this renderer (the flaws of the previous hand-made
SVG are fixed here):
  1. Association lines are drawn edge-to-edge: they stop at the ellipse rim,
     never at the ellipse centre and never in empty space.
  2. Every actor sits OUTSIDE the system boundary; every use case sits INSIDE.
  3. Colour is meaningful: bottleneck steps are red, neutral steps slate,
     proposed steps green, system actors blue. A legend states this.
  4. Emoji are banned (unreliable in PDF/print); only plain Unicode glyphs.
  5. All counters (bottleneck/solution totals) are derived from the model.

Source of truth: tools/usecase_model.py
Run:

    python3 docs/presentation/tools/generate_diagrams.py
"""

from __future__ import annotations

from pathlib import Path

from usecase_model import (
    AS_IS,
    MAPPING,
    TO_BE,
    Model,
    UseCase,
    bottleneck_count,
    solution_count,
)

ROOT = Path(__file__).resolve().parents[2]          # docs/
OUT_DIR = ROOT / "presentation" / "assets"

# ── Canvas geometry ──────────────────────────────────────────────────────────
W, H = 1180, 860
# Layout is checked by tools/verify_usecase_layout.py: the pins column ends at
# x=584 and the ovals must stay fully inside the boundary (596 -> 1048).
BOUNDARY = (268, 92, 800, 748)      # x, y, w, h of the «system» boundary box
UC_CX = 822                          # use-case column centre (right of the pins)
UC_RX, UC_RY = 226, 30
ROW_TOP, ROW_GAP = 152, 96

# ── Palette (mirrors assets/style.css tokens) ────────────────────────────────
RED, RED_BG, RED_DARK, RED_TINT = "#dc2626", "#fee2e2", "#991b1b", "#fff5f5"
GREEN, GREEN_BG, GREEN_DARK, GREEN_TINT = "#16a34a", "#dcfce7", "#14532d", "#f6fef9"
BLUE, BLUE_BG, BLUE_DARK = "#2563eb", "#dbeafe", "#1e40af"
SLATE, SLATE_DIM, LINE = "#0f172a", "#475569", "#cbd5e1"
FONT = "Inter, 'DejaVu Sans', 'Segoe UI', Arial, sans-serif"


def esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def tspan_lines(lines: list[str], x: float, y: float, size: float,
                weight, fill: str, leading: float = 13.5,
                anchor: str = "middle") -> str:
    spans = "".join(
        f'<tspan x="{x}" y="{y + i * leading}">{esc(line)}</tspan>'
        for i, line in enumerate(lines)
    )
    return (f'<text text-anchor="{anchor}" font-family="{FONT}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}">{spans}</text>')


def _wrap(text: str, limit: int) -> list[str]:
    words, lines, cur = text.split(), [], ""
    for word in words:
        if len(cur) + len(word) + 1 <= limit:
            cur = f"{cur} {word}".strip()
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ── Layout helpers ───────────────────────────────────────────────────────────
def uc_center(uc: UseCase) -> tuple[float, float]:
    return UC_CX, ROW_TOP + uc.order * ROW_GAP


def _primary_order(model: Model, actor_key: str) -> int:
    for uc in model.usecases:
        if uc.actor == actor_key:
            return uc.order
    for uc in model.usecases:
        for key, _ in uc.links:
            if key == actor_key:
                return uc.order
    return 0


def actor_pos(model: Model, actor_key: str) -> tuple[float, float]:
    """Actor anchor (x, y) on the left rail, aligned to the row it drives."""
    lane = next((a.lane for a in model.actors if a.key == actor_key), 0)
    return 104.0, ROW_TOP + lane * ROW_GAP


def ellipse_edge(cx: float, cy: float, tx: float, ty: float) -> tuple[float, float]:
    """Where the ray centre->(tx,ty) meets the use-case ellipse rim."""
    dx, dy = tx - cx, ty - cy
    if dx == 0 and dy == 0:
        return cx + UC_RX, cy
    scale = 1.0 / ((dx / UC_RX) ** 2 + (dy / UC_RY) ** 2) ** 0.5
    return cx + dx * scale, cy + dy * scale


# ── SVG primitives ───────────────────────────────────────────────────────────
def actor_svg(x: float, y: float, name: str, role: str, kind: str) -> str:
    hw = actor_box_halfwidth(name, role)
    if kind == "system":
        return f'''
  <g transform="translate({x:.0f}, {y:.0f})">
    <rect x="-27" y="-25" width="54" height="54" rx="9" fill="{BLUE_BG}" stroke="{BLUE}" stroke-width="2.2"/>
    <circle cx="0" cy="2" r="10" fill="none" stroke="{BLUE_DARK}" stroke-width="2"/>
    <g stroke="{BLUE_DARK}" stroke-width="2" stroke-linecap="round">
      <line x1="0" y1="-8" x2="0" y2="-16"/><line x1="0" y1="12" x2="0" y2="20"/>
      <line x1="-10" y1="2" x2="-18" y2="2"/><line x1="10" y1="2" x2="18" y2="2"/>
    </g>
    <rect x="{-hw:.1f}" y="38" width="{2 * hw:.1f}" height="31" rx="6" fill="#eff6ff" stroke="{BLUE}" stroke-width="1.1"/>
    <text x="0" y="53" text-anchor="middle" font-family="{FONT}" font-size="11.5" font-weight="700" fill="{BLUE_DARK}">{esc(name)}</text>
    <text x="0" y="64" text-anchor="middle" font-family="{FONT}" font-size="9.5" font-weight="600" fill="{BLUE}">{esc(role)}</text>
  </g>'''
    return f'''
  <g transform="translate({x:.0f}, {y:.0f})">
    <circle cx="0" cy="-30" r="12.5" fill="#ffffff" stroke="{SLATE}" stroke-width="2.2"/>
    <line x1="0" y1="-17.5" x2="0" y2="15" stroke="{SLATE}" stroke-width="2.2"/>
    <line x1="-17" y1="-7" x2="17" y2="-7" stroke="{SLATE}" stroke-width="2.2"/>
    <line x1="0" y1="15" x2="-14" y2="37" stroke="{SLATE}" stroke-width="2.2"/>
    <line x1="0" y1="15" x2="14" y2="37" stroke="{SLATE}" stroke-width="2.2"/>
    <rect x="{-hw:.1f}" y="46" width="{2 * hw:.1f}" height="31" rx="6" fill="#f8fafc" stroke="{LINE}" stroke-width="1"/>
    <text x="0" y="61" text-anchor="middle" font-family="{FONT}" font-size="11.5" font-weight="700" fill="{SLATE}">{esc(name)}</text>
    <text x="0" y="72" text-anchor="middle" font-family="{FONT}" font-size="9.5" font-weight="600" fill="{SLATE_DIM}">{esc(role)}</text>
  </g>'''


def actor_box_halfwidth(name: str, role: str) -> float:
    """Half-width of the actor label box.

    Must fit BOTH lines: the name renders at 11.5px and the role at 9.5px.
    Approximate advance widths for Inter/DejaVu Sans are ~0.60em and ~0.58em.
    """
    name_px = 11.5 * 0.60 * len(name)
    role_px = 9.5 * 0.58 * len(role)
    return max(84.0, max(name_px, role_px) / 2 + 18)


def label_pill(x: float, y: float, text: str) -> str:
    w = 8.8 * len(text) + 20
    return (f'<rect x="{x - w / 2:.1f}" y="{y - 9:.1f}" width="{w:.1f}" height="18" rx="4" '
            f'fill="#ffffff" stroke="{BLUE}" stroke-width="1"/>'
            + tspan_lines([text], x, y + 4, 9.5, 700, BLUE))


def relation_svg(rel: str, x1: float, y1: float, x2: float, y2: float) -> str:
    if rel == "assoc":
        return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                f'stroke="{SLATE_DIM}" stroke-width="1.6"/>')
    stereotype = "<<include>>" if rel == "include" else "<<extend>>"
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{BLUE}" stroke-width="1.5" stroke-dasharray="5,4" marker-end="url(#arrow)"/>'
        + label_pill((x1 + x2) / 2, (y1 + y2) / 2, stereotype)
    )


def usecase_node(uc: UseCase, mode: str) -> str:
    cx, cy = uc_center(uc)
    if mode == "as-is":
        is_hot = uc.bottleneck is not None
        fill, stroke, text = (RED_BG, RED, RED_DARK) if is_hot else ("#f8fafc", LINE, SLATE_DIM)
        sw = 2.4 if is_hot else 1.6
    else:
        fill, stroke, text, sw = GREEN_BG, GREEN, GREEN_DARK, 2.2

    label = f"{uc.code}: {uc.name}"
    # Two balanced lines keep the label inside the 472px-wide ellipse.
    if len(label) > 34:
        cut = label.rfind(" ", 0, (len(label) + 1) // 2 + 6)
        head, tail = (label[:cut], label[cut + 1:]) if cut > 12 else (label, "")
    else:
        head, tail = label, ""
    rows = [head, tail] if tail else [head]
    body = tspan_lines(rows, cx, cy + (5 if not tail else -2), 12.5, 750, text, leading=15)
    return (f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{UC_RX}" ry="{UC_RY}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>{body}')


def callout(uc: UseCase, mode: str) -> str:
    if mode == "as-is" and not uc.bottleneck:
        return ""
    if mode == "to-be" and not uc.solution:
        return ""

    _, cy = uc_center(uc)
    if mode == "as-is":
        accent, bg, dark = RED, RED_BG, RED_DARK
        title = f"[{uc.bottleneck}] {uc.b_title.split(' - ', 1)[-1]}"
        detail, cause = uc.b_evidence, uc.b_cause
    else:
        accent, bg, dark = GREEN, GREEN_BG, GREEN_DARK
        title = uc.s_title.split(" - ", 1)[-1]
        detail, cause = uc.s_evidence, ""

    x, y, w, h = 316, cy - 34, 268, 68
    rows = [title] + _wrap(detail, 40) + (_wrap(cause, 42) if cause else [])
    text = tspan_lines(rows[:4], x + 14, y + 16, 9.5, 700, dark, leading=13, anchor="start")
    stripe = f'<rect x="{x:.0f}" y="{y:.0f}" width="5" height="{h}" rx="2.5" fill="{accent}"/>'
    return (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w}" height="{h}" rx="7" '
            f'fill="{bg}" stroke="{accent}" stroke-width="1.3"/>{stripe}{text}')


def legend_svg() -> str:
    y = H - 34
    entries = [
        (RED, "Bottleneck terbukti dari data"),
        (SLATE_DIM, "Langkah tanpa hambatan"),
        (GREEN, "Langkah solusi terusulkan"),
        (BLUE, "Aktor sistem / relasi UML"),
    ]
    # Measure with real font metrics (9.5px bold ~= 0.60em advance) and keep
    # the whole group strictly inside the 286..1126 legend bar.
    chip_w, text_adv = 15.0, 9.5 * 0.60
    used = sum(chip_w + 6 + text_adv * len(text) for _, text in entries)
    gap = max(12.0, (840 - 24 - used) / (len(entries) - 1))
    chips, x = [], 298.0
    for color, text in entries:
        chips.append(f'<rect x="{x:.1f}" y="{y - 9}" width="15" height="11" rx="3" fill="{color}"/>')
        chips.append(f'<text x="{x + 21:.1f}" y="{y}" font-family="{FONT}" font-size="9.5" '
                     f'font-weight="700" fill="{SLATE_DIM}">{text}</text>')
        x += chip_w + 6 + text_adv * len(text) + gap
    return (f'<rect x="286" y="{y - 22}" width="840" height="34" rx="8" fill="#f8fafc" '
            f'stroke="{LINE}" stroke-width="1"/>' + "".join(chips))


# ── Whole diagram ────────────────────────────────────────────────────────────
def render(model: Model, mode: str) -> str:
    bx, by, bw, bh = BOUNDARY
    accent = RED if mode == "as-is" else GREEN
    tint = RED_TINT if mode == "as-is" else GREEN_TINT
    hot = bottleneck_count(model) if mode == "as-is" else solution_count(model)
    badge = f"{hot} TITIK BOTTLENECK" if mode == "as-is" else f"{hot} SOLUSI TERINTEGRASI"

    lines: list[str] = []
    for uc in model.usecases:
        ucx, ucy = uc_center(uc)
        for actor_key, rel in uc.links:
            if actor_key not in {a.key for a in model.actors}:
                continue
            actor = next(a for a in model.actors if a.key == actor_key)
            ax, ay = actor_pos(model, actor_key)
            side = ax + actor_box_halfwidth(actor.name, actor.role)   # real box edge
            # Keep every association inside its OWN row band: a long diagonal
            # from a distant actor row would slice through the ovals between.
            ally = ay if ay == ucy else min(max(ay, ucy - UC_RY + 8), ucy + UC_RY - 8)
            ex, ey = ellipse_edge(ucx, ucy, side, ally)
            if ally == ay:
                lines.append(relation_svg(rel, side, ay, ex, ey))
                continue
            # Elbow route: horizontal into the lane, vertical, then into the rim.
            # The UML semantics (solid assoc vs dashed «include»/«extend» with an
            # arrowhead) MUST survive this branch too — that was the old bug.
            bend = UC_CX - UC_RX - 26
            if rel == "assoc":
                lines.append(
                    f'<polyline points="{side:.1f},{ay:.1f} {bend:.1f},{ay:.1f} '
                    f'{bend:.1f},{ally:.1f} {ex:.1f},{ally:.1f}" fill="none" '
                    f'stroke="{SLATE_DIM}" stroke-width="1.6"/>')
            else:
                lines.append(
                    f'<polyline points="{side:.1f},{ay:.1f} {bend:.1f},{ay:.1f} '
                    f'{bend:.1f},{ally:.1f} {ex:.1f},{ally:.1f}" fill="none" '
                    f'stroke="{BLUE}" stroke-width="1.5" stroke-dasharray="5,4" '
                    f'marker-end="url(#arrow)"/>')
                stereotype = "<<include>>" if rel == "include" else "<<extend>>"
                lines.append(label_pill((side + bend) / 2, ay - 11, stereotype))

    actors = [actor_svg(*actor_pos(model, a.key), a.name, a.role, a.kind)
              for a in model.actors]
    nodes = [usecase_node(uc, mode) for uc in model.usecases]
    pins = [callout(uc, mode) for uc in model.usecases]

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="auto"
     role="img" aria-label="{esc(model.title)}"
     style="background:#ffffff;border-radius:12px;border:1px solid {LINE};box-shadow:0 3px 7px rgba(15,23,42,.08)">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="{BLUE}"/>
    </marker>
  </defs>

  <rect x="0" y="0" width="{W}" height="54" fill="{tint}"/>
  <text x="24" y="25" font-family="{FONT}" font-size="14.5" font-weight="800" fill="{accent}">DIAGRAM {esc(model.title)} &#183; BAHASA UML 2.5</text>
  <text x="24" y="43" font-family="{FONT}" font-size="10.5" font-weight="600" fill="{SLATE_DIM}">Sumber bukti: docs/cleaned_data/cleaned_tickets.csv &#183; 788 tiket operasional riil</text>
  <rect x="{W - 218}" y="16" width="194" height="23" rx="5" fill="{accent}"/>
  <text x="{W - 121}" y="31" text-anchor="middle" font-family="{FONT}" font-size="10.5" font-weight="800" fill="#ffffff">{badge}</text>

  <rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="14" fill="{tint}" stroke="{accent}" stroke-dasharray="8,5" stroke-width="2.2"/>
  <text x="{bx + 18}" y="{by + 26}" font-family="{FONT}" font-size="12" font-weight="800" fill="{accent}" letter-spacing="0.4">{esc(model.boundary_label)}</text>

  {''.join(lines)}
  {''.join(actors)}
  {''.join(nodes)}
  {''.join(pins)}
  {legend_svg()}
</svg>
'''


def render_comparison() -> str:
    width, height = W, 486
    col_l, col_r = 300, 760
    row_h, top = 52, 118
    rows = [f'''<rect x="{col_l - 152}" y="{top - 48}" width="304" height="30" rx="6" fill="{RED_BG}" stroke="{RED}" stroke-width="1.4"/>
  <text x="{col_l}" y="{top - 28}" text-anchor="middle" font-family="{FONT}" font-size="11.5" font-weight="800" fill="{RED_DARK}">AS-IS &#183; PROSES KONVENSIONAL</text>
  <rect x="{col_r - 152}" y="{top - 48}" width="304" height="30" rx="6" fill="{GREEN_BG}" stroke="{GREEN}" stroke-width="1.4"/>
  <text x="{col_r}" y="{top - 28}" text-anchor="middle" font-family="{FONT}" font-size="11.5" font-weight="800" fill="{GREEN_DARK}">TO-BE &#183; SISTEM TERUSULKAN</text>
  <rect x="{(col_l + col_r) / 2 - 96}" y="{top - 48}" width="192" height="30" rx="6" fill="#f8fafc" stroke="{LINE}"/>
  <text x="{(col_l + col_r) / 2}" y="{top - 28}" text-anchor="middle" font-family="{FONT}" font-size="11" font-weight="800" fill="{SLATE_DIM}">STATUS ELIMINASI</text>''']

    for i, (as_code, as_label, bottleneck, to_code, to_label, resolution) in enumerate(MAPPING):
        y = top + i * row_h
        is_hot = bottleneck != "-"
        left_fill, left_stroke = (RED_BG, RED) if is_hot else ("#f8fafc", LINE)
        rows.append(f'''
  <rect x="{col_l - 158}" y="{y}" width="316" height="42" rx="7" fill="{left_fill}" stroke="{left_stroke}" stroke-width="1.4"/>
  <text x="{col_l - 146}" y="{y + 18}" font-family="{FONT}" font-size="10.5" font-weight="800" fill="{RED_DARK}">{esc(as_code)}</text>
  <text x="{col_l - 146}" y="{y + 33}" font-family="{FONT}" font-size="9.5" font-weight="600" fill="{SLATE_DIM}">{esc(as_label)}</text>
  <rect x="{col_r - 158}" y="{y}" width="316" height="42" rx="7" fill="{GREEN_BG}" stroke="{GREEN}" stroke-width="1.4"/>
  <text x="{col_r - 146}" y="{y + 18}" font-family="{FONT}" font-size="10.5" font-weight="800" fill="{GREEN_DARK}">{esc(to_code)}</text>
  <text x="{col_r - 146}" y="{y + 33}" font-family="{FONT}" font-size="9.5" font-weight="600" fill="{SLATE_DIM}">{esc(to_label)}</text>
  <line x1="{col_l + 158}" y1="{y + 21}" x2="{col_r - 162}" y2="{y + 21}" stroke="{SLATE_DIM}" stroke-width="1.6" marker-end="url(#arrowG)"/>
  <rect x="{(col_l + col_r) / 2 - 96}" y="{y + 9}" width="192" height="24" rx="5" fill="#ffffff" stroke="{left_stroke}"/>
  <text x="{(col_l + col_r) / 2}" y="{y + 25}" text-anchor="middle" font-family="{FONT}" font-size="9.5" font-weight="800"
        fill="{RED if is_hot else SLATE_DIM}">{esc(bottleneck if is_hot else 'TANPA BOTTLENECK')} &#8594; {esc(resolution)}</text>''')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="auto"
     role="img" aria-label="Pemetaan use case konvensional ke sistem terusulkan"
     style="background:#ffffff;border-radius:12px;border:1px solid {LINE};box-shadow:0 3px 7px rgba(15,23,42,.08)">
  <defs>
    <marker id="arrowG" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="{SLATE_DIM}"/>
    </marker>
  </defs>
  <rect x="0" y="0" width="{width}" height="54" fill="#eef2f7"/>
  <text x="24" y="25" font-family="{FONT}" font-size="14.5" font-weight="800" fill="{SLATE}">PEMETAAN USE CASE: KONVENSIONAL (AS-IS) &#8594; TERUSULKAN (TO-BE)</text>
  <text x="24" y="43" font-family="{FONT}" font-size="10.5" font-weight="600" fill="{SLATE_DIM}">Setiap bottleneck B1&#8211;B4 dipetakan ke solusi S1&#8211;S6 yang mengeliminasinya</text>
  {''.join(rows)}
  <rect x="170" y="{height - 40}" width="840" height="28" rx="7" fill="#f8fafc" stroke="{LINE}"/>
  <text x="590" y="{height - 22}" text-anchor="middle" font-family="{FONT}" font-size="10" font-weight="700" fill="{SLATE_DIM}">Kotak merah = langkah terbukti bottleneck dari data &#183; Kotak abu = langkah tanpa hambatan terukur</text>
</svg>
'''


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    outputs = {
        "diagram_legacy_usecase.svg": render(AS_IS, "as-is"),
        "diagram_proposed_usecase.svg": render(TO_BE, "to-be"),
        "diagram_usecase_comparison.svg": render_comparison(),
    }
    for name, svg in outputs.items():
        path = OUT_DIR / name
        path.write_text(svg, encoding="utf-8")
        print(f"OK  {path.relative_to(ROOT.parent)}  ({path.stat().st_size / 1024:.1f} KB)")
    print(f"    AS-IS bottlenecks={bottleneck_count(AS_IS)} / TO-BE solutions={solution_count(TO_BE)}")


if __name__ == "__main__":
    main()