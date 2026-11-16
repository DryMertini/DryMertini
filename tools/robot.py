"""A tired patchwork robot that sits on the cable hub and charges off incoming pulses."""
import random

T = 18.0  # master cycle in seconds: charge up, cheer up, reset


def cables(p, hx, hy, yb, w=850, step=95):
    """Cables fanning out below the hub, each with a pulse running in at its own rhythm."""
    rnd = random.Random(7)
    lines, pulses = [], []
    tx = -330
    while tx <= w + 700:
        ex, ey = tx, yb
        if tx < 0:
            ex, ey = 0, hy + (yb - hy) * (0 - hx) / (tx - hx)
        elif tx > w:
            ex, ey = w, hy + (yb - hy) * (w - hx) / (tx - hx)
        tx += step
        if ey < hy + 14:
            continue
        length = ((ex - hx) ** 2 + (ey - hy) ** 2) ** 0.5
        d = f"M{ex:.1f} {ey:.1f}L{hx} {hy}"
        lines.append(d)
        dur = round(rnd.uniform(2.8, 7.6), 2)
        beg = round(rnd.uniform(0, dur), 2)
        f = min(0.9, (0.45 + length / 520) / dur)
        mo = (f'<animateMotion path="{d}" keyPoints="0;1;1" keyTimes="0;{f:.3f};1" calcMode="linear" dur="{dur}s" begin="-{beg}s" repeatCount="indefinite"/>'
              f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;{f:.3f};{f:.3f};1" dur="{dur}s" begin="-{beg}s" repeatCount="indefinite"/>')
        pulses.append(f'<circle r="5.5" fill="{p["gold"]}" opacity="0" filter="url(#soft)">{mo}</circle><circle r="2.4" fill="{p["spark"]}" opacity="0">{mo}</circle>')
    return (f'<path d="{"".join(lines)}" fill="none" stroke="url(#go)" stroke-opacity="0.55" stroke-width="1.2"/>' + "".join(pulses))


def _anim(attr, values, times, extra=""):
    values, times = list(values), list(times)
    if times[-1] < T:  # keyTimes must run to the end of the cycle or browsers drop the animation
        times.append(T)
        values.append(values[-1])
    kt = ";".join(f"{t / T:.4f}" for t in times)
    return f'<animate attributeName="{attr}" values="{";".join(values)}" keyTimes="{kt}" dur="{T}s" repeatCount="indefinite" {extra}/>'


def _gear(p, r=4.2):
    return (f'<circle r="{r}" fill="none" stroke="{p["nm"]}" stroke-width="2.6" stroke-dasharray="2.2 2.2"/>'
            f'<circle r="{r - 1.2}" fill="{p["chip2"]}" stroke="{p["nm"]}" stroke-width="1.2"/><circle r="1" fill="{p["nm"]}"/>')


def robot(p, hx, hy, scale=1.0):
    ink, gold, green, body, dim = p["ink"], p["nm"], p["green"], p["chip2"], p["dim"]
    dx, dy = 6, -5  # wireframe depth offset
    FULL, RESET = 12.6, 17.0  # battery full -> robot dance until reset
    DANCE_STEP = 0.45
    DANCE_N = int((RESET - FULL - 0.3) / DANCE_STEP)

    def box(pts):
        d = "M" + "L".join(f"{x} {y}" for x, y in pts) + "Z"
        back = "M" + "L".join(f"{x + dx} {y + dy}" for x, y in pts) + "Z"
        links = "".join(f"M{x} {y}l{dx} {dy}" for x, y in pts)
        return (f'<path d="{back}" fill="none" stroke="{ink}" stroke-opacity="0.4" stroke-width="1"/>'
                f'<path d="{links}" fill="none" stroke="{ink}" stroke-opacity="0.5" stroke-width="1"/>'
                f'<path d="{d}" fill="{body}" stroke="{ink}" stroke-width="1.6" stroke-linejoin="round"/>')

    # each arm: (shoulder, rest elbow/hand, floor elbow/hand, head elbow/hand, floor scrap, spot on head, start time)
    arms = [
        dict(sh=(-30, -47), rest=((-41, -24), (-39, -8)), floor=((-46, -22), (-52, -1)), head=((-49, -62), (-33, -97)),
             scrap=(-54, 3), spot=(-20, -105), t0=3.0,
             da=((-50, -47), (-50, -70)), db=((-50, -47), (-50, -24))),
        dict(sh=(30, -47), rest=((43, -26), (42, -1)), floor=((47, -22), (57, 0)), head=((51, -60), (35, -95)),
             scrap=(60, 4), spot=(27, -102), t0=8.0,
             da=((50, -47), (50, -24)), db=((50, -47), (50, -70))),
    ]

    o = [f'<g transform="translate({hx} {hy}) scale({scale})" stroke-linecap="round" stroke-linejoin="round">']
    # hub plate
    o.append(f'<ellipse cx="0" cy="0" rx="34" ry="8" fill="{gold}" opacity="0.5" filter="url(#soft)"><animate attributeName="opacity" values="0.2;0.6;0.25;0.5;0.2" dur="3.1s" repeatCount="indefinite"/></ellipse>'
             f'<ellipse cx="0" cy="4" rx="27" ry="6.5" fill="{body}" stroke="{gold}" stroke-opacity="0.5" stroke-width="1.2"/>'
             f'<ellipse cx="0" cy="0" rx="27" ry="6.5" fill="{body}" stroke="{gold}" stroke-width="1.6"/>')
    # scraps lying on the floor, waiting to be picked up
    for a in arms:
        g = a["t0"] + 1.0
        o.append(f'<g transform="translate({a["scrap"][0]} {a["scrap"][1]})" opacity="1">{_gear(p)}'
                 + _anim("opacity", ["1", "1", "0", "0", "1"], [0, g, g + 0.01, T - 0.9, T]) + '</g>')
    # breathing body
    o.append('<g><animateTransform attributeName="transform" type="translate" values="0 0;0 1.6;0 0" dur="4.4s" repeatCount="indefinite"/>')
    o.append(f'<rect x="-13" y="-11" width="26" height="11" fill="{body}" stroke="{ink}" stroke-width="1.6"/>')
    # torso
    o.append(box([(-30, -52), (30, -52), (24, -11), (-24, -11)]))
    o.append(f'<path d="M-7 -52L3 -11" stroke="{gold}" stroke-width="1.2" fill="none"/>'
             f'<path d="M-9 -45h7M-7.5 -37h7M-5.5 -29h7M-3.5 -21h7" stroke="{gold}" stroke-width="1.2" fill="none"/>'
             f'<g fill="{dim}"><circle cx="-24" cy="-46" r="1.5"/><circle cx="-20" cy="-17" r="1.5"/></g>')
    for i in range(4):  # battery: one cell every few seconds, full at FULL, drained at the end
        y = -22 - i * 8
        on = 2.0 + i * 3.5
        o.append(f'<rect x="9" y="{y}" width="13" height="5.5" rx="1" fill="{green}" opacity="0.15" stroke="{green}" stroke-opacity="0.6" stroke-width="0.8">'
                 + _anim("opacity", ["0.15", "0.15", "1", "1", "0.15"], [0, on, on + 0.4, RESET + 0.4, T]) + '</rect>')
    o.append(f'<rect x="-5" y="-58" width="10" height="7" fill="{body}" stroke="{ink}" stroke-width="1.4"/>')
    # head: slow tilt, jerk on each snort
    o.append('<g><animateTransform attributeName="transform" type="rotate" values="-2 0 -58;3.5 0 -58;-2 0 -58" dur="9s" repeatCount="indefinite"/>')
    o.append('<g><animateTransform attributeName="transform" type="translate" values="0 0;0 0;0 -2.5;0 1;0 0" keyTimes="0;0.84;0.88;0.93;1" dur="6.8s" repeatCount="indefinite"/>')
    lt, lv = [0.0, FULL + 0.2], ["0 0 -58", "0 0 -58"]
    for k in range(DANCE_N):
        t = FULL + 0.3 + k * DANCE_STEP
        ang = "-8 0 -58" if k % 2 == 0 else "8 0 -58"
        lt += [t, t + DANCE_STEP - 0.1]
        lv += [ang, ang]
    lt += [RESET + 0.3, T]
    lv += ["0 0 -58", "0 0 -58"]
    o.append(f'<g><animateTransform attributeName="transform" type="rotate" values="{";".join(lv)}" keyTimes="{";".join(f"{x / T:.4f}" for x in lt)}" dur="{T}s" repeatCount="indefinite"/>')
    o.append(f'<path d="M15 -98l-3 -3l6 -3l-6 -3l6 -3l-2 -3" fill="none" stroke="{ink}" stroke-width="1.4"/>'
             f'<circle cx="16" cy="-116" r="6" fill="{green}" filter="url(#soft)"><animate attributeName="opacity" values="0.1;0.9;0.2;0.1;0.7;0.1" keyTimes="0;0.08;0.2;0.55;0.62;1" dur="4.3s" repeatCount="indefinite"/></circle>'
             f'<circle cx="16" cy="-116" r="2.6" fill="{green}"/>'
             f'<path d="M7 -121l-4 -3M16 -125v-5M25 -121l4 -3" stroke="{green}" stroke-width="1.4" fill="none" opacity="0">'
             + _anim("opacity", ["0", "0", "1", "1", "0"], [0, FULL, FULL + 0.3, RESET, RESET + 0.3]) + '</path>')
    o.append(box([(-4, -98), (30, -98), (30, -58), (-4, -58)]))
    o.append(box([(-30, -101), (-4, -101), (-4, -61), (-30, -61)]))
    o.append(f'<path d="M-8 -93h8M-8 -85h8M-8 -69h8" stroke="{gold}" stroke-width="1.2" fill="none"/>'
             f'<g fill="{dim}"><circle cx="-26" cy="-97" r="1.3"/><circle cx="26" cy="-94" r="1.3"/><circle cx="26" cy="-62" r="1.3"/></g>')
    # eyes
    glow = _anim("opacity", ["0.55", "0.55", "1", "1", "0.55"], [0, FULL, FULL + 0.3, RESET, RESET + 0.3])
    o.append(f'<circle cx="-17" cy="-84" r="7" fill="{body}" stroke="{gold}" stroke-width="1.5"/><circle cx="-17" cy="-82.5" r="2.4" fill="{gold}">{glow}</circle>'
             f'<rect x="6" y="-90" width="15" height="12" rx="2" fill="{body}" stroke="{gold}" stroke-width="1.5"/><rect x="11.5" y="-85" width="4.4" height="4.4" fill="{gold}">{glow}</rect>')
    # eyelids: droopy by default, wide open while the battery is full; blink on top of that
    kt = ";".join(f"{t / T:.4f}" for t in (0, FULL, FULL + 0.4, RESET, RESET + 0.5, T))
    o.append(f'<g><animateTransform attributeName="transform" type="translate" values="0 0;0 0;0 0;0 0;0 0;0 0" keyTimes="{kt}" dur="{T}s" repeatCount="indefinite"/>'
             '<g><animateTransform attributeName="transform" type="translate" values="0 0;0 0;0 5.5;0 5.5;0 0;0 0" keyTimes="0;0.5;0.54;0.62;0.68;1" dur="7.3s" repeatCount="indefinite"/>'
             f'<rect x="-25" y="-97" width="16" height="13.5" fill="{body}"/><path d="M-24.6 -83.5H-9.4" stroke="{ink}" stroke-width="1.6"/>'
             f'<rect x="5" y="-96" width="17" height="11" fill="{body}"/><path d="M5.4 -85H21.6" stroke="{ink}" stroke-width="1.6"/></g></g>')
    o.append(f'<path d="M-30 -101H-4M-4 -98H30" stroke="{ink}" stroke-width="1.6" fill="none"/>')
    # eye bags fade when it cheers up; mouth goes from frown to grin
    tired = _anim("opacity", ["1", "1", "0", "0", "1"], [0, FULL, FULL + 0.4, RESET, RESET + 0.5])
    happy = _anim("opacity", ["0", "0", "1", "1", "0"], [0, FULL, FULL + 0.4, RESET, RESET + 0.5])
    o.append(f'<path d="M-23 -74.5q6 3 12 0M7 -75.5q6.5 3 13 0" fill="none" stroke="{dim}" stroke-width="1.2"/>'
             f'<rect x="-9" y="-78" width="10" height="6" rx="2" fill="{body}" stroke="{ink}" stroke-width="1.2"/><g fill="{ink}"><circle cx="-6" cy="-75" r="0.9"/><circle cx="-2" cy="-75" r="0.9"/></g>'
             f'<path d="M-15 -65.5Q0 -68.5 15 -64.5M-8 -67.5v3M0 -68v3M8 -67v3" fill="none" stroke="{ink}" stroke-width="1.3"/>')
    # snort puffs
    for sx, ex in ((-6, -15), (-2, 6)):
        o.append(f'<circle cx="{sx}" cy="-73" r="1.5" fill="none" stroke="{ink}" stroke-width="1" opacity="0">'
                 f'<animate attributeName="opacity" values="0;0;0.9;0" keyTimes="0;0.85;0.88;1" dur="6.8s" repeatCount="indefinite"/>'
                 f'<animate attributeName="cx" values="{sx};{sx};{ex}" keyTimes="0;0.85;1" dur="6.8s" repeatCount="indefinite"/>'
                 f'<animate attributeName="cy" values="-73;-73;-63" keyTimes="0;0.85;1" dur="6.8s" repeatCount="indefinite"/>'
                 f'<animate attributeName="r" values="1.5;1.5;5" keyTimes="0;0.85;1" dur="6.8s" repeatCount="indefinite"/></circle>')
    # scraps already bolted onto the head (stay until the cycle resets)
    for a in arms:
        at = a["t0"] + 2.6
        o.append(f'<g transform="translate({a["spot"][0]} {a["spot"][1]})" opacity="0">{_gear(p)}'
                 + _anim("opacity", ["0", "0", "1", "1", "0"], [0, at, at + 0.01, T - 0.9, T - 0.5]) + '</g>')
    o.append("</g></g></g>")  # end head
    # arms: reach down, grab a scrap, lift it to the head, drop back
    for a in arms:
        t0 = a["t0"]
        times = [0, t0, t0 + 1.0, t0 + 1.4, t0 + 2.6, t0 + 3.2, t0 + 4.0, FULL + 0.2]
        seq = ["rest", "rest", "floor", "floor", "head", "head", "rest", "rest"]
        for k in range(DANCE_N):  # the robot: stiff right angles, snapping between two poses
            t = FULL + 0.3 + k * DANCE_STEP
            times += [t, t + DANCE_STEP - 0.1]
            seq += ["da" if k % 2 == 0 else "db"] * 2
        times += [RESET + 0.3, T]
        seq += ["rest", "rest"]
        sx, sy = a["sh"]
        dvals = [f"M{sx} {sy}L{a[k][0][0]} {a[k][0][1]}L{a[k][1][0]} {a[k][1][1]}" for k in seq]
        ex = [str(a[k][0][0]) for k in seq]
        ey = [str(a[k][0][1]) for k in seq]
        hxv = [str(a[k][1][0]) for k in seq]
        hyv = [str(a[k][1][1] + 4) for k in seq]
        r = a["rest"]
        o.append(f'<path d="{dvals[0]}" fill="none" stroke="{ink}" stroke-width="1.8">{_anim("d", dvals, times)}</path>'
                 f'<circle cx="{r[0][0]}" cy="{r[0][1]}" r="2.3" fill="{gold}">{_anim("cx", ex, times)}{_anim("cy", ey, times)}</circle>'
                 f'<circle cx="{r[1][0]}" cy="{r[1][1] + 4}" r="4" fill="none" stroke="{ink}" stroke-width="1.5" stroke-dasharray="19 6.2">{_anim("cx", hxv, times)}{_anim("cy", hyv, times)}</circle>')
        # the scrap riding in the hand
        g0, g1 = t0 + 1.0, t0 + 2.6
        pos = [f"{a['scrap'][0]} {a['scrap'][1]}", f"{a['scrap'][0]} {a['scrap'][1]}", f"{a['scrap'][0]} {a['scrap'][1]}", f"{a['spot'][0]} {a['spot'][1]}", f"{a['spot'][0]} {a['spot'][1]}"]
        kt2 = ";".join(f"{t / T:.4f}" for t in (0, g0, g0 + 0.4, g1, T))
        o.append(f'<g opacity="0"><animateTransform attributeName="transform" type="translate" values="{";".join(pos)}" keyTimes="{kt2}" dur="{T}s" repeatCount="indefinite"/>'
                 + _anim("opacity", ["0", "0", "1", "1", "0", "0"], [0, g0, g0 + 0.01, g1, g1 + 0.01, T]) + _gear(p) + '</g>')
    o.append("</g></g>")
    return "".join(o)
