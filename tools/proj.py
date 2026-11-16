#!/usr/bin/env python3
"""Headers for the Push_Swap and a-maze-ing READMEs (dark + light)."""
import os, random, sys
from letters import word, word_width
from gen import PAL, svg

OUT = sys.argv[1] if len(sys.argv) > 1 else "proj"
os.makedirs(OUT, exist_ok=True)


def frame(p, W, H, D=8):
    c = "".join(f"M{x} {y}l{D} {D}" for x, y in ((W - 3, 5), (W + 1, H - 11), (W - 11, H + 1), (5, H - 3)))
    return (f'<rect x="{1 + D}" y="{1 + D}" width="{W}" height="{H}" rx="14" fill="none" stroke="{p["nm"]}" stroke-opacity="0.4"/>'
            f'<path d="{c}" stroke="{p["nm"]}" stroke-opacity="0.5" fill="none"/>'
            f'<rect x="1" y="1" width="{W}" height="{H}" rx="14" fill="{p["chip2"]}" stroke="{p["nm"]}" stroke-opacity="0.75" stroke-width="1.5"/>')


def head(p, title, sub, tags):
    return (word(title, 28, 44, 0.5, p["nm"], 1.5, depth=5, back_op=0.5, link_op=0.6)
            + f'<text x="28" y="134" class="sans" font-size="17" fill="{p["mute"]}">{sub}</text>'
            + f'<text x="28" y="168" class="mono" font-size="12.5" fill="{p["nm"]}">{tags}</text>')


def push_swap(p):
    W, H = 838, 196
    vals = [3, 1, 5, 2, 4]
    states = [([3, 1, 5, 2, 4], []), ([1, 3, 5, 2, 4], []), ([3, 5, 2, 4], [1]), ([5, 2, 4, 3], [1]),
              ([3, 5, 2, 4], [1]), ([1, 3, 5, 2, 4], []), ([3, 1, 5, 2, 4], [])]
    ops = ["sa", "pb", "ra", "rra", "pa", "sa"]
    ax, bx, y0, row = 500, 668, 44, 22
    n = len(states) - 1
    kt = []
    for i in range(n):  # hold, then move
        kt += [i / n, (i + 0.55) / n]
    kt.append(1.0)
    art = [f'<text x="{ax}" y="32" class="mono" font-size="12" fill="{p["dim"]}">stack a</text><text x="{bx}" y="32" class="mono" font-size="12" fill="{p["dim"]}">stack b</text>',
           f'<path d="M{ax - 8} {y0 - 4}V{y0 + 5 * row}H{ax + 108}M{bx - 8} {y0 - 4}V{y0 + 5 * row}H{bx + 108}" fill="none" stroke="{p["line"]}" stroke-width="1.5"/>']
    for v in vals:
        pos = []
        for a, bb in states:
            pos.append((ax, y0 + a.index(v) * row) if v in a else (bx, y0 + bb.index(v) * row))
        seq = []
        for i in range(n):
            seq += [pos[i], pos[i]]
        seq.append(pos[n])
        tv = ";".join(f"{x} {y}" for x, y in seq)
        w = 22 + v * 15
        col = p["green"] if v == 1 else p["nm"]
        art.append(f'<g><animateTransform attributeName="transform" type="translate" values="{tv}" keyTimes="{";".join(f"{k:.3f}" for k in kt)}" dur="7.2s" repeatCount="indefinite"/>'
                   f'<rect x="4" y="4" width="{w}" height="14" rx="2" fill="none" stroke="{col}" stroke-opacity="0.45"/>'
                   f'<path d="M{w} 0l4 4M{w} 14l4 4M0 14l4 4" stroke="{col}" stroke-opacity="0.5" fill="none"/>'
                   f'<rect width="{w}" height="14" rx="2" fill="{p["chip"]}" stroke="{col}" stroke-width="1.5"/></g>')
    for i, op in enumerate(ops):
        a, bq = (i + 0.5) / n, (i + 1) / n
        art.append(f'<text x="{(ax + bx + 100) / 2:.0f}" y="{y0 + 5 * row + 22}" class="mono" font-size="14" fill="{p["fg"]}" text-anchor="middle" opacity="0">{op}'
                   f'<animate attributeName="opacity" calcMode="discrete" values="0;1;0" keyTimes="0;{a:.3f};{bq:.3f}" dur="7.2s" repeatCount="indefinite"/></text>')
    body = frame(p, W, H) + head(p, "PUSH_SWAP", "Sort a stack with two stacks and eleven moves.", "C  ·  linked lists  ·  chunk sort") + "".join(art)
    return svg(W + 11, H + 11, "push_swap: sort a stack with two stacks and eleven moves.", p, body)


def maze(p):
    W, H = 838, 196
    cols, rows, cs, ox, oy = 16, 7, 19, 500, 30
    rnd = random.Random(11)
    walls_h = [[True] * cols for _ in range(rows + 1)]
    walls_v = [[True] * (cols + 1) for _ in range(rows)]
    seen = [[False] * cols for _ in range(rows)]
    parent = {}
    stack = [(0, 0)]
    seen[0][0] = True
    while stack:
        x, y = stack[-1]
        nb = [(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
              if 0 <= x + dx < cols and 0 <= y + dy < rows and not seen[y + dy][x + dx]]
        if not nb:
            stack.pop()
            continue
        nx, ny = rnd.choice(nb)
        if nx != x:
            walls_v[y][max(x, nx)] = False
        else:
            walls_h[max(y, ny)][x] = False
        seen[ny][nx] = True
        parent[(nx, ny)] = (x, y)
        stack.append((nx, ny))
    walls_v[0][0] = False
    walls_v[rows - 1][cols] = False
    d = []
    for yy in range(rows + 1):
        for xx in range(cols):
            if walls_h[yy][xx]:
                d.append(f"M{ox + xx * cs} {oy + yy * cs}h{cs}")
    for yy in range(rows):
        for xx in range(cols + 1):
            if walls_v[yy][xx]:
                d.append(f"M{ox + xx * cs} {oy + yy * cs}v{cs}")
    wd = "".join(d)
    path, c = [], (cols - 1, rows - 1)
    while c != (0, 0):
        path.append(c)
        c = parent[c]
    path.append((0, 0))
    path.reverse()
    pts = [(ox - 8, oy + cs / 2)] + [(ox + x * cs + cs / 2, oy + y * cs + cs / 2) for x, y in path] + [(ox + cols * cs + 8, oy + (rows - 1) * cs + cs / 2)]
    pd = "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    L = sum(abs(pts[i + 1][0] - pts[i][0]) + abs(pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1))
    corners = "".join(f"M{x} {y}l5 5" for x, y in ((ox + cols * cs, oy), (ox + cols * cs, oy + rows * cs), (ox, oy + rows * cs)))
    art = (f'<path d="{wd}" transform="translate(5 5)" fill="none" stroke="{p["nm"]}" stroke-opacity="0.3" stroke-width="1"/>'
           f'<path d="{corners}" stroke="{p["nm"]}" stroke-opacity="0.5" fill="none"/>'
           f'<path d="{wd}" fill="none" stroke="{p["nm"]}" stroke-width="1.6" stroke-linecap="round"/>'
           f'<path d="{pd}" fill="none" stroke="{p["green"]}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="{L:.0f}" stroke-dashoffset="{L:.0f}">'
           f'<animate attributeName="stroke-dashoffset" values="{L:.0f};0;0" keyTimes="0;0.8;1" dur="5.5s" repeatCount="indefinite"/></path>'
           f'<circle r="4" fill="{p["green"]}"><animateMotion path="{pd}" keyPoints="0;1;1" keyTimes="0;0.8;1" calcMode="linear" dur="5.5s" repeatCount="indefinite"/></circle>')
    body = frame(p, W, H) + head(p, "A-MAZE-ING", "Generates a maze, then finds the shortest way out.", "Python  ·  DFS generation  ·  IDDFS solver") + art
    return svg(W + 11, H + 11, "a-maze-ing: generates a maze, then finds the shortest way out.", p, body)


for mode, p in PAL.items():
    open(f"{OUT}/push_swap-{mode}.svg", "w").write(push_swap(p))
    open(f"{OUT}/maze-{mode}.svg", "w").write(maze(p))
print("ok")
