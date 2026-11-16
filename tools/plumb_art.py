"""Shared plumbline artwork: the five layers lighting in turn, and a swinging plumb bob."""


def plumb_art(p, ox, oy, bob=218):
    rows = ["data", "retrieve", "validate", "failures", "evals"]
    o = []
    for i, name in enumerate(rows):
        y = oy + i * 26
        a, b = 0.06 + i * 0.13, 0.10 + i * 0.13
        kt = f"0;{a:.2f};{b:.2f};0.92;1"
        o.append(f'<text x="{ox}" y="{y + 11}" class="mono" font-size="12" fill="{p["mute"]}">{name}</text>'
                 f'<rect x="{ox + 72}" y="{y + 4}" width="70" height="14" rx="2" fill="none" stroke="{p["nm"]}" stroke-opacity="0.4"/>'
                 f'<path d="M{ox + 138} {y}l4 4M{ox + 138} {y + 14}l4 4M{ox + 68} {y + 14}l4 4" stroke="{p["nm"]}" stroke-opacity="0.5" fill="none"/>'
                 f'<rect x="{ox + 68}" y="{y}" width="70" height="14" rx="2" fill="{p["chip"]}" stroke="{p["nm"]}" stroke-width="1.5"/>'
                 f'<rect x="{ox + 70}" y="{y + 2}" width="66" height="10" rx="1" fill="{p["green"]}" opacity="0"><animate attributeName="opacity" values="0;0;0.85;0.85;0" keyTimes="{kt}" dur="6s" repeatCount="indefinite"/></rect>'
                 f'<path d="M{ox + 152} {y + 7}l4 4 7-8" fill="none" stroke="{p["green"]}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" opacity="0.2"><animate attributeName="opacity" values="0.2;0.2;1;1;0.2" keyTimes="{kt}" dur="6s" repeatCount="indefinite"/></path>')
    ax, ay, L = ox + bob, oy - 14, 96
    o.append(f'<path d="M{ax} {ay}V{ay + 152}" stroke="{p["dim"]}" stroke-width="1" stroke-dasharray="3 5"/>'
             f'<path d="M{ax - 22} {ay}H{ax + 22}" stroke="{p["ink"]}" stroke-width="2" stroke-linecap="round"/>'
             f'<g><animateTransform attributeName="transform" type="rotate" values="-6 {ax} {ay};6 {ax} {ay};-6 {ax} {ay}" keyTimes="0;0.5;1" calcMode="spline" keySplines="0.45 0 0.55 1;0.45 0 0.55 1" dur="3.4s" repeatCount="indefinite"/>'
             f'<path d="M{ax} {ay}V{ay + L}" stroke="{p["ink"]}" stroke-width="1.4"/>'
             f'<path d="M{ax + 4} {ay + L + 4}l10 12-10 30-10-30z" fill="none" stroke="{p["nm"]}" stroke-opacity="0.45"/>'
             f'<path d="M{ax + 10} {ay + L + 12}l4 4M{ax} {ay + L + 42}l4 4" stroke="{p["nm"]}" stroke-opacity="0.5" fill="none"/>'
             f'<rect x="{ax - 5}" y="{ay + L - 4}" width="10" height="6" fill="{p["chip"]}" stroke="{p["nm"]}" stroke-width="1.4"/>'
             f'<path d="M{ax} {ay + L}l10 12-10 30-10-30z" fill="{p["chip"]}" stroke="{p["nm"]}" stroke-width="1.6" stroke-linejoin="round"/>'
             f'<path d="M{ax} {ay + L + 2}V{ay + L + 38}" stroke="{p["nm"]}" stroke-opacity="0.5"/></g>')
    return "".join(o)
