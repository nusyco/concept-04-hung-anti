import os
import sys
import glob
import json
import math
import time
import shutil
import subprocess
import numpy as np
import cv2
from scipy.io import wavfile
from scipy import signal
from PIL import Image, ImageDraw, ImageFont

ENGINE_DIR = os.path.dirname(os.path.abspath(__file__))
if ENGINE_DIR not in sys.path:
    sys.path.insert(0, ENGINE_DIR)

from hung_gfx import (
    W, H, FPS,
    FONT_COND_BOLD, FONT_SANS_BOLD, FONT_SANS_REG, get_font,
    draw_header_logo, render_black_outro_frame,
    draw_carbon_pill_overlay, draw_split_seam_pill,
    draw_hook_wordplay_p1, draw_question_wordplay_p1,
    draw_chest_wordplay_p5, draw_podium_wordplay_p8a,
    draw_dual_wall_3d_callout, draw_corridor_keytext_p8c,
    draw_minimal_broll_caption, draw_progressive_broll_caption,
    draw_top_question_wordplay, draw_cta_wordplay_p9b,
    apply_radial_zoom_blur, apply_double_light_leak, apply_whip_blur
)
from hung_cards import (
    read_still_cropped, extract_video_segment_frames, extract_aroll_reframed_frames,
    compose_split_50_50, compose_split_3tier,
    build_contract_p4_frames, build_contract_p6_top_frames
)

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--version", default="v8")
ARGS, _ = parser.parse_known_args()
VER = ARGS.version

PROJ_DIR = os.path.dirname(ENGINE_DIR)
SRC_DIR  = os.path.join(PROJ_DIR, "SOURCE")
OUT_DIR  = os.path.join(PROJ_DIR, "04_OUTPUT", VER)
TEMP_ASC = rf"C:\Users\NCPC\AppData\Local\Temp\hung_anti_{VER}"

SR = 48000
SAMPLES_PER_FRAME = SR // FPS  # Exact 1600 samples per frame at 30.00 fps!

# Clean Official Le Parc Place / ParkCity Hanoi Supplementary Paths
C02_DIR   = r"c:\HUB_NUSYCO_ A.I_AGENT\4. WORK - CÔNG VIỆC\Marketing\Concept 02 - Lâm Phát Long - The Emerald"
VID_LT4K  = os.path.join(C02_DIR, "_DUNG_AI_LPL", "web", "4k_Lt0-3aXquLc.webm")
VID_ZL    = os.path.join(C02_DIR, "_DUNG_AI_LPL", "web", "ZLcS-4iS6Ik.mp4")
VID_MXKB  = glob.glob(r"C:\About Me\TÀI NGUYÊN DỰNG\FOOTAGE\01_Le_Parc_Place_ParkCity_Ha_Dong\01_Toan_Canh_Flycam_Tien_Do\*MxKb76QXGi4*.mp4")[0]
VID_ISPH  = glob.glob(r"C:\About Me\TÀI NGUYÊN DỰNG\FOOTAGE\01_Le_Parc_Place_ParkCity_Ha_Dong\*\*3G3UXrFZ-hY*.mp4")[0]

STILL_DIR1 = os.path.join(C02_DIR, "TAI_LIEU_DU_AN", "01_chinh_thuc_parkcityhanoi")
STILL_DIR2 = os.path.join(C02_DIR, "TAI_LIEU_DU_AN", "02_brochure_fliphtml5", "floorplan", "pages")
IMG_TOWER  = os.path.join(STILL_DIR1, "project-tower.webp")
IMG_LOBBY  = os.path.join(STILL_DIR1, "gallery-lift-lobby.webp")
IMG_POOL   = os.path.join(STILL_DIR1, "gallery-pool.webp")
IMG_THELINC= os.path.join(STILL_DIR1, "thelinc-homebanner.webp")
IMG_P05    = os.path.join(STILL_DIR2, "p05.webp")
IMG_P21    = os.path.join(STILL_DIR2, "p21.webp")
IMG_P32    = os.path.join(STILL_DIR2, "p32.webp")

BGM_PATH = r"C:\About Me\TÀI NGUYÊN DỰNG\NHẠC NỀN\02_LUXURY_AMBIENT_PIANO (Phong su Du an - Sa ban - Quang Son)\06_Real_Estate_Corporate_-_Luxury_Property_Tour_(Wavebeats_NCM).mp3"
SFX_ROOT = r"C:\About Me\TÀI NGUYÊN DỰNG\SFX"


# ==============================================================================
# 1. AUDIO HELPERS — 48kHz STEREO PRECISION MIXER
# ==============================================================================
def decode_audio_48k_stereo(media_path):
    """Decode any audio/video file to float32 stereo (-1..1) at 48,000 Hz via FFmpeg pipe."""
    cmd = [
        "ffmpeg", "-v", "error", "-i", media_path,
        "-vn", "-ac", "2", "-ar", str(SR), "-f", "f32le", "pipe:1"
    ]
    raw = subprocess.check_output(cmd)
    arr = np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).copy()
    return arr


def clean_and_level_voice(stereo_arr, is_field_mic=False, target_active_db=-17.2):
    """High-pass rumble + level active speech RMS consistently across DJI mic & Studio VO."""
    fc = 95.0 if is_field_mic else 75.0
    sos = signal.butter(2, fc / (SR * 0.5), btype="highpass", output="sos")
    out = signal.sosfiltfilt(sos, stereo_arr, axis=0).astype(np.float32)

    if is_field_mic:
        b_pk, a_pk = signal.iirpeak(3200.0 / (SR * 0.5), Q=1.2)
        pres = signal.lfilter(b_pk, a_pk, out, axis=0).astype(np.float32)
        out = out + 0.22 * pres

    mono = out.mean(axis=1)
    win = SR // 20
    n_w = len(mono) // win
    if n_w > 0:
        chunks = mono[:n_w * win].reshape(n_w, win)
        rms_w = np.sqrt(np.mean(chunks ** 2, axis=1) + 1e-12)
        active = rms_w[rms_w > (10 ** (-42.0 / 20.0))]
        cur_rms = float(np.percentile(active, 65)) if len(active) > 0 else float(np.sqrt(np.mean(mono ** 2) + 1e-12))
    else:
        cur_rms = float(np.sqrt(np.mean(mono ** 2) + 1e-12))

    want_rms = 10 ** (target_active_db / 20.0)
    gain = min(4.5, want_rms / max(cur_rms, 1e-6))
    out = out * gain

    ceil = 10 ** (-2.0 / 20.0)
    out = ceil * np.tanh(out / ceil)

    fi = min(int(0.020 * SR), len(out) // 4)
    fo = min(int(0.035 * SR), len(out) // 4)
    if fi > 0:
        curve_i = (0.5 - 0.5 * np.cos(np.pi * np.linspace(0, 1, fi, dtype=np.float32)))[:, None]
        out[:fi] *= curve_i
    if fo > 0:
        curve_o = (0.5 + 0.5 * np.cos(np.pi * np.linspace(0, 1, fo, dtype=np.float32)))[:, None]
        out[-fo:] *= curve_o
    return out


def place_sfx(master_sfx, sfx_path, t_sec, peak_db=-16.5, max_dur_s=1.35):
    """Place a distinct SFX normalized to peak_db at exact timestamp t_sec."""
    if not os.path.exists(sfx_path):
        print(f"  [WARN] Missing SFX: {sfx_path}")
        return
    arr = decode_audio_48k_stereo(sfx_path)
    max_len = int(max_dur_s * SR)
    if len(arr) > max_len:
        arr = arr[:max_len].copy()
        fo = min(int(0.12 * SR), len(arr) // 3)
        arr[-fo:] *= np.linspace(1.0, 0.0, fo, dtype=np.float32)[:, None]

    pk = float(np.max(np.abs(arr)) + 1e-9)
    arr = arr * ((10 ** (peak_db / 20.0)) / pk)

    idx0 = max(0, int(round(t_sec * SR)))
    idx1 = min(len(master_sfx), idx0 + len(arr))
    if idx1 > idx0:
        master_sfx[idx0:idx1] += arr[:idx1 - idx0]


# ==============================================================================
# 2. MAIN TIMELINE & SPEECH-SYNCED VISUAL BUILDER (L1–L13)
# ==============================================================================
def build_v1():
    t0_wall = time.time()
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(TEMP_ASC, exist_ok=True)

    pieces_spec = [
        # id, file, is_field, in_s, n_frames, gap_f, trans_type
        ("P1", os.path.join(SRC_DIR, "DJI_20261028100837_0089_D.MP4"), True,  0.36, 177, 10, "radial_zoom"),
        ("P2", os.path.join(SRC_DIR, "VOICE CẢNH 2.wav"),              False, 0.00, 267, 18, "light_leak"),
        ("P3", os.path.join(SRC_DIR, "DJI_20261028105941_0127_D.MP4"), True,  0.50, 201, 12, "whip_v"),
        ("P4", os.path.join(SRC_DIR, "VOICE CẢNH 4.wav"),              False, 0.00, 196, 14, "light_leak"),
        ("P5", os.path.join(SRC_DIR, "DJI_20261028103012_0106_D.MP4"), True,  1.52, 134, 20, "light_leak"),
        ("P6", os.path.join(SRC_DIR, "VOICE CẢNH 6.wav"),              False, 0.00, 394, 14, "light_leak"),
        ("P7", os.path.join(SRC_DIR, "VOICE CẢNH 7.wav"),              False, 0.00, 696, 14, "light_leak"),
        ("P8", os.path.join(SRC_DIR, "VOICE CẢNH 8.wav"),              False, 0.00, 426, 16, "light_leak"),
        ("P9", os.path.join(SRC_DIR, "VOICE CẢNH 9.wav"),              False, 0.00, 312, 12, "light_leak"),
    ]
    OUTRO_FRAMES = 84  # 2.80s solid #000000 brand outro (Hung DNA R1, R18)

    timeline = []
    cur_f = 0
    for pid, fpath, is_field, in_s, n_f, gap_f, tr_type in pieces_spec:
        vis_f = n_f + gap_f
        timeline.append({
            "id": pid,
            "path": fpath,
            "is_field": is_field,
            "in_s": in_s,
            "speech_f": n_f,
            "gap_f": gap_f,
            "vis_f": vis_f,
            "start_f": cur_f,
            "end_f": cur_f + vis_f,
            "start_s": cur_f / float(FPS),
            "end_s": (cur_f + vis_f) / float(FPS),
            "trans_after": tr_type,
        })
        cur_f += vis_f

    outro_start_f = cur_f
    total_frames = outro_start_f + OUTRO_FRAMES
    total_dur_s = total_frames / float(FPS)
    print(f"[TIMELINE] Content={outro_start_f}f ({outro_start_f/FPS:.2f}s) + Outro={OUTRO_FRAMES}f -> Total={total_frames}f ({total_dur_s:.2f}s)")

    # --------------------------------------------------------------------------
    # STEP A: BUILD 48kHz STEREO VOICE + BGM + 25 DISTINCT SPEECH-SYNCED SFX
    # --------------------------------------------------------------------------
    print("[AUDIO] Decoding & leveling 9 spoken pieces + BGM + 25 distinct speech-synced SFX...")
    total_samples = total_frames * SAMPLES_PER_FRAME
    voice_track = np.zeros((total_samples, 2), dtype=np.float32)

    for blk in timeline:
        raw_a = decode_audio_48k_stereo(blk["path"])
        s0 = int(round(blk["in_s"] * SR))
        s_len = blk["speech_f"] * SAMPLES_PER_FRAME
        seg = raw_a[s0:s0 + s_len]
        if len(seg) < s_len:
            seg = np.vstack([seg, np.zeros((s_len - len(seg), 2), dtype=np.float32)])
        leveled = clean_and_level_voice(seg, is_field_mic=blk["is_field"], target_active_db=-17.0)
        dst0 = blk["start_f"] * SAMPLES_PER_FRAME
        voice_track[dst0:dst0 + s_len] = leveled

    bgm_raw = decode_audio_48k_stereo(BGM_PATH)
    while len(bgm_raw) < total_samples + SR:
        bgm_raw = np.vstack([bgm_raw, bgm_raw])
    bgm_seg = bgm_raw[int(1.5 * SR):int(1.5 * SR) + total_samples].copy()
    bgm_rms = float(np.sqrt(np.mean(bgm_seg ** 2) + 1e-12))
    target_bgm_rms = 10 ** ((-17.0 - 14.2) / 20.0)
    bgm_seg *= (target_bgm_rms / bgm_rms)

    # Dynamic BGM envelope ducking (-2.8 dB under active speech, breathes open in pauses & transitions — Locked Rule L23)
    v_mono = np.abs(voice_track.mean(axis=1))
    hop = SR // 50  # 20ms blocks
    n_blk = len(v_mono) // hop
    if n_blk > 0:
        v_blk = v_mono[:n_blk * hop].reshape(n_blk, hop).mean(axis=1)
        win_sm = np.hanning(19)
        win_sm /= win_sm.sum()
        v_env = np.convolve(v_blk, win_sm, mode="same")
        active_mask = np.clip((v_env - 0.006) / 0.024, 0.0, 1.0)
        duck_min = 10 ** (-2.8 / 20.0)
        duck_blk = 1.0 - (1.0 - duck_min) * active_mask
        duck_curve = np.interp(
            np.arange(total_samples, dtype=np.float32),
            np.arange(n_blk, dtype=np.float32) * hop + hop * 0.5,
            duck_blk
        ).astype(np.float32)
        bgm_seg *= duck_curve[:, None]

    fi_b = int(0.6 * SR)
    bgm_seg[:fi_b] *= np.linspace(0.2, 1.0, fi_b, dtype=np.float32)[:, None]
    outro_s0 = outro_start_f * SAMPLES_PER_FRAME
    bgm_seg[outro_s0:] *= np.linspace(1.0, 0.0, total_samples - outro_s0, dtype=np.float32)[:, None]

    sfx_track = np.zeros((total_samples, 2), dtype=np.float32)
    bmap = {b["id"]: b for b in timeline}

    TS1 = os.path.join(SFX_ROOT, "5. Sound Effect", "Bộ Bảo Hay Dùng", "theSOUNDS 1")
    TS2 = os.path.join(SFX_ROOT, "5. Sound Effect", "Bộ Bảo Hay Dùng", "theSOUNDS 2")

    # Multi-layer Studio Sound Design: 59 unique non-repeating SFX cues across P1..P9 (Locked Rule L23!)
    sfx_cues = [
        # --- P1: Hook A-Roll + Multi-Color KeyText Wordplay + KeyText Question ---
        (0.02,                        os.path.join(TS1, "Whoosh", "Quick Whoosh.wav"),         -14.5, 0.8),
        (bmap["P1"]["start_s"] + 0.26, os.path.join(TS1, "Whoosh", "Fabric Whoosh.wav"),       -16.0, 0.7),
        (bmap["P1"]["start_s"] + 1.70, os.path.join(TS1, "Hits", "Subtle Hit.wav"),            -14.5, 0.9),
        (bmap["P1"]["start_s"] + 2.15, os.path.join(TS1, "Clicks", "Touch Screen Click.wav"),  -16.5, 0.5),
        (bmap["P1"]["start_s"] + 4.05, os.path.join(TS1, "Whoosh", "Clean Whoosh.wav"),        -16.0, 0.7),
        (bmap["P1"]["start_s"] + 4.68, os.path.join(TS1, "Clicks", "Pop Flash.wav"),           -15.0, 0.6),
        (bmap["P1"]["end_s"] - 0.14,   os.path.join(TS1, "Whoosh", "Whoosh Impact.wav"),       -14.0, 0.9),

        # --- P2: Living Room + Grand Entrance SUV + Top 2-Color KeyText Question ---
        (bmap["P2"]["start_s"] + 0.40, os.path.join(TS2, "Magic", "Magic  (1).mp3"),           -17.2, 0.8),
        (bmap["P2"]["start_s"] + 4.16, os.path.join(TS1, "Whoosh", "Fluid Whoosh.wav"),        -15.5, 0.7),
        (bmap["P2"]["start_s"] + 6.66, os.path.join(TS1, "Clicks", "Touch Screen Click 2.wav"),-16.0, 0.5),
        (bmap["P2"]["start_s"] + 7.20, os.path.join(TS1, "Hits", "Take it Easy.wav"),          -14.8, 0.9),
        (bmap["P2"]["end_s"] - 0.28,   os.path.join(TS2, "Riser", "ShortRiser1.wav"),          -16.5, 0.45),
        (bmap["P2"]["end_s"] - 0.14,   os.path.join(TS2, "Film Burn", "Film Burn1.wav"),       -14.2, 1.0),

        # --- P3: Outdoor Park A-Roll + Subtle Birds + Carbon Pill ---
        (bmap["P3"]["start_s"] + 0.35, os.path.join(TS1, "Extras", "Birds.wav"),               -24.5, 2.6),
        (bmap["P3"]["start_s"] + 2.60, os.path.join(SFX_ROOT, "HAY DÙNG", "04 Ui Opening.wav"),-15.5, 0.8),
        (bmap["P3"]["start_s"] + 2.74, os.path.join(TS1, "Hits", "Sun Ray.wav"),               -15.2, 0.9),
        (bmap["P3"]["start_s"] + 2.90, os.path.join(TS1, "Clicks", "Sequence Click.wav"),      -16.8, 0.6),
        (bmap["P3"]["end_s"] - 0.12,   os.path.join(SFX_ROOT, "Transition Sound Effects", "Whip Sound Effect ( By Ashish Editz )_01.mp3"), -14.2, 0.8),

        # --- P4: Photorealistic Contract Unfold + 3 Clause Illuminations ---
        (bmap["P4"]["start_s"] + 0.08, os.path.join(TS2, "Paper", "Paper (2).wav"),            -15.5, 0.8),
        (bmap["P4"]["start_s"] + 4.70, os.path.join(SFX_ROOT, "Ui Sound", "SFX- Ui01.mp3"),    -16.0, 0.6),
        (bmap["P4"]["start_s"] + 5.10, os.path.join(SFX_ROOT, "Ui Sound", "SFX- Ui03.mp3"),    -16.0, 0.6),
        (bmap["P4"]["start_s"] + 5.94, os.path.join(SFX_ROOT, "HAY DÙNG", "07 Claim.mp3"),     -15.2, 0.8),
        (bmap["P4"]["end_s"] - 0.28,   os.path.join(TS2, "Riser", "ShortRiser2.wav"),          -16.5, 0.45),
        (bmap["P4"]["end_s"] - 0.14,   os.path.join(TS2, "Film Burn", "Film Burn2.wav"),       -14.2, 1.0),

        # --- P5: Interior A-Roll + Mid-Chest Multi-Color KeyText ---
        (bmap["P5"]["start_s"] + 0.62, os.path.join(TS1, "Clicks", "Click.wav"),               -16.5, 0.4),
        (bmap["P5"]["start_s"] + 1.35, os.path.join(TS2, "Magic", "Magic  (2).mp3"),           -16.0, 0.8),
        (bmap["P5"]["start_s"] + 1.55, os.path.join(TS1, "Hits", "Slow Hit.wav"),              -14.8, 0.9),
        (bmap["P5"]["end_s"] - 0.14,   os.path.join(TS1, "Extras", "Sunflare.wav"),            -14.5, 1.0),

        # --- P6: Walk-through + Whip + Split-Seam Olive Box ("Đối chiếu 4 MỤC") + Porte Cochere ---
        (bmap["P6"]["start_s"] + 0.08, os.path.join(SFX_ROOT, "HAY DÙNG", "03 Interface reveal.wav"), -15.8, 0.8),
        (bmap["P6"]["start_s"] + 3.20, os.path.join(SFX_ROOT, "Transition Sound Effects", "Whip 2 Sound Effect ( By Ashish Editz )_01.mp3"), -14.5, 0.7),
        (bmap["P6"]["start_s"] + 3.38, os.path.join(TS2, "Paper", "Paper (3).wav"),            -15.8, 0.7),
        (bmap["P6"]["start_s"] + 3.55, os.path.join(SFX_ROOT, "Ui Sound", "SFX- Ui05.mp3"),    -16.0, 0.6),
        (bmap["P6"]["start_s"] + 5.50, os.path.join(TS1, "Clicks", "Click2.wav"),              -17.0, 0.4),
        (bmap["P6"]["start_s"] + 9.20, os.path.join(TS1, "Whoosh", "Low Whoosh.wav"),          -15.8, 0.7),
        (bmap["P6"]["end_s"] - 0.28,   os.path.join(TS2, "Riser", "ShortRiser3.wav"),          -16.5, 0.45),
        (bmap["P6"]["end_s"] - 0.14,   os.path.join(TS2, "Film Burn", "Film Burn3.wav"),       -14.2, 1.0),

        # --- P7: 6 Sub-shots Project Scale, Split-Seam Olive Box ("Căn 2-4PN"), & Ecosystem ---
        (bmap["P7"]["start_s"] + 4.00, os.path.join(TS1, "Whoosh", "Deep Low Whoosh.wav"),     -15.0, 0.8),
        (bmap["P7"]["start_s"] + 4.18, os.path.join(SFX_ROOT, "Ui Sound", "SFX- Ui06.mp3"),    -15.8, 0.7),
        (bmap["P7"]["start_s"] + 8.06, os.path.join(SFX_ROOT, "Swoosh", "SFX- Swoosh07.mp3"),  -14.5, 0.7),
        (bmap["P7"]["start_s"] + 8.26, os.path.join(TS2, "Magic", "Magic  (3).mp3"),           -16.0, 0.8),
        (bmap["P7"]["start_s"] + 11.93,os.path.join(TS2, "Whooshes", "Whoosh2.wav"),           -16.2, 0.7),
        (bmap["P7"]["start_s"] + 14.60,os.path.join(TS1, "Clicks", "Pop Flash 2.wav"),         -15.5, 0.7),
        (bmap["P7"]["start_s"] + 19.20,os.path.join(TS2, "Whooshes", "Whoosh5.wav"),           -16.2, 0.7),
        (bmap["P7"]["end_s"] - 0.28,   os.path.join(TS2, "Riser", "ShortRiser4.wav"),          -16.5, 0.45),
        (bmap["P7"]["end_s"] - 0.14,   os.path.join(TS2, "Film Burn", "Film Burn4.wav"),       -14.2, 1.0),

        # --- P8: 4-Story Gold Number-Stack + Corridor Multi-Color KeyText (P8C) + Family Convenience ---
        (bmap["P8"]["start_s"] + 1.80, os.path.join(TS1, "Hits", "Beneath.wav"),               -14.8, 0.9),
        (bmap["P8"]["start_s"] + 2.52, os.path.join(SFX_ROOT, "HAY DÙNG", "06 Sonar ping.mp3"),-17.0, 0.8),
        (bmap["P8"]["start_s"] + 4.72, os.path.join(SFX_ROOT, "Swoosh", "SFX- Swoosh03.mp3"),  -14.8, 0.7),
        (bmap["P8"]["start_s"] + 7.05, os.path.join(SFX_ROOT, "Swoosh", "SFX- Swoosh12.mp3"),  -14.8, 0.7),
        (bmap["P8"]["start_s"] + 8.73, os.path.join(TS2, "Magic", "Magic  (4).mp3"),           -15.8, 0.8),
        (bmap["P8"]["start_s"] + 9.73, os.path.join(TS1, "Extras", "Glass Cling.wav"),         -15.5, 0.8),
        (bmap["P8"]["start_s"] + 11.93,os.path.join(TS2, "Whooshes", "Whoosh8.wav"),           -16.0, 0.7),
        (bmap["P8"]["end_s"] - 0.28,   os.path.join(TS2, "Riser", "ShortRiser5.wav"),          -16.0, 0.5),
        (bmap["P8"]["end_s"] - 0.14,   os.path.join(TS1, "Extras", "Sunflare2.wav"),           -14.2, 1.0),

        # --- P9: CTA Floorplan Carbon Pill + Multi-Color Hotline KeyText ---
        (bmap["P9"]["start_s"] + 0.10, os.path.join(TS2, "Paper", "Paper (4).wav"),            -15.8, 0.7),
        (bmap["P9"]["start_s"] + 1.68, os.path.join(SFX_ROOT, "Ui Sound", "SFX- Ui02.mp3"),    -15.5, 0.7),
        (bmap["P9"]["start_s"] + 5.93, os.path.join(SFX_ROOT, "HAY DÙNG", "02 Message.mp3"),   -14.8, 0.8),
        (bmap["P9"]["start_s"] + 6.86, os.path.join(TS1, "Whoosh", "Short Deep Whoosh.wav"),   -16.2, 0.6),
        (bmap["P9"]["start_s"] + 7.80, os.path.join(TS1, "Clicks", "Quick Shutter 2.wav"),     -16.5, 0.5),
    ]
    used_sfx = set()
    for ts, spath, pdb, mdur in sfx_cues:
        assert os.path.exists(spath), f"Missing SFX path: {spath}"
        assert spath not in used_sfx, f"Duplicate SFX path: {spath}"
        used_sfx.add(spath)
        place_sfx(sfx_track, spath, ts, peak_db=pdb, max_dur_s=mdur)

    mix = voice_track + bgm_seg + sfx_track
    tp_ceil = 10 ** (-1.2 / 20.0)
    mix = tp_ceil * np.tanh(mix / tp_ceil)

    raw_wav = os.path.join(TEMP_ASC, "mix_raw.wav")
    norm_wav = os.path.join(TEMP_ASC, "mix_master.wav")
    wavfile.write(raw_wav, SR, (mix * 32767.0).astype(np.int16))

    subprocess.check_call([
        "ffmpeg", "-y", "-v", "error", "-i", raw_wav,
        "-af", "loudnorm=I=-14.8:TP=-1.2:LRA=6.5",
        "-ar", str(SR), "-ac", "2", norm_wav
    ])
    print(f"[AUDIO] Mastered {len(used_sfx)} unique SFX + Dynamic BGM + Voice -> {norm_wav}")

    # --------------------------------------------------------------------------
    # STEP B: RENDER ALL 9 SCENE VISUAL BLOCKS + SPEECH-SYNCED 3D OVERLAYS
    # --------------------------------------------------------------------------
    scene_frames = {}

    # --- P1: Hook A-Roll (DJI_0089) + Multi-Color KeyText Wordplay -> 2-Color KeyText Question (L14, L15, L18, L19) ---
    p1 = bmap["P1"]
    print(f"[VIDEO] Building P1 ({p1['vis_f']}f)...")
    f_p1 = extract_aroll_reframed_frames(
        p1["path"], p1["in_s"], p1["vis_f"],
        target_face_cx=0.66, target_face_cy=0.34,
        base_crop_h=2280, zoom_end=1.07, bottom_scrim=0.16
    )
    for i in range(p1["vis_f"]):
        if i < 121:  # 0.00s .. 4.03s (Settles at 2.20s -> holds 100% solid for 1.63s, out_f=6!)
            draw_hook_wordplay_p1(f_p1[i], i, 121 - i)
        elif 121 <= i < p1["vis_f"] - 1:  # 4.03s .. 6.20s (Holds 100% solid for 1.15s, out_f=6!)
            draw_question_wordplay_p1(f_p1[i], i - 121, (p1["vis_f"] - 1) - i)
    scene_frames["P1"] = f_p1

    # --- P2: Problem Setup (P2A Living Room + P2B Grand Entrance SUV Arrival — L14, L15) ---
    p2 = bmap["P2"]
    n2a = 126  # 4.20s
    n2b = p2["vis_f"] - n2a
    print(f"[VIDEO] Building P2 ({n2a}f + {n2b}f)...")
    f_p2a = extract_video_segment_frames(
        os.path.join(SRC_DIR, "DJI_20261028114628_0147_D.MP4"),
        t_start=2.4, n_frames=n2a,
        focus_cx=0.50, focus_cy=0.48, zoom_start=1.00, zoom_end=1.06,
        bright_mode="aroll", bottom_scrim=0.22
    )
    # Single-line B-Roll caption appears smoothly as ONE cohesive line & holds > 3.1s (L14, L15)!
    for i in range(n2a):
        if i >= 12:
            draw_minimal_broll_caption(
                f_p2a[i], i - 12, n2a - i,
                "Tầng đẹp, view thoáng, tiện ích có gì ?",
                cy_norm=0.755, style="focus_rack_in"
            )

    f_p2b = extract_video_segment_frames(
        VID_LT4K, t_start=16.8, n_frames=n2b,
        crop_region=(0.0, 0.0, 1.0, 0.85),
        focus_cx=0.48, focus_cy=0.55, zoom_start=1.00, zoom_end=1.07,
        bright_mode="broll", bottom_scrim=0.26
    )
    for i in range(n2b):
        if i >= 4:
            draw_minimal_broll_caption(
                f_p2b[i], i - 4, n2b - i,
                "Với gia đình có ô tô - cần hỏi ngay từ đầu:",
                cy_norm=0.775, style="focus_rack_in"
            )
        # 2-Color KeyText Top Question ("XE CỦA MÌNH / SẼ ĐỖ Ở ĐÂU ?") — holds solid for 2.10s (L14, L15)!
        if i >= 74:
            draw_top_question_wordplay(
                f_p2b[i], i - 74, n2b - i,
                "XE CỦA MÌNH", "SẼ ĐỖ Ở ĐÂU ?", d_l2=16, cy_norm=0.205
            )
    scene_frames["P2"] = f_p2a + f_p2b

    # --- P3: Core USP A-Roll (DJI_0127) + Cohesive Full-Display Carbon Pill (L14, L15) ---
    p3 = bmap["P3"]
    print(f"[VIDEO] Building P3 ({p3['vis_f']}f)...")
    f_p3 = extract_aroll_reframed_frames(
        p3["path"], p3["in_s"], p3["vis_f"],
        target_face_cx=0.50, target_face_cy=0.33,
        base_crop_h=2080, zoom_end=1.07, bottom_scrim=0.18
    )
    p3_pill_start = 78  # Opens cleanly at 2.60s & holds 100% solid for 4.30 full seconds!
    for i in range(p3["vis_f"]):
        if i < p3_pill_start:
            if i >= 3:
                draw_minimal_broll_caption(f_p3[i], i - 3, p3_pill_start - i, "Tại Le Parc Place - ParkCity Hanoi", cy_norm=0.765, style="focus_rack_in")
        else:
            draw_carbon_pill_overlay(
                f_p3[i], i - p3_pill_start, p3["vis_f"] - i,
                "ĐIỂM KHÁC BIỆT", "SLOT Ô TÔ ĐỊNH DANH", "HỢP ĐỒNG MUA BÁN CHỖ ĐỂ XE RIÊNG",
                cy_norm=0.818, d_tag=2, d_l1=4, d_l2=7
            )
    scene_frames["P3"] = f_p3

    # --- P4: Photorealistic Contract Showcase (3 Rows Synced to Voice + Long Cohesive Caption Hold) ---
    p4 = bmap["P4"]
    print(f"[VIDEO] Building P4 ({p4['vis_f']}f)...")
    f_p4 = build_contract_p4_frames(p4["vis_f"], t_row1=4.70, t_row2=5.10, t_row3=5.94)
    for i in range(p4["vis_f"]):
        if i >= 4:
            draw_minimal_broll_caption(
                f_p4[i], i - 4, p4["vis_f"] - i,
                "Định danh: chỗ đỗ xe xác định cụ thể trên hợp đồng",
                cy_norm=0.922, style="focus_rack_in"
            )
    scene_frames["P4"] = f_p4

    # --- P5: Interior A-Roll (DJI_0106) + Multi-Color Mid-Chest KeyText (Tight Reference Spacing & 2.3s Solid Hold!) ---
    p5 = bmap["P5"]
    print(f"[VIDEO] Building P5 ({p5['vis_f']}f)...")
    f_p5 = extract_aroll_reframed_frames(
        p5["path"], p5["in_s"], p5["vis_f"],
        target_face_cx=0.50, target_face_cy=0.30,
        base_crop_h=1980, zoom_end=1.06, bottom_scrim=0.14
    )
    st_f5 = 18  # Starts at 0.60s ("nhìn rõ tên văn bản / Hợp đồng MUA BÁN / CHỖ ĐỂ XE") -> holds solid for 2.30s!
    for i in range(p5["vis_f"]):
        if i >= st_f5:
            draw_chest_wordplay_p5(f_p5[i], i - st_f5, p5["vis_f"] - i, cy_norm=0.668)
    scene_frames["P5"] = f_p5

    # --- P6: Practical Value (P6A Walk-through + Whip + P6B 50/50 Contract Split + P6C Porte Cochere — L14, L15) ---
    p6 = bmap["P6"]
    n6a, n6b = 98, 178
    n6c = p6["vis_f"] - n6a - n6b
    print(f"[VIDEO] Building P6 ({n6a}f + {n6b}f + {n6c}f)...")
    f_p6a = extract_video_segment_frames(
        os.path.join(SRC_DIR, "DJI_20261028114853_0149_D.MP4"),
        t_start=0.8, n_frames=n6a,
        focus_cx=0.50, focus_cy=0.46, zoom_start=1.00, zoom_end=1.06,
        bright_mode="aroll", bottom_scrim=0.22
    )
    for i in range(n6a):
        draw_carbon_pill_overlay(
            f_p6a[i], i, n6a - i,
            "GIÁ TRỊ THỰC TẾ", "SỰ RÕ RÀNG RẤT ĐÁNG GIÁ", "VỚI CĂN HỘ HÌNH THÀNH TRONG TƯƠNG LAI",
            cy_norm=0.818, d_tag=2, d_l1=4, d_l2=7
        )

    top_6b = build_contract_p6_top_frames(n6b, rel_triggers=(2.23, 2.95, 3.55, 4.20))
    bot_6b = read_still_cropped(
        IMG_P21, W, 960, zoom_start=1.00, zoom_end=1.08, n_frames=n6b,
        focus_cx=0.50, focus_cy=0.56, crop_region=(0.04, 0.08, 0.96, 0.94)
    )
    f_p6b = compose_split_50_50(top_6b, bot_6b, divider_px=4)
    # Cohesive Split-Seam Olive Pill opens immediately & holds solid for 5.1s (0% partial wipes — L14, L15, L16)!
    for i in range(n6b):
        if i >= 4:
            draw_split_seam_pill(
                f_p6b[i], i - 4, n6b - i,
                "Đối chiếu", "4 MỤC", "TRONG HỢP ĐỒNG", "( Vị trí - Thời hạn - Chi phí )",
                cy_norm=0.50, d_sc=3, d_big=5, d_r1=7, d_r2=9
            )

    for k in range(6):
        idx_a = n6a - 3 + k
        if 0 <= idx_a < n6a:
            f_p6a[idx_a] = apply_whip_blur(f_p6a[n6a - 4], f_p6b[3], (k + 1) / 7.0, direction="vertical")

    f_p6c = extract_video_segment_frames(
        VID_LT4K, t_start=25.0, n_frames=n6c,
        crop_region=(0.0, 0.0, 1.0, 0.85),
        focus_cx=0.50, focus_cy=0.52, zoom_start=1.00, zoom_end=1.06,
        bright_mode="broll", bottom_scrim=0.24
    )
    for i in range(n6c):
        if i >= 5:
            draw_minimal_broll_caption(
                f_p6c[i], i - 5, n6c - i,
                "Gia đình có 1 hay nhiều ô tô - chủ động phương án từ đầu",
                cy_norm=0.760, style="focus_rack_in"
            )
    scene_frames["P6"] = f_p6a + f_p6b + f_p6c

    # --- P7: Project & Ecosystem Overview (6 Sub-shots — Cohesive Full Pills & Captions, 0% Wipe at 1:04–1:06! L14, L15, L16) ---
    p7 = bmap["P7"]
    n7a, n7b, n7c, n7d, n7e = 120, 124, 114, 80, 138
    n7f = p7["vis_f"] - (n7a + n7b + n7c + n7d + n7e)
    print(f"[VIDEO] Building P7 ({n7a}+{n7b}+{n7c}+{n7d}+{n7e}+{n7f}f)...")

    f_p7a = extract_video_segment_frames(
        VID_LT4K, t_start=88.2, n_frames=n7a,
        crop_region=(0.0, 0.0, 1.0, 0.85),
        focus_cx=0.50, focus_cy=0.48, zoom_start=1.00, zoom_end=1.06,
        bright_mode="broll", bottom_scrim=0.22
    )
    for i in range(n7a):
        if i >= 12:
            draw_minimal_broll_caption(
                f_p7a[i], i - 12, n7a - i,
                "Le Parc Place - tọa lạc tại KĐT ParkCity Hanoi",
                cy_norm=0.755, style="focus_rack_in"
            )

    t7_1 = extract_video_segment_frames(VID_MXKB, 16.0, n7b, W, 640, crop_region=(0.05, 0.12, 0.95, 0.95), zoom_end=1.06)
    t7_2 = extract_video_segment_frames(VID_MXKB, 41.5, n7b, W, 640, crop_region=(0.05, 0.12, 0.95, 0.95), zoom_end=1.06)
    t7_3 = extract_video_segment_frames(VID_MXKB, 67.0, n7b, W, 640, crop_region=(0.05, 0.12, 0.95, 0.95), zoom_end=1.06)
    f_p7b = compose_split_3tier(t7_1, t7_2, t7_3, divider_px=4)
    for i in range(n7b):
        draw_carbon_pill_overlay(
            f_p7b[i], i, n7b - i,
            "QUY MÔ ĐÔ THỊ", "KĐT PARKCITY 77,4 HA", "LÊ TRỌNG TẤN - DƯƠNG NỘI - HÀ NỘI",
            cy_norm=0.818, d_tag=2, d_l1=4, d_l2=7
        )

    top_7c = extract_video_segment_frames(
        os.path.join(SRC_DIR, "DJI_20261028114805_0148_D.MP4"),
        t_start=4.0, n_frames=n7c, w_out=W, h_out=960,
        focus_cx=0.50, focus_cy=0.52, zoom_end=1.06, bright_mode="aroll"
    )
    bot_7c = extract_video_segment_frames(
        os.path.join(SRC_DIR, "DJI_20261028114628_0147_D.MP4"),
        t_start=28.8, n_frames=n7c, w_out=W, h_out=960,
        focus_cx=0.45, focus_cy=0.54, zoom_end=1.06, bright_mode="aroll"
    )
    f_p7c = compose_split_50_50(top_7c, bot_7c, divider_px=4)
    for i in range(n7c):
        if i >= 4:
            draw_split_seam_pill(
                f_p7c[i], i - 4, n7c - i,
                "Căn", "2-4PN", "& BIỆT THỰ TRÊN KHÔNG", "( Đa dạng diện tích lựa chọn )",
                cy_norm=0.50, d_sc=3, d_big=5, d_r1=7, d_r2=9
            )

    for k in range(6):
        idx_b = n7b - 3 + k
        if 0 <= idx_b < n7b:
            f_p7b[idx_b] = apply_whip_blur(f_p7b[n7b - 4], f_p7c[3], (k + 1) / 7.0, direction="horizontal")

    f_p7d = read_still_cropped(IMG_P05, W, H, zoom_start=1.00, zoom_end=1.07, n_frames=n7d, bottom_scrim=0.22)
    for i in range(n7d):
        if i >= 5:
            draw_minimal_broll_caption(
                f_p7d[i], i - 5, n7d - i,
                "Tầm nhìn thoáng hướng công viên & hồ trung tâm",
                cy_norm=0.755, style="focus_rack_in"
            )

    # P7E (1:03–1:07): 100% Full-Display Cohesive Carbon Pill right from start — ZERO partial wipe (Locked Rule L16)!
    e7_1 = extract_video_segment_frames(VID_ISPH, 16.5, n7e, W, 640, crop_region=(0.0, 0.15, 1.0, 0.78), zoom_start=1.00, zoom_end=1.06)
    e7_2 = extract_video_segment_frames(VID_LT4K, 40.5, n7e, W, 640, crop_region=(0.0, 0.0, 1.0, 0.85), zoom_end=1.07)
    e7_3 = read_still_cropped(IMG_THELINC, W, 640, zoom_start=1.00, zoom_end=1.09, n_frames=n7e)
    f_p7e = compose_split_3tier(e7_1, e7_2, e7_3, divider_px=4)
    for i in range(n7e):
        draw_carbon_pill_overlay(
            f_p7e[i], i, n7e - i,
            "HỆ SINH THÁI", "ISPH - PARKCITY CLUB - THE LINC", "HỌC TẬP - RÈN LUYỆN - MUA SẮM NỘI KHU",
            cy_norm=0.818, d_tag=2, d_l1=4, d_l2=7
        )

    f_p7f = extract_video_segment_frames(
        VID_LT4K, t_start=58.2, n_frames=n7f,
        crop_region=(0.0, 0.0, 1.0, 0.85),
        focus_cx=0.45, focus_cy=0.50, zoom_start=1.00, zoom_end=1.06,
        bright_mode="broll", bottom_scrim=0.22
    )
    for i in range(n7f):
        if i >= 5:
            draw_minimal_broll_caption(
                f_p7f[i], i - 5, n7f - i,
                "Thuận tiện học tập, rèn luyện sức khỏe & mua sắm",
                cy_norm=0.755, style="focus_rack_in"
            )

    scene_frames["P7"] = f_p7a + f_p7b + f_p7c + f_p7d + f_p7e + f_p7f

    # --- P8: 4-Story Above-Ground Parking (Gold Hero) & Harmonious Multi-Color Corridor KeyText (L14, L15, L22) ---
    p8 = bmap["P8"]
    n8a, n8b, n8c = 144, 70, 144
    n8d = p8["vis_f"] - (n8a + n8b + n8c)
    print(f"[VIDEO] Building P8 ({n8a}+{n8b}+{n8c}+{n8d}f)...")

    f_p8a = extract_video_segment_frames(
        VID_LT4K, t_start=16.0, n_frames=n8a,
        crop_region=(0.0, 0.0, 1.0, 0.85),
        focus_cx=0.52, focus_cy=0.48, zoom_start=1.00, zoom_end=1.07,
        bright_mode="broll", bottom_scrim=0.58
    )
    for i in range(n8a):
        if 4 <= i < 52:
            draw_minimal_broll_caption(f_p8a[i], i - 4, 52 - i, "Trở lại với câu chuyện chỗ đỗ xe...", cy_norm=0.775, style="focus_rack_in")
        elif i >= 54:  # Opens at 1.80s & holds 100% solid for 1.73s!
            draw_podium_wordplay_p8a(f_p8a[i], i - 54, n8a - i, cy_norm=0.775)

    top_8b = extract_video_segment_frames(VID_ZL, 196.0, n8b, W, 960, focus_cx=0.45, focus_cy=0.55, zoom_end=1.05)
    bot_8b = extract_video_segment_frames(VID_ZL, 202.8, n8b, W, 960, focus_cx=0.52, focus_cy=0.55, zoom_end=1.05)
    f_p8b = compose_split_50_50(top_8b, bot_8b, divider_px=4)
    for i in range(n8b):
        if i >= 5:
            draw_minimal_broll_caption(
                f_p8b[i], i - 5, n8b - i,
                "Đón ánh sáng & thông gió tự nhiên",
                cy_norm=0.50, style="focus_rack_in"
            )

    for k in range(6):
        idx_8a = n8a - 3 + k
        if 0 <= idx_8a < n8a:
            f_p8a[idx_8a] = apply_whip_blur(f_p8a[n8a - 4], f_p8b[3], (k + 1) / 7.0, direction="horizontal")

    # P8C: Le Parc Place Corridor (`DJI_0148` t=16.20s..21.00s) + Harmonious Multi-Color KeyText Lockup (Locked Rule L22)!
    f_p8c = extract_video_segment_frames(
        os.path.join(SRC_DIR, "DJI_20261028114805_0148_D.MP4"),
        t_start=16.20, n_frames=n8c,
        focus_cx=0.50, focus_cy=0.50, zoom_start=1.00, zoom_end=1.05,
        bright_mode="aroll", bottom_scrim=0.38
    )
    for i in range(n8c):
        draw_corridor_keytext_p8c(f_p8c[i], i, n8c - i, cy_norm=0.772)

    for k in range(6):
        idx_8b = n8b - 3 + k
        if 0 <= idx_8b < n8b:
            f_p8b[idx_8b] = apply_whip_blur(f_p8b[n8b - 4], f_p8c[3], (k + 1) / 7.0, direction="vertical")

    f_p8d = extract_video_segment_frames(
        VID_LT4K, t_start=33.0, n_frames=n8d,
        crop_region=(0.0, 0.0, 1.0, 0.85),
        focus_cx=0.50, focus_cy=0.50, zoom_start=1.00, zoom_end=1.06,
        bright_mode="broll", bottom_scrim=0.22
    )
    for i in range(n8d):
        if i >= 5:
            draw_minimal_broll_caption(
                f_p8d[i], i - 5, n8d - i,
                "Sự thuận tiện gia đình mình sử dụng mỗi ngày",
                cy_norm=0.755, style="focus_rack_in"
            )

    scene_frames["P8"] = f_p8a + f_p8b + f_p8c + f_p8d

    # --- P9: Call To Action (P9A 50/50 Floorplan + Full Carbon Pill -> P9B Presenter + Multi-Color CTA KeyText) ---
    p9 = bmap["P9"]
    n9a = 178  # 5.93s
    n9b = p9["vis_f"] - n9a
    print(f"[VIDEO] Building P9 ({n9a}f + {n9b}f) + Black Outro ({OUTRO_FRAMES}f)...")

    top_9a = read_still_cropped(IMG_P32, W, 960, zoom_start=1.00, zoom_end=1.08, n_frames=n9a, focus_cx=0.52, focus_cy=0.58, crop_region=(0.04, 0.08, 0.96, 0.94))
    bot_9a = read_still_cropped(IMG_LOBBY, W, 960, zoom_start=1.00, zoom_end=1.07, n_frames=n9a)
    f_p9a = compose_split_50_50(top_9a, bot_9a, divider_px=4)
    for i in range(n9a):
        if 3 <= i < 48:
            draw_minimal_broll_caption(f_p9a[i], i - 3, 48 - i, "Anh chị quan tâm căn hộ tại Le Parc Place?", cy_norm=0.815, style="focus_rack_in")
        elif i >= 50:
            draw_carbon_pill_overlay(
                f_p9a[i], i - 50, n9a - i,
                "NHẬN TÀI LIỆU GỐC", "MẶT BẰNG & MẪU HỢP ĐỒNG", "ĐỂ LẠI SỐ ĐIỆN THOẠI EM GỬI NGAY",
                cy_norm=0.815, d_tag=2, d_l1=4, d_l2=7
            )

    f_p9b = extract_video_segment_frames(
        os.path.join(SRC_DIR, "DJI_20261028114931_0151_D.MP4"),
        t_start=5.0, n_frames=n9b,
        crop_region=(0.0, 0.30, 1.0, 1.0),
        focus_cx=0.50, focus_cy=0.50, zoom_start=1.00, zoom_end=1.06,
        bright_mode="aroll", bottom_scrim=0.36
    )
    for i in range(n9b):
        draw_cta_wordplay_p9b(f_p9b[i], i, n9b - i, cy_norm=0.760)
    scene_frames["P9"] = f_p9a + f_p9b

    # --------------------------------------------------------------------------
    # STEP C: ASSEMBLE MASTER FRAME STREAM + GLOBAL TRANSITIONS + HEADER LOGO
    # --------------------------------------------------------------------------
    all_frames = []
    for blk in timeline:
        flist = scene_frames[blk["id"]]
        assert len(flist) == blk["vis_f"], f"Mismatch {blk['id']}: {len(flist)} vs {blk['vis_f']}"
        all_frames.extend(flist)

    outro_frames = [render_black_outro_frame(i, OUTRO_FRAMES) for i in range(OUTRO_FRAMES)]
    all_frames.extend(outro_frames)
    assert len(all_frames) == total_frames

    for f_i in range(6):
        strength = 0.22 * ((6 - f_i) / 6.0)
        all_frames[f_i] = apply_radial_zoom_blur(all_frames[f_i], strength=strength, steps=7)

    for blk in timeline:
        cut_f = blk["end_f"]
        tr = blk["trans_after"]
        if tr == "radial_zoom":
            for rel in range(-3, 4):
                idx = cut_f + rel
                if 0 <= idx < outro_start_f:
                    st = 0.22 * (1.0 - abs(rel) / 4.0)
                    all_frames[idx] = apply_radial_zoom_blur(all_frames[idx], strength=st, steps=7)
        elif tr == "whip_v":
            p_prev = all_frames[cut_f - 4].copy()
            p_next = all_frames[cut_f + 3].copy()
            for k, rel in enumerate(range(-3, 3)):
                idx = cut_f + rel
                if 0 <= idx < outro_start_f:
                    all_frames[idx] = apply_whip_blur(p_prev, p_next, (k + 1) / 7.0, direction="vertical")
        elif tr == "light_leak":
            for rel in range(-4, 5):
                idx = cut_f + rel
                if 0 <= idx < total_frames:
                    all_frames[idx] = apply_double_light_leak(all_frames[idx], rel)

    for idx in range(outro_start_f):
        draw_header_logo(all_frames[idx], opacity=0.92)

    # --------------------------------------------------------------------------
    # STEP D: AUTO-SELECT HARDWARE NVENC OR HIGH-BITRATE LIBX264 + MUX 48kHz AUDIO
    # --------------------------------------------------------------------------
    temp_mp4 = os.path.join(TEMP_ASC, f"{VER}_out.mp4")
    final_mp4 = os.path.join(OUT_DIR, f"{VER}.mp4")

    nv_probe = subprocess.run(
        ["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "color=black:s=256x256:d=0.1", "-c:v", "h264_nvenc", "-f", "null", "-"],
        capture_output=True
    )
    if nv_probe.returncode == 0:
        v_enc_args = ["-c:v", "h264_nvenc", "-preset", "p6", "-cq", "18", "-b:v", "0", "-pix_fmt", "yuv420p"]
        enc_label = "h264_nvenc (-cq 18)"
    else:
        v_enc_args = ["-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p"]
        enc_label = "libx264 (-crf 17 -preset fast)"

    print(f"[ENCODE] Streaming {total_frames} frames (1080x1920 @ 30fps) to {enc_label}...")
    ff_cmd = [
        "ffmpeg", "-y", "-v", "error",
        "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "pipe:0",
        "-i", norm_wav,
        *v_enc_args,
        "-c:a", "aac", "-b:a", "256k", "-ar", str(SR),
        "-movflags", "+faststart",
        temp_mp4
    ]
    proc = subprocess.Popen(ff_cmd, stdin=subprocess.PIPE)
    for fr in all_frames:
        proc.stdin.write(fr.tobytes())
    proc.stdin.close()
    ret = proc.wait()
    if ret != 0:
        raise RuntimeError(f"FFmpeg encode failed with code {ret}")

    shutil.copy2(temp_mp4, final_mp4)
    print(f"[DONE] Saved Master MP4 -> {final_mp4} ({os.path.getsize(final_mp4)/(1024*1024):.1f} MB)")

    qa_path = os.path.join(OUT_DIR, f"QA_CONTACT_SHEET_{VER}.jpg")
    build_qa_contact_sheet(all_frames, qa_path)

    meta_path = os.path.join(OUT_DIR, f"{VER}_timeline_meta.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump({
            "version": VER,
            "resolution": f"{W}x{H}",
            "fps": FPS,
            "total_frames": total_frames,
            "total_duration_s": round(total_dur_s, 3),
            "outro_start_s": round(outro_start_f / float(FPS), 3),
            "unique_sfx_count": len(used_sfx),
            "scenes": timeline,
        }, f, ensure_ascii=False, indent=2)

    print(f"[COMPLETE] Total build ({VER}) finished in {time.time() - t0_wall:.1f}s!")


def build_qa_contact_sheet(all_frames, out_jpg_path):
    """Extract 24 evenly spaced frames across the full video into a clean 4x6 QA sheet."""
    n_total = len(all_frames)
    sample_indices = [int(round(i * (n_total - 1) / 23.0)) for i in range(24)]

    cols, rows = 4, 6
    tw, th = 360, 640
    pad, top_bar = 18, 86
    sheet_w = cols * tw + (cols + 1) * pad
    sheet_h = top_bar + rows * (th + 42) + (rows + 1) * pad

    sheet = Image.new("RGB", (sheet_w, sheet_h), (18, 20, 26))
    dr = ImageDraw.Draw(sheet)
    f_hdr = get_font(FONT_SANS_BOLD, 30)
    f_lbl = get_font(FONT_SANS_BOLD, 18)

    dr.text((pad, 24), f"QA CONTACT SHEET — CONCEPT 04 (HUNG ANTI) - LE PARC PLACE - {VER} (24 FRAMES)", font=f_hdr, fill=(245, 212, 118))

    for idx_k, f_idx in enumerate(sample_indices):
        r = idx_k // cols
        c = idx_k % cols
        x0 = pad + c * (tw + pad)
        y0 = top_bar + pad + r * (th + 42 + pad)

        rgb = cv2.cvtColor(all_frames[f_idx], cv2.COLOR_BGR2RGB)
        thumb = Image.fromarray(rgb).resize((tw, th), Image.Resampling.LANCZOS)
        sheet.paste(thumb, (x0, y0))
        dr.rectangle([x0, y0, x0 + tw - 1, y0 + th - 1], outline=(70, 80, 96), width=2)

        ts = f_idx / float(FPS)
        lbl = f"#{idx_k+1:02d}  |  t = {ts:05.2f}s  (f={f_idx})"
        dr.text((x0 + 6, y0 + th + 10), lbl, font=f_lbl, fill=(225, 232, 240))

    sheet.save(out_jpg_path, quality=93)
    print(f"[QA] Saved 24-frame QA Contact Sheet -> {out_jpg_path}")


if __name__ == "__main__":
    build_v1()
