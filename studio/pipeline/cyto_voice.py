"""Turn Utsha's raw recording into Cyto's voice (unrecognizable as him, keeps his Toronto delivery).
python3 cyto_voice.py in.(m4a|mp3|wav) out.wav [preset]
Presets: cyto (default) | cartoon | gruff
How: WORLD vocoder splits the voice into pitch + vocal-tract shape (formants) + breath.
Shifting BOTH pitch and formants changes who it sounds like (pitch alone = chipmunk-you).
Then a character chain: clean-up, presence EQ, compression, light grit, tiny doubler."""
import sys, subprocess, tempfile, os
import numpy as np, pyworld as pw
from pedalboard import (Pedalboard, HighpassFilter, LowShelfFilter, HighShelfFilter, PeakFilter,
                        Compressor, Distortion, Chorus, Gain, Limiter, NoiseGate)
from pedalboard.io import AudioFile

PRESETS = {  # semitones, formant ratio (>1 = smaller head), grit dB, doubler mix
    "cyto":    dict(st=3.5, fr=1.17, grit=4.0, chorus=0.12),
    "cartoon": dict(st=6.0, fr=1.26, grit=3.0, chorus=0.15),
    "gruff":   dict(st=-2.5, fr=0.88, grit=7.0, chorus=0.08),
}
SR = 48000


def load(path):
    tmp = tempfile.mktemp(suffix=".wav")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", path, "-ac", "1", "-ar", str(SR), tmp], check=True)
    with AudioFile(tmp) as f: x = f.read(f.frames)[0].astype(np.float64)
    os.remove(tmp); return x


def warp(env, ratio):
    """Move formants: new[k] = old[k / ratio] along the frequency axis."""
    n = env.shape[1]; src = np.arange(n) / ratio
    out = np.empty_like(env)
    for i in range(env.shape[0]): out[i] = np.interp(src, np.arange(n), env[i], right=env[i, -1])
    return out


def convert(x, st, fr):
    f0, t = pw.harvest(x, SR, f0_floor=60, f0_ceil=700, frame_period=5.0)
    sp = pw.cheaptrick(x, f0, t, SR); ap = pw.d4c(x, f0, t, SR)
    f0 = f0 * 2 ** (st / 12)
    y = pw.synthesize(f0, warp(sp, fr), warp(ap, fr), SR, frame_period=5.0)
    return y.astype(np.float32)


def character(y, grit, chorus):
    board = Pedalboard([
        HighpassFilter(90), NoiseGate(threshold_db=-45, ratio=4),
        LowShelfFilter(cutoff_frequency_hz=200, gain_db=-2.5),
        PeakFilter(cutoff_frequency_hz=2800, gain_db=4.0, q=0.9),   # presence = reads on phone speakers
        HighShelfFilter(cutoff_frequency_hz=9000, gain_db=2.0),
        Compressor(threshold_db=-20, ratio=4, attack_ms=5, release_ms=80),
        Distortion(drive_db=grit), Gain(-grit * 0.8),
        Chorus(rate_hz=0.6, depth=0.08, centre_delay_ms=9, feedback=0.0, mix=chorus),
        Limiter(threshold_db=-1.5),
    ])
    return board(y, SR)


if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    p = PRESETS[sys.argv[3] if len(sys.argv) > 3 else "cyto"]
    y = character(convert(load(src), p["st"], p["fr"]), p["grit"], p["chorus"])
    with AudioFile(dst, "w", SR, 1) as f: f.write(y[None, :] if y.ndim == 1 else y)
    print(f"{dst}  ({len(y)/SR:.1f}s, preset {sys.argv[3] if len(sys.argv) > 3 else 'cyto'})")
