"""LF02 v3 procedural motion layer (per-frame, 30 fps), driven from Python and applied by ONE GSAP proxy tween per scene.

Why: v2 arms were single tubes that snapped between opacity-toggled poses ("bad hand/arm animation"), pupils were tweened
by several systems at once (eyes drifting out of the eye), blinks were 1-frame swaps. Here every limb is a 2-segment
rig solved with 2-bone IK every frame:
  * hand targets travel on ARCS (polar interpolation around the shoulder), slow-in/slow-out + small overshoot
  * shoulders lead: the elbow angle lags the shoulder by 1 frame; the hand/prop lags the forearm by 2-3 frames with
    a velocity overshoot (follow-through), so a gesture snaps, overshoots, settles
  * eyes: pupils are clamped to <= 25 % of the eye width, move as 3-frame saccades, the head (face features) follows
    ~0.1 s later; listeners look at the speaker and HOLD; 3-frame blinks every 2-4 s
Channels (element id -> per-frame values) are emitted as JSON + a tiny applier (setAttribute / style.transform)."""
import math, json, random

FPS = 30


def dvec(th):
    r = math.radians(th); return (-math.sin(r), math.cos(r))          # segment drawn pointing DOWN, rotated clockwise by th


def ang_of(vx, vy): return math.degrees(math.atan2(-vx, vy))


def ik(S, P, L1, L2, bend):
    vx, vy = P[0] - S[0], P[1] - S[1]; D = math.hypot(vx, vy)
    D = max(abs(L1 - L2) + 1e-3, min(L1 + L2 - 1e-3, D))
    phi = ang_of(vx, vy)
    a = math.degrees(math.acos(max(-1, min(1, (L1 * L1 + D * D - L2 * L2) / (2 * L1 * D)))))
    g = math.degrees(math.acos(max(-1, min(1, (L1 * L1 + L2 * L2 - D * D) / (2 * L1 * L2)))))
    return phi + bend * a, -bend * (180 - g)


def fk(S, A, B, L1, L2):
    d1 = dvec(A); d2 = dvec(A + B)
    E = (S[0] + L1 * d1[0], S[1] + L1 * d1[1])
    return E, (E[0] + L2 * d2[0], E[1] + L2 * d2[1])


def ease(k, kind="io"):
    k = max(0.0, min(1.0, k))
    if kind == "lin": return k
    if kind == "out": return 1 - (1 - k) ** 3
    if kind == "in": return k ** 2
    if kind == "back":                                   # back.out(1.4): snap + overshoot + settle
        c = 1.4; return 1 + (c + 1) * (k - 1) ** 3 + c * (k - 1) ** 2
    return 0.5 - 0.5 * math.cos(math.pi * k)             # sine in-out (slow in / slow out)


def lag(xs, n): return [xs[max(0, i - n)] for i in range(len(xs))]


class Arm:
    """2-segment arm. S shoulder, L1/L2 segment lengths (char-canvas units). bend: +1/-1 picked so the elbow points
    outward (away from body centre bx)."""
    def __init__(self, pid, S, L1, L2, rest, bx, hand_rest_abs=0.0):
        self.pid, self.S, self.L1, self.L2, self.rest = pid, S, L1, L2, rest
        self.bend = max((1, -1), key=lambda b: abs(fk(S, *ik(S, rest, L1, L2, b), L1, L2)[0][0] - bx))
        self.keys = []            # (t, target(x,y), dur, ease, hand_abs or None, shape)
        self.hand_rest_abs = hand_rest_abs
        self.wig = []             # (t0, t1, amp_px, period) small hand wiggles (writing, waving)

    def to(self, t, P, dur=.22, kind="back", hand=None, shape=None):
        self.keys.append((t, P, dur, kind, hand, shape)); return self

    def frames(self, n, override=None):
        """-> per-frame (A, B_lagged, H_rel, shape, hand_xy). override: optional per-frame list of (P, hand_abs|None, shape) or None."""
        S, L1, L2, bend = self.S, self.L1, self.L2, self.bend
        keys = sorted(self.keys, key=lambda k: k[0])
        aligned = (lambda P: sum(ik(S, P, L1, L2, bend)) + self.hand_rest_abs) if self.hand_rest_abs is not None else (lambda P: 0.0)
        cur = self.rest; habs = aligned(cur); hmode = None; shape = "relaxed"
        seg = None; ki = 0; Ps, Hs, shapes = [], [], []
        for f in range(n):
            t = f / FPS
            while ki < len(keys) and keys[ki][0] <= t + 1e-6:
                t0, P, dur, kind, hand, shp = keys[ki]
                seg = (t0, cur, P, max(dur, 1 / FPS), kind, habs, hand)
                if shp: shape = shp
                ki += 1
            if seg:
                t0, P0, P1, dur, kind, h0, h1 = seg
                k = ease((t - t0) / dur, kind)
                r0, a0 = math.hypot(P0[0] - S[0], P0[1] - S[1]), ang_of(P0[0] - S[0], P0[1] - S[1])
                r1, a1 = math.hypot(P1[0] - S[0], P1[1] - S[1]), ang_of(P1[0] - S[0], P1[1] - S[1])
                da = (a1 - a0 + 180) % 360 - 180
                r = r0 + (r1 - r0) * k; a = a0 + da * k                    # ARC around the shoulder
                d = dvec(a); cur = (S[0] + r * d[0], S[1] + r * d[1])
                he = h1 if h1 is not None else aligned(cur)
                habs = h0 + (he - h0) * min(1.0, max(0.0, k)); hmode = h1
                if (t - t0) >= dur: seg = None
            elif hmode is None:
                habs = aligned(cur)
            P = cur
            for t0, t1, amp, per in self.wig:
                if t0 <= t <= t1:
                    e = min(1, (t - t0) / .15, (t1 - t) / .15)
                    P = (P[0] + e * amp * math.sin(2 * math.pi * (t - t0) / per), P[1] + e * amp * .35 * math.sin(4 * math.pi * (t - t0) / per))
            h_out = habs
            if override and override[f] is not None:
                P, ho, so = override[f]
                h_out = ho if ho is not None else aligned(P); shape = so or shape
            Ps.append(P); Hs.append(h_out); shapes.append(shape)
        AB = [ik(S, P, L1, L2, bend) for P in Ps]
        A = [a for a, _ in AB]; B = lag([b for _, b in AB], 1)                 # shoulder leads the elbow by a frame
        F = [a + b for a, b in zip(A, B)]
        Hl = []
        for i in range(n):                                                  # hand lags 2 frames + velocity overshoot
            a2 = Hs[max(0, i - 2)]; a4 = Hs[max(0, i - 4)]
            Hl.append(a2 + .3 * max(-25, min(25, a2 - a4)))
        H = [hl - fi for hl, fi in zip(Hl, F)]
        hw = [fk(S, a, b, L1, L2)[1] for a, b in zip(A, B)]
        return A, B, H, shapes, hw


SHAPES = ("relaxed", "grip", "fist", "point")


class Motion:
    """Collects channels for one scene. chan(id, kind, ...) kinds:
       r (rotate about px,py) | t (translate x,y) | o (opacity) | c (CSS translate/rotate/scale on an HTML div)"""
    def __init__(self, T):
        self.n = int(round(T * FPS)) + 2
        self.ch = {}

    @staticmethod
    def _c(xs, nd=1):
        if isinstance(xs, (int, float)): return round(xs, nd)
        xs = [round(x, nd) for x in xs]
        return xs[0] if all(x == xs[0] for x in xs) else xs

    def rot(self, id_, px, py, xs): self.ch[id_] = ["r", round(px, 1), round(py, 1), self._c(xs)]
    def tr(self, id_, xs, ys): self.ch[id_] = ["t", self._c(xs), self._c(ys)]
    def op(self, id_, xs): self.ch[id_] = ["o", self._c(xs, 2)]
    def css(self, id_, xs, ys, rs=0, sx=1, sy=1): self.ch[id_] = ["c", self._c(xs), self._c(ys), self._c(rs), self._c(sx, 3), self._c(sy, 3)]
    def svgm(self, id_, px, py, xs, ys, rs=0, sx=1, sy=1):
        self.ch[id_] = ["m", round(px, 1), round(py, 1), self._c(xs), self._c(ys), self._c(rs), self._c(sx, 3), self._c(sy, 3)]

    def arm(self, arm, override=None):
        A, B, H, shapes, hw = arm.frames(self.n, override)
        S = arm.S; p = arm.pid
        self.rot(p + "UA", S[0], S[1], A)
        self.rot(p + "FA", S[0], S[1] + arm.L1, B)
        self.rot(p + "HD", S[0], S[1] + arm.L1 + arm.L2, H)
        for s in SHAPES:
            self.op(f"{p}h_{s}", [1 if x == s else 0 for x in shapes])
        return dict(A=A, B=B, H=H, shapes=shapes, hand=hw)

    def js(self):
        if not self.ch: return ""
        D = json.dumps({"n": self.n, "c": self.ch}, separators=(",", ":"))
        return ("(function(){const D=" + D + ";const E={};for(const k in D.c){E[k]=document.getElementById(k);}"
                "const v=(a,f)=>typeof a==='number'?a:a[Math.min(f,a.length-1)];"
                "const ap=function(f){for(const k in D.c){const c=D.c[k],e=E[k];if(!e)continue;const t=c[0];"
                "if(t==='r')e.setAttribute('transform','rotate('+v(c[3],f)+' '+c[1]+' '+c[2]+')');"
                "else if(t==='t')e.setAttribute('transform','translate('+v(c[1],f)+' '+v(c[2],f)+')');"
                "else if(t==='o')e.setAttribute('opacity',v(c[1],f));"
                "else if(t==='m'){const px=c[1],py=c[2];e.setAttribute('transform','translate('+v(c[3],f)+' '+v(c[4],f)+') rotate('+v(c[5],f)+' '+px+' '+py+') translate('+px+' '+py+') scale('+v(c[6],f)+' '+v(c[7],f)+') translate('+(-px)+' '+(-py)+')');}"
                "else if(t==='c')e.style.transform='translate('+v(c[1],f)+'px,'+v(c[2],f)+'px) rotate('+v(c[3],f)+'deg) scale('+v(c[4],f)+','+v(c[5],f)+')';}};"
                "window.__mvD=D;window.__mv=ap;ap(0);const P={f:0};"
                "tl.fromTo(P,{f:0},{f:D.n-1,duration:(D.n-1)/30,ease:'none',immediateRender:false,onUpdate:()=>ap(Math.round(P.f))},0);})();")


# ------------------------------------------------------------------ eyes
def eye_track(n, rx, targets, blinks, lid_open, lid_half, lid_shut, clamp=.45, inner_max=0.0, seed=1):
    """targets: per-frame (dx, dy) in [-1,1] (look direction). Returns per-frame pupil (x,y) px, face offset (x,y) px,
    blink-lid y. Saccade: 3-frame ease-out move; face follows the pupils 3 frames later (eyes LEAD the head)."""
    cl = clamp * rx - inner_max            # 25 % of the eye width = 0.5 rx; keep margin for the expression's own offset
    px, py, cur, start, tgt, k0 = [], [], (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), -99
    for f in range(n):
        tx, ty = targets[f]
        tt = (max(-1, min(1, tx)) * cl, max(-1, min(1, ty)) * cl * .6)
        if abs(tt[0] - tgt[0]) > .5 or abs(tt[1] - tgt[1]) > .5:
            start, tgt, k0 = cur, tt, f
        k = ease((f - k0 + 1) / 3, "out") if f - k0 < 3 else 1
        cur = (start[0] + (tgt[0] - start[0]) * k, start[1] + (tgt[1] - start[1]) * k)
        px.append(cur[0]); py.append(cur[1])
    # face (head turn) follows the eyes ~0.1 s later, smoothed
    fx, fy, sx, sy = [], [], 0.0, 0.0
    for f in range(n):
        g = max(0, f - 3)
        sx += (px[g] * .55 - sx) * .25; sy += (py[g] * .4 - sy) * .25
        fx.append(sx); fy.append(sy)
    lid = [lid_open] * n
    for b in blinks:
        f = int(round(b * FPS))
        for i, v in enumerate((lid_half, lid_shut, lid_half)):
            if 0 <= f + i < n: lid[f + i] = v
    return px, py, fx, fy, lid


def auto_blinks(T, seed, avoid=()):
    rnd = random.Random(seed); t = rnd.uniform(.5, 1.6); out = []
    while t < T - .2:
        if not any(a - .1 <= t <= b for a, b in avoid): out.append(round(t, 3))
        t += rnd.uniform(2.0, 4.0)
    return out
