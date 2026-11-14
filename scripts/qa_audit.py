import os
import sys
import json
import subprocess
import numpy as np
import cv2
from scipy.io import wavfile
from PIL import Image, ImageDraw

# Ensure CUDA DLLs for faster_whisper
site_pkgs = r"C:\Users\NCPC\AppData\Local\Programs\Python\Python312\Lib\site-packages"
nv_root = os.path.join(site_pkgs, "nvidia")
if os.path.isdir(nv_root):
    for sub in os.listdir(nv_root):
        bdir = os.path.join(nv_root, sub, "bin")
        if os.path.isdir(bdir):
            os.add_dll_directory(bdir)
            os.environ["PATH"] = bdir + os.pathsep + os.environ.get("PATH", "")

ENGINE_DIR = os.path.dirname(os.path.abspath(__file__))
if ENGINE_DIR not in sys.path:
    sys.path.insert(0, ENGINE_DIR)
from hung_gfx import FONT_SANS_BOLD, get_font

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--version", default="v8")
ARGS, _ = parser.parse_known_args()
VER = ARGS.version

PROJ_DIR = os.path.dirname(ENGINE_DIR)
OUT_DIR  = os.path.join(PROJ_DIR, "04_OUTPUT", VER)
MP4_PATH = os.path.join(OUT_DIR, f"{VER}.mp4")
META_PATH = os.path.join(OUT_DIR, f"{VER}_timeline_meta.json")
TEMP_DIR = rf"C:\Users\NCPC\AppData\Local\Temp\hung_anti_{VER}"
os.makedirs(TEMP_DIR, exist_ok=True)
TEMP_WAV = os.path.join(TEMP_DIR, f"{VER}_16k_check.wav")


def run_qa():
    print("=== 1. FFPROBE STREAM & DURATION CHECK ===")
    pr = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries",
        "stream=codec_type,codec_name,width,height,r_frame_rate,duration,sample_rate,channels",
        "-of", "json", MP4_PATH
    ]).decode("utf-8")
    probe_data = json.loads(pr)
    for st in probe_data.get("streams", []):
        print(" ", st)

    print("\n=== 2. EBU R128 LOUDNESS & TRUE PEAK CHECK ===")
    ebu = subprocess.run(
        ["ffmpeg", "-nostats", "-i", MP4_PATH, "-filter_complex", "ebur128=peak=true", "-f", "null", "-"],
        capture_output=True, text=True
    )
    tail_lines = [ln for ln in ebu.stderr.splitlines() if any(k in ln for k in ["I:", "LRA:", "Peak:", "Threshold:"])]
    for ln in tail_lines[-8:]:
        print(" ", ln)

    print("\n=== 3. KEYFRAME TYPOGRAPHY & LUMINANCE AUDIT ===")
    meta = json.load(open(META_PATH, encoding="utf-8"))
    bmap = {s["id"]: s for s in meta["scenes"]}

    # 12 exact hero moments across all 9 scenes (including P7E 1:05 full cohesive Pill check!)
    moments = [
        ("01_P1_Hook_Wordplay",  bmap["P1"]["start_s"] + 3.50),
        ("02_P1_Hook_Question",  bmap["P1"]["start_s"] + 5.45),
        ("03_P2B_Top_Question",  bmap["P2"]["start_s"] + 8.30),
        ("04_P3_Carbon_Pill",    bmap["P3"]["start_s"] + 5.80),
        ("05_P4_Contract_3Rows", bmap["P4"]["start_s"] + 6.35),
        ("06_P5_Chest_Wordplay", bmap["P5"]["start_s"] + 4.10),
        ("07_P6B_Split_Seam",    bmap["P6"]["start_s"] + 7.20),
        ("08_P7C_5050_Split",    bmap["P7"]["start_s"] + 10.60),
        ("09_P7E_1m05s_FullPill",bmap["P7"]["start_s"] + 16.50),
        ("10_P8A_NumberStack",      bmap["P8"]["start_s"] + 4.00),
        ("11_P8C_Corridor_KeyText", bmap["P8"]["start_s"] + 10.70),
        ("12_P9B_CTA_Wordplay",     bmap["P9"]["start_s"] + 9.10),
    ]

    cap = cv2.VideoCapture(MP4_PATH)
    cols, rows = 4, 3
    tw, th = 450, 800
    pad, hdr = 18, 72
    grid = Image.new("RGB", (cols * tw + (cols + 1) * pad, hdr + rows * (th + 38) + (rows + 1) * pad), (16, 18, 24))
    dr = ImageDraw.Draw(grid)
    f_h = get_font(FONT_SANS_BOLD, 28)
    f_l = get_font(FONT_SANS_BOLD, 18)
    dr.text((pad, 20), f"KEY TYPOGRAPHY & FACE-SAFE AUDIT — {VER}.mp4 (12 ARCHETYPE SNAPSHOTS)", font=f_h, fill=(140, 238, 248))

    y_meds = []
    for idx, (label, ts) in enumerate(moments):
        f_no = int(round(ts * 30))
        cap.set(cv2.CAP_PROP_POS_FRAMES, f_no)
        ok, fr = cap.read()
        if not ok:
            continue
        gray = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
        ym = float(np.median(gray))
        yp95 = float(np.percentile(gray, 95))
        y_meds.append((label, round(ym, 1), round(yp95, 1)))
        rgb = cv2.cvtColor(fr, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(rgb).resize((tw, th), Image.Resampling.LANCZOS)
        r, c = idx // cols, idx % cols
        x0 = pad + c * (tw + pad)
        y0 = hdr + pad + r * (th + 38 + pad)
        grid.paste(im, (x0, y0))
        dr.text((x0 + 6, y0 + th + 8), f"{label} ({ts:.1f}s) Y_med={ym:.0f}", font=f_l, fill=(235, 240, 245))
    cap.release()

    key_sheet = os.path.join(OUT_DIR, f"QA_KEY_TYPOGRAPHY_{VER}.jpg")
    grid.save(key_sheet, quality=94)
    print("  Luminance stats:", y_meds)
    print("  Saved key typography audit ->", key_sheet)

    print("\n=== 4. FASTER-WHISPER RENDERED SPEECH COMPLETENESS AUDIT ===")
    subprocess.check_call([
        "ffmpeg", "-y", "-v", "error", "-i", MP4_PATH,
        "-vn", "-ac", "1", "-ar", "16000", TEMP_WAV
    ])
    sr16, pcm = wavfile.read(TEMP_WAV)
    af = pcm.astype(np.float32) / 32768.0
    from faster_whisper import WhisperModel
    wm = WhisperModel("large-v3", device="cuda", compute_type="float16")
    segs, _ = wm.transcribe(af, language="vi", beam_size=5, word_timestamps=True)
    for s in segs:
        print(f"  [{s.start:05.2f}s -> {s.end:05.2f}s] {s.text.strip()}")


if __name__ == "__main__":
    run_qa()
