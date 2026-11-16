"""Constructed outline lettering: each glyph is built from overlapping outlined pieces."""

T = 24  # stem thickness, cap height is 100


def rect(x, y, w, h):
    return ("poly", [(x, y), (x + w, y), (x + w, y + h), (x, y + h)])


def rrect(x, y, w, h, r):
    k = r * 0.29
    pts = [(x + k, y + k), (x + w - k, y + k), (x + w - k, y + h - k), (x + k, y + h - k)]
    d = (f"M{x + r} {y}H{x + w - r}A{r} {r} 0 0 1 {x + w} {y + r}V{y + h - r}A{r} {r} 0 0 1 {x + w - r} {y + h}"
         f"H{x + r}A{r} {r} 0 0 1 {x} {y + h - r}V{y + r}A{r} {r} 0 0 1 {x + r} {y}Z")
    return ("path", d, pts)


GLYPHS = {
    "M": (96, [rect(0, 0, T, 100), rect(72, 0, T, 100),
               ("poly", [(0, 0), (24, 0), (60, 78), (36, 78)]),
               ("poly", [(96, 0), (72, 0), (36, 78), (60, 78)])]),
    "E": (70, [rect(0, 0, T, 100), rect(0, 0, 70, 22), rect(0, 39, 60, 22), rect(0, 78, 70, 22)]),
    "R": (84, [rect(0, 0, T, 100),
               ("path", "M0 0H51A29 29 0 0 1 51 58H0Z", [(0, 0), (51, 0), (80, 29), (51, 58), (0, 58)]),
               ("path", "M24 22H50A7 7 0 0 1 50 36H24Z", [(24, 22), (50, 22), (50, 36), (24, 36)]),
               ("poly", [(30, 58), (56, 58), (84, 100), (58, 100)])]),
    "T": (78, [rect(0, 0, 78, 22), rect(27, 0, T, 100)]),
    "A": (92, [("poly", [(34, 0), (58, 0), (24, 100), (0, 100)]),
               ("poly", [(34, 0), (58, 0), (92, 100), (68, 100)]),
               rect(16, 60, 60, 20)]),
    "S": (74, [rrect(0, 0, 74, 22, 11), rrect(0, 0, 24, 61, 12), rrect(0, 39, 74, 22, 11),
               rrect(50, 39, 24, 61, 12), rrect(0, 78, 74, 22, 11)]),
    "L": (64, [rect(0, 0, T, 100), rect(0, 78, 64, 22)]),
    "N": (86, [rect(0, 0, T, 100), rect(62, 0, T, 100),
               ("poly", [(0, 0), (26, 0), (86, 100), (60, 100)])]),
}


def _flip(pieces):
    out = []
    for p in pieces:
        out.append(("poly", [(x, 100 - y) for x, y in p[1]]))
    return out


GLYPHS.update({
    "P": (80, [rect(0, 0, T, 100),
               ("path", "M0 0H51A29 29 0 0 1 51 58H0Z", [(0, 0), (51, 0), (80, 29), (51, 58), (0, 58)]),
               ("path", "M24 22H50A7 7 0 0 1 50 36H24Z", [(24, 22), (50, 22), (50, 36), (24, 36)])]),
    "U": (80, [rect(0, 0, T, 100), rect(56, 0, T, 100), rect(0, 78, 80, 22)]),
    "H": (80, [rect(0, 0, T, 100), rect(56, 0, T, 100), rect(0, 39, 80, 22)]),
    "W": (96, _flip(GLYPHS["M"][1])),
    "Z": (76, [rect(0, 0, 76, 22), rect(0, 78, 76, 22), ("poly", [(50, 0), (76, 0), (26, 100), (0, 100)])]),
    "I": (24, [rect(0, 0, T, 100)]),
    "G": (74, [rrect(0, 0, 74, 22, 11), rrect(0, 0, 24, 100, 12), rrect(0, 78, 74, 22, 11),
               rrect(50, 45, 24, 55, 12), rect(36, 45, 38, 20)]),
    "-": (40, [rect(0, 40, 40, 20)]),
    "_": (60, [rect(0, 80, 60, 20)]),
})


def word_width(word, gap=12):
    return sum(GLYPHS[c][0] for c in word) + gap * (len(word) - 1)


def _piece(p, ox, oy, s):
    if p[0] == "poly":
        pts = " ".join(f"{ox + x * s:.1f},{oy + y * s:.1f}" for x, y in p[1])
        return f'<polygon points="{pts}"/>'
    return f'<path transform="translate({ox:.1f} {oy:.1f}) scale({s})" d="{p[1]}" vector-effect="non-scaling-stroke"/>'


def word(text, x, y, s=1.0, color="#d9a441", sw=2, depth=0, back_op=0.35, link_op=0.5, nodes=False, gap=12, node_color=None):
    """Returns SVG for a word. depth>0 adds a back face and connecting edges (wireframe 3D)."""
    front, back, links, dots = [], [], [], []
    cx = x
    for ch in text:
        w, pieces = GLYPHS[ch]
        for p in pieces:
            front.append(_piece(p, cx, y, s))
            pts = p[1] if p[0] == "poly" else p[2]
            if depth:
                back.append(_piece(p, cx + depth, y + depth, s))
                for (px, py) in pts:
                    X, Y = cx + px * s, y + py * s
                    links.append(f"M{X:.1f} {Y:.1f}l{depth} {depth}")
            if nodes:
                for (px, py) in pts:
                    dots.append(f'<circle cx="{cx + px * s:.1f}" cy="{y + py * s:.1f}" r="2.4"/>')
        cx += (w + gap) * s
    out = f'<g fill="none" stroke="{color}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round">'
    if depth:
        out += f'<g stroke-opacity="{back_op}" stroke-width="{sw * 0.7:.1f}">{"".join(back)}</g>'
        out += f'<path stroke-opacity="{link_op}" stroke-width="{sw * 0.6:.1f}" d="{"".join(links)}"/>'
    out += "".join(front)
    out += "</g>"
    if nodes:
        out += f'<g fill="{node_color or color}">{"".join(dots)}</g>'
    return out
