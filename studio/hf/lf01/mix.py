"""LF01 global mix: voice + continuous synth music bed (ducked, -24 dB) + SFX (Ep 12 ElevenLabs whoosh/pop/hit/chime, reused, 0 credits)
at the beat times every chapter build logged (sfx_chK.json). Output: /home/claude/lf01/mix.wav (48k, loudnorm -14 LUFS)."""
import json, subprocess, sys, numpy as np
sys.path.insert(0, "/home/claude/cyto2"); sys.path.insert(0, "/home/claude/hf/lf01")
from engine import tone, noise, hp, lp, add, load_mono, SR
import lf
V = "/home/claude/lf01"; T = lf.B[-1]
def load_sfx(name, max_len):
    x = load_mono(f"/home/claude/ep13/sfx/{name}.wav", SR); env = np.abs(x); nz = np.where(env > env.max() * 0.004)[0]
    x = x[nz[0]: min(len(x), nz[0] + int(max_len * SR))] if len(nz) else x[: int(max_len * SR)]
    f = min(len(x), int(0.08 * SR)); x[-f:] *= np.linspace(1, 0, f); return x / (np.sqrt(np.mean(x ** 2)) + 1e-9)
def pad(m, dur, g=0.035):
    f = 440 * 2 ** ((m - 69) / 12); t = np.arange(int(dur * SR)) / SR
    env = np.minimum(1, t / 0.5) * np.minimum(1, (dur - t) / 0.7).clip(0, 1)
    return (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t) + 0.15 * np.sin(2 * np.pi * 3.01 * f * t)) * env * g
n = int((T + 0.5) * SR); music = np.zeros(n, np.float32)
BPM = 90; BAR = 60 / BPM * 4
chords = [[48, 55, 60, 64], [45, 52, 57, 60], [41, 48, 53, 57], [43, 50, 55, 59]]   # C  Am  F  G: hopeful, warm
t = 0.0; i = 0
while t < T + 0.5:
    for m in chords[i % 4]: add(music, pad(m + 12, BAR + 0.8), t)
    add(music, pad(chords[i % 4][0], BAR + 0.4, 0.05), t); t += BAR; i += 1
kick = tone(100, 42, 0.3, 0.1) * 0.5; snare = hp(noise(0.12, 5), 0.25) * np.exp(-np.arange(int(0.12 * SR)) / SR / 0.04) * 0.1
hat = hp(noise(0.03, 2), 0.6) * np.exp(-np.arange(int(0.03 * SR)) / SR / 0.008) * 0.06
BEAT = 60 / BPM; t = 14.3; s = 0          # drums enter on the catchphrase
quiet = [(lf.B[3], lf.B[4])]               # first-week chapter: drums out (calmer)
while t < T + 0.5:
    if not any(a <= t < b for a, b in quiet):
        if s % 4 in (0, 2): add(music, kick, t)
        if s % 4 in (1, 3): add(music, snare, t)
        add(music, hat, t + BEAT / 2)
    t += BEAT; s += 1
music = lp(music, 0.3)
v = load_mono(f"{V}/voice.wav", SR); vv = np.zeros(n, np.float32); m = min(n, len(v)); vv[:m] = v[:m]
vrms = np.sqrt(np.mean(vv[np.abs(vv) > 0.02] ** 2))
env = np.convolve(np.abs(vv), np.ones(2205) / 2205, mode="same"); env /= env.max() + 1e-9
music *= (1 - 0.6 * np.clip(env * 3, 0, 1))
music *= vrms * 10 ** (-24 / 20) / (np.sqrt(np.mean(music ** 2)) + 1e-9)
fo = int(2.0 * SR); music[-fo:] *= np.linspace(1, 0.3, fo)
S = {"whoosh": load_sfx("whoosh", 0.9), "pop": load_sfx("pop", 0.35), "hit": load_sfx("hit", 1.4), "chime": load_sfx("chime", 1.5)}
GAIN = {"whoosh": -19, "pop": -20, "hit": -16, "chime": -18}
sfx = np.zeros(n, np.float32); ev = []
for k in range(8): ev += json.load(open(f"{V}/sfx_ch{k}.json"))
ev.sort(key=lambda e: e[1]); last = {}; used = 0
for kind, tt in ev:          # de-dupe: same kind within 0.25 s
    if tt - last.get(kind, -9) < 0.25: continue
    last[kind] = tt; add(sfx, S[kind] * vrms * 10 ** (GAIN[kind] / 20), max(0, tt)); used += 1
mix = music + sfx; mix[:m] += v[:m]
mix = np.tanh(mix / max(1.0, np.max(np.abs(mix)) * 0.9)) * 0.95; mix = mix[: int(T * SR)]
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-", f"{V}/raw_mix.wav"], input=(mix * 32767).astype(np.int16).tobytes(), check=True)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f"{V}/raw_mix.wav", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-ac", "2", f"{V}/mix.wav"], check=True)
print("mix", round(T, 3), "s; sfx events", used, "of", len(ev))
