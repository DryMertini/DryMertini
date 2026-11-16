#!/usr/bin/env python3
"""Generates the profile SVGs in dark and light variants (3D / wireframe style)."""
import os, sys
from letters import word
from robot import cables, robot
from plumb_art import plumb_art

OUT = sys.argv[1] if len(sys.argv) > 1 else "out"
os.makedirs(OUT, exist_ok=True)

PAL = {
    "dark": dict(fg="#f0f6fc", fg2="#aeb8c4", mute="#9da7b3", dim="#6e7681", line="#262c35",
                 gold="#e3aa3f", hot="#c9742a", deep="#3a1c06", ink="#c9d1d9", nm="#d9a441", spark="#fff1c9", green="#3fb950",
                 chip="#161b22", chip2="#0d1117", glow=0.16, grid=0.5),
    "light": dict(fg="#0d1117", fg2="#3d4651", mute="#57606a", dim="#8c959f", line="#d0d7de",
                  gold="#9a6700", hot="#bc6c25", deep="#f0d2a6", ink="#24292f", nm="#9a6700", spark="#ffd98a", green="#1a7f37",
                  chip="#ffffff", chip2="#f3f5f8", glow=0.10, grid=0.55),
}
STYLE = """<style>
.sans{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}
.mono{font-family:ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,"Liberation Mono",monospace}
</style>"""


def lerp(c1, c2, t):
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(a[i] + (b[i] - a[i]) * t):02x}" for i in range(3))


def common(p):
    return f'''{STYLE}
<linearGradient id="go" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{p['gold']}"/><stop offset="1" stop-color="{p['hot']}"/></linearGradient>
<linearGradient id="fgv" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{p['fg']}"/><stop offset="1" stop-color="{p['fg2']}"/></linearGradient>
<filter id="glow" x="-20%" y="-40%" width="140%" height="180%"><feGaussianBlur stdDeviation="5"/></filter>
<filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2.2"/></filter>'''


def svg(w, h, label, p, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{label}">\n<defs>{common(p)}</defs>\n{body}\n</svg>\n')


def block(text, attrs, n, p, step=1.0):
    """Solid 3D extrusion: filled copies stepping down-right, shaded front to back."""
    out = []
    for i in range(n, 0, -1):
        c = lerp(p["hot"], p["deep"], (i - 1) / max(n - 1, 1))
        out.append(f'<text {attrs} transform="translate({i * step:.1f} {i * step:.1f})" fill="{c}" stroke="{c}" stroke-width="1" stroke-linejoin="round">{text}</text>')
    return "\n".join(out)


def wire(text, attrs, n, step, stroke, sw=1.1, o0=0.6):
    """Wireframe extrusion: offset outline copies, fading with depth."""
    out = []
    for i in range(n, 0, -1):
        o = o0 * (1 - (i - 1) / n) ** 1.4
        out.append(f'<text {attrs} transform="translate({i * step:.1f} {i * step:.1f})" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-opacity="{o:.2f}">{text}</text>')
    return "\n".join(out)


def header(p):
    lanes = [("orchestration", 1.3, 0.0, 0.55), ("agents", 1.7, 0.6, 0.5), ("pipelines", 0.9, 0.2, 0.6),
             ("automation", 1.1, 0.7, 0.6), ("web3", 1.9, 1.1, 0.5)]
    b = []
    b.append(f'''<defs>
<linearGradient id="comet" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{p['hot']}" stop-opacity="0"/><stop offset="0.7" stop-color="{p['gold']}"/><stop offset="1" stop-color="{p['spark']}"/></linearGradient>
<radialGradient id="halo" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{p['gold']}" stop-opacity="{p['glow']}"/><stop offset="1" stop-color="{p['gold']}" stop-opacity="0"/></radialGradient>
<linearGradient id="floorfade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.35" stop-color="#fff" stop-opacity="0.9"/><stop offset="1" stop-color="#fff"/></linearGradient>
<mask id="floor"><rect x="420" y="276" width="430" height="116" fill="url(#floorfade)"/></mask>
<clipPath id="lanes"><rect x="566" y="60" width="244" height="200"/></clipPath>
</defs>''')
    # cable fan + the robot that feeds on it
    HX, HY = 635, 410
    b.append(cables(p, HX, HY, 504))
    b.append(robot(p, HX, HY, 1.25))
    # handle + status
    b.append(f'''<g transform="translate(3 9)" fill="none" stroke="{p['gold']}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
<path d="M0 0H24L12 14Z"/><path d="M12 14V25M5 25H19"/><path d="M21 -6L14 6" stroke="{p['mute']}"/>
<circle cx="15" cy="5" r="2.4" fill="{p['green']}" stroke="none"/></g>
<text x="40" y="30" class="mono" font-size="15" fill="{p['gold']}">DryMertini</text>
<circle cx="766" cy="25" r="7" fill="{p['green']}" filter="url(#soft)"><animate attributeName="opacity" values="0.6;0.05;0.6" dur="1.4s" repeatCount="indefinite"/></circle>
<circle cx="766" cy="25" r="4" fill="{p['green']}"/>
<text x="846" y="30" class="mono" font-size="13" fill="{p['mute']}" text-anchor="end">building</text>''')
    # name: blueprint lettering (outlines only, shallow wireframe depth, joints on ASLAN)
    guides = "".join(f'<path d="M0 {gy}H432" stroke="{p["line"]}" stroke-width="1" stroke-dasharray="4 5"/>' for gy in (52, 142, 160, 250))
    marks = "".join(f'<path d="M{gx - 4} {gy}h8M{gx} {gy - 4}v8" stroke="{p["dim"]}" stroke-width="1"/>' for gx in (436,) for gy in (52, 142, 160, 250))
    b.append(guides + marks)
    b.append(word("MERT", 0, 52, 0.9, p["ink"], 1.6, depth=6, back_op=0.5, link_op=0.6))
    b.append(word("ASLAN", 0, 160, 0.9, p["nm"], 1.6, depth=6, back_op=0.5, link_op=0.6, nodes=True, node_color=p["green"]))
    b.append(f'<path d="M0 44V258" stroke="{p["green"]}" stroke-width="1" stroke-opacity="0.55"><animateTransform attributeName="transform" type="translate" values="0 0;416 0;0 0" dur="7s" repeatCount="indefinite"/></path>')
    b.append(f'<text x="0" y="300" class="sans" font-size="20" fill="{p["mute"]}">Full-stack developer · AI agents &amp; pipelines</text>')
    # typed line
    phrases = ["builds AI agents that ship", "wires pipelines end to end", "full-stack, from UI to chain"]
    cw, slot, T, x0, ty = 9.65, 3.2, 9.6, 22, 336
    b.append(f'<text x="0" y="{ty}" class="mono" font-size="16" fill="{p["gold"]}">&gt;</text>')
    cur_t, cur_x = [], []
    for i, ph in enumerate(phrases):
        n = len(ph)
        t0 = i * slot
        times, widths = [0.0], [0.0]
        for k in range(1, n + 1):
            times.append(t0 + 0.2 + k * (1.0 / n))
            widths.append(k * cw + 2)
        times.append(t0 + slot - 0.15)
        widths.append(0.0)
        kt = ";".join(f"{t / T:.4f}" for t in times)
        wv = ";".join(f"{w:.1f}" for w in widths)
        b.append(f'''<clipPath id="t{i}"><rect x="{x0}" y="{ty - 20}" width="0" height="28"><animate attributeName="width" calcMode="discrete" values="{wv}" keyTimes="{kt}" dur="{T}s" repeatCount="indefinite"/></rect></clipPath>
<text x="{x0}" y="{ty}" class="mono" font-size="16" fill="{p['fg']}" clip-path="url(#t{i})" textLength="{n * cw:.1f}" lengthAdjust="spacingAndGlyphs">{ph}</text>''')
        cur_t += times[1:] if i else times
        cur_x += [x0 + w for w in (widths[1:] if i else widths)]
    kt = ";".join(f"{t / T:.4f}" for t in cur_t)
    xv = ";".join(f"{x + 3:.1f}" for x in cur_x)
    b.append(f'''<rect x="{x0}" y="{ty - 15}" width="9" height="18" fill="{p['gold']}"><animate attributeName="x" calcMode="discrete" values="{xv}" keyTimes="{kt}" dur="{T}s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="0.8s" repeatCount="indefinite"/></rect>''')
    # lanes
    for i, (name, dur, beg, hit) in enumerate(lanes):
        y = 84 + i * 40
        anim = f'<animate attributeName="x" values="456;810;810" keyTimes="0;{hit};1" dur="{dur}s" begin="-{beg}s" repeatCount="indefinite"/>'
        b.append(f'''<text x="452" y="{y + 5}" class="mono" font-size="13" fill="{p['mute']}">{name}</text>
<path d="M571 {y + 5}H815M566 {y}l5 5M810 {y}l5 5" stroke="{p['nm']}" stroke-opacity="0.35" stroke-width="1" fill="none"/>
<path d="M566 {y}H810" stroke="{p['line']}" stroke-width="2"/>
<g clip-path="url(#lanes)"><rect y="{y - 5}" width="110" height="10" rx="5" fill="url(#comet)" opacity="0.7" filter="url(#soft)">{anim}</rect><rect y="{y - 2}" width="110" height="4" rx="2" fill="url(#comet)">{anim}</rect></g>
<path d="M822 {y}l5 5 9-10" fill="none" stroke="{p['green']}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" opacity="0.3"><animate attributeName="opacity" values="0.3;0.3;1;0.3" keyTimes="0;{hit - 0.05:.2f};{hit + 0.02:.2f};1" dur="{dur}s" begin="-{beg}s" repeatCount="indefinite"/></path>''')
    return svg(850, 508, "Mert Aslan, DryMertini. Full-stack developer, AI agents and pipelines.", p, "\n".join(b))


def loading(p):
    chips = ["Kubernetes", "Cloud infrastructure as code", "Cloud identity & access", "Observability"]
    W, H, D = 836, 176, 9
    b = []
    dots = "".join(f'<tspan opacity="0.15">.<animate attributeName="opacity" values="0.15;1;0.15" dur="0.9s" begin="-{0.9 - i * 0.3:.1f}s" repeatCount="indefinite"/></tspan>' for i in range(3))
    corners = "".join(f"M{x} {y}l{D} {D}" for x, y in ((W - 3, 5), (W + 1, H - 11), (W - 11, H + 1), (5, H - 3)))
    b.append(f'''<defs><clipPath id="bar"><rect x="24" y="150" width="{W - 48}" height="3" rx="1.5"/></clipPath>
<linearGradient id="cardf" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{p['chip']}"/><stop offset="1" stop-color="{p['chip2']}"/></linearGradient></defs>
<rect x="{1 + D}" y="{1 + D}" width="{W}" height="{H}" rx="14" fill="none" stroke="{p['nm']}" stroke-opacity="0.4" stroke-width="1"/>
<path d="{corners}" stroke="{p['nm']}" stroke-opacity="0.5" stroke-width="1" fill="none"/>
<rect x="1" y="1" width="{W}" height="{H}" rx="14" fill="url(#cardf)" stroke="{p['nm']}" stroke-opacity="0.75" stroke-width="1.5"/>
<text x="24" y="36" class="mono" font-size="14" fill="{p['nm']}">loading{dots}</text>
<text x="23" y="74" class="sans" font-size="28" font-weight="800" letter-spacing="-0.8" fill="{p['fg']}">Going deep on cloud infrastructure</text>''')
    x = 24
    for i, c in enumerate(chips):
        w = round(len(c) * 7.9 + 40)
        b.append(f'''<g transform="translate({x} 94)"><rect x="4" y="4" width="{w}" height="32" rx="16" fill="none" stroke="{p['nm']}" stroke-opacity="0.4" stroke-width="1"/>
<rect x="0" y="0" width="{w}" height="32" rx="16" fill="{p['chip2']}" stroke="{p['line']}" stroke-width="1.5"/>
<circle cx="16" cy="16" r="3.2" fill="{p['nm']}"><animate attributeName="opacity" values="1;0.25;1" dur="1.6s" begin="-{i * 0.4:.1f}s" repeatCount="indefinite"/></circle>
<text x="27" y="20.5" class="mono" font-size="13" fill="{p['fg']}">{c.replace("&", "&amp;")}</text></g>''')
        x += w + 12
    b.append(f'''<rect x="24" y="150" width="{W - 48}" height="3" rx="1.5" fill="{p['line']}"/>
<g clip-path="url(#bar)"><rect x="-200" y="150" width="200" height="3" fill="{p['nm']}"><animate attributeName="x" values="-200;{W}" dur="1.8s" repeatCount="indefinite"/></rect></g>''')
    return svg(W + D + 3, H + D + 3, "Loading: going deep on cloud infrastructure. Kubernetes, cloud infrastructure as code, cloud identity and access, observability.", p, "\n".join(b))


def card(p, num, title, l1, l2, tags, art, label):
    t = 'x="23" y="94" class="sans" font-size="40" font-weight="900" letter-spacing="-1.5"'
    plates = "".join(f'<rect x="{1 + k * 2}" y="{1 + k * 2}" width="400" height="200" rx="14" fill="{lerp(p["hot"], p["deep"], k / 6)}" fill-opacity="0.9"/>' for k in range(6, 0, -1))
    b = f'''<defs><linearGradient id="cardf" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{p['chip']}"/><stop offset="1" stop-color="{p['chip2']}"/></linearGradient>
<linearGradient id="edge" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{p['gold']}"/><stop offset="0.6" stop-color="{p['hot']}" stop-opacity="0.5"/><stop offset="1" stop-color="{p['hot']}" stop-opacity="0"/></linearGradient></defs>
{plates}
<rect x="1" y="1" width="400" height="200" rx="14" fill="url(#cardf)" stroke="url(#go)" stroke-opacity="0.7" stroke-width="1.5"/>
<path d="M15 1H260" stroke="url(#edge)" stroke-width="2.5" stroke-linecap="round"/>
<text x="24" y="38" class="mono" font-size="11" letter-spacing="1.5" fill="{p['dim']}">{num} / HACKATHON BUILD</text>
<path d="M366 26h12v12M378 26l-13 13" fill="none" stroke="{p['gold']}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
<text {t} fill="{p['fg']}">{title}</text>
<text x="24" y="128" class="sans" font-size="14" fill="{p['mute']}">{l1}</text>
<text x="24" y="148" class="sans" font-size="14" fill="{p['mute']}">{l2}</text>
<text x="24" y="182" class="mono" font-size="12" fill="{p['gold']}">{tags}</text>
{art}'''
    return svg(416, 216, label, p, b)


def autark(p):
    nodes = [(314, 58), (372, 90), (306, 112)]
    edges = [(0, 1), (1, 2), (2, 0)]
    a = []
    for i, (s, e) in enumerate(edges):
        (x1, y1), (x2, y2) = nodes[s], nodes[e]
        a.append(f'<path d="M{x1} {y1}L{x2} {y2}" stroke="url(#go)" stroke-opacity="0.45" stroke-width="1.5"/>')
        for col, r, d, bg, path in [(p["spark"], 3.5, 0.9 + i * 0.25, i * 0.3, f"M{x1} {y1}L{x2} {y2}"),
                                    (p["green"], 2.8, 1.3 + i * 0.2, i * 0.5, f"M{x2} {y2}L{x1} {y1}")]:
            a.append(f'<circle r="{r + 3}" fill="{col}" opacity="0.6" filter="url(#soft)"><animateMotion path="{path}" dur="{d}s" begin="-{bg}s" repeatCount="indefinite"/></circle>'
                     f'<circle r="{r}" fill="{col}"><animateMotion path="{path}" dur="{d}s" begin="-{bg}s" repeatCount="indefinite"/></circle>')
    for i, (x, y) in enumerate(nodes):
        a.append("".join(f'<circle cx="{x + k}" cy="{y + k}" r="11" fill="{lerp(p["hot"], p["deep"], k / 4)}"/>' for k in range(4, 0, -1))
                 + f'<circle cx="{x}" cy="{y}" r="11" fill="{p["chip2"]}" stroke="url(#go)" stroke-width="2"/>'
                 f'<circle cx="{x}" cy="{y}" r="3" fill="{p["gold"]}"/>'
                 f'<circle cx="{x}" cy="{y}" r="11" fill="none" stroke="{p["gold"]}" stroke-width="1.5"><animate attributeName="r" values="11;22" dur="1.6s" begin="-{i * 0.5}s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.7;0" dur="1.6s" begin="-{i * 0.5}s" repeatCount="indefinite"/></circle>')
    return card(p, "02", "Autark", "Agent-to-agent trading floor on Solana,", "settled with x402 micropayments.",
                "TypeScript · Solana · x402", "\n".join(a), "Autark: agent-to-agent trading floor on Solana with x402 micropayments.")


def pastport(p):
    cx, cy, dx, dy = 326, 54, 52, 28
    a = []
    # slab under the grid
    for k in range(8, 0, -1):
        c = lerp(p["hot"], p["deep"], k / 8)
        a.append(f'<path d="M{cx} {cy + k}l{dx} {dy}l{-dx} {dy}l{-dx} {-dy}z" fill="{c}"/>')
    a.append(f'<path d="M{cx} {cy}l{dx} {dy}l{-dx} {dy}l{-dx} {-dy}z" fill="{p["chip2"]}" stroke="url(#go)" stroke-width="1.5"/>')
    for k in range(1, 4):
        t = k / 4
        a.append(f'<path d="M{cx - dx * t:.1f} {cy + dy * t:.1f}l{dx} {dy}M{cx + dx * t:.1f} {cy + dy * t:.1f}l{-dx} {dy}" stroke="url(#go)" stroke-opacity="0.5" stroke-width="1.1"/>')
    sweep = f'<animateTransform attributeName="transform" type="translate" values="0 0;{-dx} {dy};0 0" dur="1.8s" repeatCount="indefinite"/>'
    a.append(f'<path d="M{cx} {cy}l{dx} {dy}" stroke="{p["gold"]}" stroke-width="6" stroke-linecap="round" opacity="0.7" filter="url(#soft)">{sweep}</path>')
    a.append(f'<path d="M{cx} {cy}l{dx} {dy}" stroke="{p["spark"]}" stroke-width="2.2" stroke-linecap="round">{sweep}</path>')
    for i, (gx, gy, h) in enumerate([(0.25, 0.25, 22), (0.5, 0.75, 32), (0.75, 0.5, 16)]):
        bx = cx + dx * gx - dx * gy
        by = cy + dy * gx + dy * gy
        vals = f"M{bx:.1f} {by:.1f}v0;M{bx:.1f} {by:.1f}v-{h};M{bx:.1f} {by:.1f}v-{h};M{bx:.1f} {by:.1f}v0"
        an = f'<animate attributeName="d" values="{vals}" keyTimes="0;0.3;0.8;1" dur="3.6s" begin="-{i * 0.5}s" repeatCount="indefinite"/>'
        a.append(f'<path d="M{bx:.1f} {by:.1f}v0" stroke="{p["green"]}" stroke-width="12" stroke-linecap="round" opacity="0.5" filter="url(#soft)">{an}</path>'
                 f'<path d="M{bx:.1f} {by:.1f}v0" stroke="{p["green"]}" stroke-width="7" stroke-linecap="round">{an}</path>')
    return card(p, "03", "PastPort", "Scan a real place with LiDAR.", "Play it as a game, in VR or on desktop.",
                "JavaScript · 3D · VR", "\n".join(a), "PastPort: scan a real place with LiDAR and play it as a game in VR or on desktop.")


def plumbline(p):
    W, H = 834, 200
    plates = "".join(f'<rect x="{1 + k * 2}" y="{1 + k * 2}" width="{W}" height="{H}" rx="14" fill="{lerp(p["hot"], p["deep"], k / 6)}" fill-opacity="0.9"/>' for k in range(6, 0, -1))
    b = f'''<defs><linearGradient id="cardf" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{p['chip']}"/><stop offset="1" stop-color="{p['chip2']}"/></linearGradient>
<linearGradient id="edge" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{p['gold']}"/><stop offset="0.6" stop-color="{p['hot']}" stop-opacity="0.5"/><stop offset="1" stop-color="{p['hot']}" stop-opacity="0"/></linearGradient></defs>
{plates}
<rect x="1" y="1" width="{W}" height="{H}" rx="14" fill="url(#cardf)" stroke="url(#go)" stroke-opacity="0.7" stroke-width="1.5"/>
<path d="M15 1H360" stroke="url(#edge)" stroke-width="2.5" stroke-linecap="round"/>
<text x="24" y="38" class="mono" font-size="11" letter-spacing="1.5" fill="{p['dim']}">01 / SOLO BUILD</text>
<path d="M800 26h12v12M812 26l-13 13" fill="none" stroke="{p['gold']}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
<text x="23" y="92" class="sans" font-size="40" font-weight="900" letter-spacing="-1.5" fill="{p['fg']}">plumbline</text>
<text x="24" y="126" class="sans" font-size="14" fill="{p['mute']}">The 90% of an LLM app that isn't the LLM: data,</text>
<text x="24" y="146" class="sans" font-size="14" fill="{p['mute']}">retrieval, validation, failure handling and evals.</text>
<text x="24" y="182" class="mono" font-size="12" fill="{p['gold']}">Python · RAG · fault injection · evals</text>
<text x="378" y="84" class="sans" font-size="34" font-weight="900" fill="{p['green']}">100%</text>
<text x="378" y="102" class="mono" font-size="11" fill="{p['mute']}">availability under</text>
<text x="378" y="116" class="mono" font-size="11" fill="{p['mute']}">injected faults</text>
<text x="378" y="158" class="sans" font-size="34" font-weight="900" fill="{p['green']}">0%</text>
<text x="446" y="146" class="mono" font-size="11" fill="{p['mute']}">poisoned</text>
<text x="446" y="160" class="mono" font-size="11" fill="{p['mute']}">answers served</text>
{plumb_art(p, 556, 50, 192)}'''
    return svg(W + 15, H + 15, "plumbline: the 90% of an LLM app that isn't the LLM. 100% availability and 0% poisoned answers under injected faults.", p, b)


def marquee(p):
    items = ["PYTHON", "C", "TYPESCRIPT", "JAVASCRIPT", "SQL", "REACT", "NEXT.JS", "SOLANA"]
    cw = 15.6
    parts, x = [], 0.0
    for i, it in enumerate(items):
        w = len(it) * cw
        base = f'x="{x:.1f}" y="36" class="sans" font-size="26" font-weight="900" textLength="{w:.1f}" lengthAdjust="spacingAndGlyphs"'
        if i % 2:
            parts.append(wire(it, base, 4, 1.0, p["nm"], 0.9, 0.45) + f'<text {base} fill="none" stroke="{p["nm"]}" stroke-width="1.2">{it}</text>')
        else:
            parts.append(wire(it, base, 4, 1.0, p["mute"], 0.9, 0.45) + f'<text {base} fill="{p["mute"]}">{it}</text>')
        x += w + 26
        parts.append(f'<path d="M{x + 3:.1f} 23l7 7-7 7-7-7z" fill="none" stroke="{p["nm"]}" stroke-opacity="0.4" stroke-width="1"/><path d="M{x:.1f} 20l7 7-7 7-7-7z" fill="none" stroke="{p["nm"]}" stroke-width="1.4"/>')
        x += 34
    row = "".join(parts)
    L = x
    b = f'''<defs><linearGradient id="fade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.12" stop-color="#fff"/><stop offset="0.88" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<mask id="m"><rect width="850" height="58" fill="url(#fade)"/></mask></defs>
<g mask="url(#m)"><path d="M0 1H850M0 57H850" stroke="url(#go)" stroke-opacity="0.5" stroke-width="1.2"/><g>{row}<g transform="translate({L:.1f} 0)">{row}</g>
<animateTransform attributeName="transform" type="translate" from="0 0" to="{-L:.1f} 0" dur="16s" repeatCount="indefinite"/></g></g>'''
    return svg(850, 58, "Stack: Python, C, TypeScript, JavaScript, SQL, React, Next.js, Solana.", p, b)



if __name__ == "__main__":
    for mode, p in PAL.items():
        for name, fn in [("header", header), ("loading", loading), ("plumbline", plumbline), ("autark", autark), ("pastport", pastport), ("stack", marquee)]:
            open(f"{OUT}/{name}-{mode}.svg", "w").write(fn(p))
    print("ok")
