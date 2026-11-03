"""Concat the 8 chapter renders, cross-check A/V sync per chapter (render's own voice track vs the master voice.wav),
then mux the global mix -> /home/claude/lf01/cyto-lf01-quit-smoking.mp4"""
import subprocess, numpy as np, sys
sys.path.insert(0, "/home/claude/hf/lf01"); import lf
R = "/home/claude/lf01/renders"; OUT = "/home/claude/lf01/cyto-lf01-quit-smoking.mp4"
open(f"{R}/list.txt", "w").write("".join(f"file '{R}/ch{k}.mp4'\n" for k in range(8)))
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", f"{R}/list.txt", "-c", "copy", f"{R}/concat.mp4"], check=True)
def pcm(src, ss=None, t=None, sr=8000):
    a = ["ffmpeg", "-v", "error"] + (["-ss", str(ss)] if ss is not None else []) + ["-i", src] + (["-t", str(t)] if t else []) + ["-ac", "1", "-ar", str(sr), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(a, capture_output=True).stdout, np.float32)
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{R}/concat.mp4"], capture_output=True, text=True).stdout)
print(f"concat duration {dur:.3f}s, expected {lf.B[-1]:.3f}s")
for k in range(8):
    t0 = lf.B[k] + 2.0
    a = pcm(f"{R}/concat.mp4", t0, 6); b = pcm("/home/claude/lf01/voice.wav", t0 - 0.5, 7)
    a = a - a.mean(); c = np.correlate(b, a, "valid"); lag = (np.argmax(c) / 8000) - 0.5
    print(f"ch{k} @ {t0:.1f}s: offset {lag * 1000:+.0f} ms")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f"{R}/concat.mp4", "-i", "/home/claude/lf01/mix.wav", "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                "-shortest", "-movflags", "+faststart", OUT], check=True)
print("wrote", OUT)
