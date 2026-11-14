import os
import math
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from hung_gfx import (
    W, H, FPS,
    FONT_COND_BLACK, FONT_COND_BOLD, FONT_TRAJAN,
    FONT_ITALIC_SER, FONT_BOLD_SER, FONT_SANS_BOLD, FONT_SANS_REG,
    get_font, fit_font, polish_frame_bright, ease_in_out_cubic, ease_in_out_sine
)


# ==============================================================================
# SUB-PIXEL FLOATING-POINT KEYFRAME ZOOM ENGINE (LOCKED RULE L10 — 0% JITTER!)
# ==============================================================================
def keyframe_zoom_ease(prog):
    """
    Cinema Keyframe Zoom Curve (Smooth Sine/Cubic blend):
    Gentle 18% ease-in ramp -> silky steady middle glide -> gentle 18% ease-out cushion.
    Never freezes on early/late frames and never snaps!
    """
    p = max(0.0, min(1.0, float(prog)))
    # Blend 65% smooth Sine Ease-In-Out + 35% linear steady glide so motion is visible & buttery from frame 1!
    return 0.65 * (0.5 * (1.0 - math.cos(math.pi * p))) + 0.35 * p


def _prepare_static_oversampled_base(bgr, w_out, h_out, focus_cx=0.50, focus_cy=0.50, oversample=1.35):
    """
    Stage 1 of Sub-Pixel Keyframe Zoom (Locked Rule L10):
    Extract a FIXED zoom=1.0 aspect-matched window (bounds never vary per frame!)
    and anti-alias pre-filter to 1.35x output resolution via INTER_AREA to prevent high-freq shimmer.
    """
    Hs, Ws = bgr.shape[:2]
    target_aspect = w_out / float(h_out)
    src_aspect = Ws / float(Hs)
    if src_aspect > target_aspect:
        bh = Hs
        bw = min(Ws, int(round(Hs * target_aspect)))
    else:
        bw = Ws
        bh = min(Hs, int(round(Ws / target_aspect)))

    cx = int(round(Ws * float(focus_cx)))
    cy = int(round(Hs * float(focus_cy)))
    bx0 = max(0, min(Ws - bw, cx - bw // 2))
    by0 = max(0, min(Hs - bh, cy - bh // 2))
    patch = bgr[by0:by0 + bh, bx0:bx0 + bw]

    w_ov = int(round(w_out * oversample))
    h_ov = int(round(h_out * oversample))
    if bw > w_ov and bh > h_ov:
        return cv2.resize(patch, (w_ov, h_ov), interpolation=cv2.INTER_AREA)
    return patch


def warp_subpixel_window(src_bgr, w_out, h_out, win_cx_px, win_cy_px, win_w_px, win_h_px):
    """
    Stage 2 of Sub-Pixel Keyframe Zoom (Locked Rule L10):
    Sample arbitrary floating-point window (win_cx_px, win_cy_px, win_w_px, win_h_px) from src_bgr
    into (w_out, h_out) with exact pixel-center alignment (+0.5 / -0.5) via float32 warpAffine.
    Eliminates 100% of integer crop stepping and odd/even 0.5px center wobble!
    """
    sx_scale = float(win_w_px) / float(w_out)
    sy_scale = float(win_h_px) / float(h_out)
    cx_src = float(win_cx_px) - 0.5
    cy_src = float(win_cy_px) - 0.5
    cx_dst = 0.5 * float(w_out) - 0.5
    cy_dst = 0.5 * float(h_out) - 0.5

    tx = cx_src - cx_dst * sx_scale
    ty = cy_src - cy_dst * sy_scale
    M_inv = np.array([[sx_scale, 0.0, tx], [0.0, sy_scale, ty]], dtype=np.float32)
    return cv2.warpAffine(
        src_bgr, M_inv, (w_out, h_out),
        flags=cv2.INTER_CUBIC | cv2.WARP_INVERSE_MAP,
        borderMode=cv2.BORDER_REFLECT_101
    )


def warp_subpixel_keyframe(ov_bgr, w_out, h_out, zoom_z, pan_dx_norm=0.0, pan_dy_norm=0.0):
    """Zoom & pan smoothly inside an oversampled base canvas with 0.0001px floating-point accuracy."""
    H_ov, W_ov = ov_bgr.shape[:2]
    z = max(1.0, float(zoom_z))
    win_w = float(W_ov) / z
    win_h = float(H_ov) / z
    cx = (0.5 + float(pan_dx_norm)) * float(W_ov)
    cy = (0.5 + float(pan_dy_norm)) * float(H_ov)
    cx = max(0.5 * win_w, min(float(W_ov) - 0.5 * win_w, cx))
    cy = max(0.5 * win_h, min(float(H_ov) - 0.5 * win_h, cy))
    return warp_subpixel_window(ov_bgr, w_out, h_out, cx, cy, win_w, win_h)


def polish_frame_bright_any(bgr, mode="broll"):
    """Bright fresh luxury grade for arbitrary dimensions (e.g. 1080x960 or 1080x640 split tiers)."""
    from hung_gfx import _LUT_AR, _LUT_BR
    lut = _LUT_AR if mode == "aroll" else _LUT_BR
    out = cv2.LUT(bgr, lut).astype(np.float32)
    if mode == "aroll":
        out[:, :, 2] *= 1.032
        out[:, :, 1] *= 1.010
        out[:, :, 0] *= 0.978
    else:
        out[:, :, 2] *= 1.020
        out[:, :, 0] *= 0.990
    out = np.clip(out, 0, 255).astype(np.uint8)
    hsv = cv2.cvtColor(out, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] * (1.13 if mode == "aroll" else 1.10), 0, 255)
    return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)


def read_still_cropped(img_path, w_out, h_out, zoom_start=1.00, zoom_end=1.09, n_frames=90,
                       focus_cx=0.50, focus_cy=0.50, crop_region=(0.0, 0.0, 1.0, 1.0),
                       bright_mode="broll", bottom_scrim=0.0):
    """
    Render buttery-smooth Sub-Pixel Keyframe Zoom frames from a high-res official still (Locked Rule L10).
    Pre-filters & grades base canvas ONCE, then applies float32 sub-pixel keyframe warp per frame!
    """
    pil_im = Image.open(img_path).convert("RGB")
    bgr0 = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)
    H0, W0 = bgr0.shape[:2]
    rx0, ry0, rx1, ry1 = crop_region
    bgr = bgr0[int(H0 * ry0):int(H0 * ry1), int(W0 * rx0):int(W0 * rx1)]

    ov_base = _prepare_static_oversampled_base(bgr, w_out, h_out, focus_cx=focus_cx, focus_cy=focus_cy, oversample=1.40)

    frames = []
    for i in range(n_frames):
        prog = i / float(max(1, n_frames - 1))
        z = float(zoom_start) + (float(zoom_end) - float(zoom_start)) * keyframe_zoom_ease(prog)
        fr = warp_subpixel_keyframe(ov_base, w_out, h_out, z)
        if w_out == W and h_out == H:
            fr = polish_frame_bright(fr, mode=bright_mode, bottom_scrim=bottom_scrim)
        else:
            fr = polish_frame_bright_any(fr, mode=bright_mode)
        frames.append(fr)
    return frames


def extract_video_segment_frames(
    video_path, t_start, n_frames, w_out=W, h_out=H,
    crop_region=(0.0, 0.0, 1.0, 1.0),
    focus_cx=0.50, focus_cy=0.50,
    zoom_start=1.00, zoom_end=1.08,
    bright_mode="broll", bottom_scrim=0.0
):
    """
    Sample exact constant-cadence 30fps frames (+1 on 30fps sources, +2 on 59.94fps DJI sources)
    and apply True Sub-Pixel Floating-Point Keyframe Zoom (Locked Rule L10 — zero stepping jitter!).
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open video: {video_path}")
    src_fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    total_src = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 999999)

    start_src_idx = max(0, int(round(t_start * src_fps)))
    cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, start_src_idx - 4))
    cur_idx = max(0, start_src_idx - 4)
    last_raw = None

    # Exact constant integer frame stride eliminates 59.94->30 or float rounding frame hiccups!
    if abs(src_fps - 30.0) < 0.15:
        fixed_stride = 1
    elif abs(src_fps - 60.0) < 0.20:
        fixed_stride = 2
    else:
        fixed_stride = None

    rx0, ry0, rx1, ry1 = crop_region
    frames = []

    for i in range(n_frames):
        if fixed_stride is not None:
            want_idx = min(total_src - 1, start_src_idx + i * fixed_stride)
        else:
            t_cur = t_start + (i / float(FPS))
            want_idx = min(total_src - 1, max(0, int(round(t_cur * src_fps))))

        while cur_idx <= want_idx:
            ok, raw = cap.read()
            if not ok:
                break
            last_raw = raw
            cur_idx += 1
        if last_raw is None:
            raise RuntimeError(f"Failed decoding frame #{i} in {video_path}")

        H0, W0 = last_raw.shape[:2]
        sub = last_raw[int(H0 * ry0):int(H0 * ry1), int(W0 * rx0):int(W0 * rx1)]
        ov_base = _prepare_static_oversampled_base(sub, w_out, h_out, focus_cx=focus_cx, focus_cy=focus_cy, oversample=1.35)

        prog = i / float(max(1, n_frames - 1))
        z = float(zoom_start) + (float(zoom_end) - float(zoom_start)) * keyframe_zoom_ease(prog)
        fr = warp_subpixel_keyframe(ov_base, w_out, h_out, z)

        if w_out == W and h_out == H:
            fr = polish_frame_bright(fr, mode=bright_mode, bottom_scrim=bottom_scrim)
        else:
            fr = polish_frame_bright_any(fr, mode=bright_mode)
        frames.append(fr)

    cap.release()
    return frames


YUNET_MODEL = r"C:\Users\NCPC\.gemini\config\skills\concept-02-lam-phat-long\scripts\models\face_detection_yunet_2023mar.onnx"
_YUNET_DET = None

def _get_yunet():
    global _YUNET_DET
    if _YUNET_DET is None:
        _YUNET_DET = cv2.FaceDetectorYN.create(YUNET_MODEL, "", (540, 960), 0.55, 0.3, 5000)
    return _YUNET_DET


def extract_aroll_reframed_frames(
    video_path, t_start, n_frames,
    raw_face_cx=0.55, raw_face_cy=0.55,
    target_face_cx=0.50, target_face_cy=0.34,
    base_crop_h=2100, zoom_end=1.08,
    bottom_scrim=0.12
):
    """
    Reframe 1728x3072 59.94fps DJI A-Roll to 1080x1920 @ 30fps with smoothed YuNet Face Tracking
    AND True Sub-Pixel Float32 Keyframe Warp (Locked Rules R12 & L10 — zero integer pan/zoom stepping!).
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open A-Roll: {video_path}")
    src_fps = cap.get(cv2.CAP_PROP_FPS) or 59.94
    total_src = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 999999)

    start_src_idx = max(0, int(round(t_start * src_fps)))
    cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, start_src_idx - 4))
    cur_idx = max(0, start_src_idx - 4)
    last_raw = None
    raw_frames = []

    fixed_stride = 2 if abs(src_fps - 60.0) < 0.20 else None

    for i in range(n_frames):
        if fixed_stride is not None:
            want_idx = min(total_src - 1, start_src_idx + i * fixed_stride)
        else:
            t_cur = t_start + (i / float(FPS))
            want_idx = min(total_src - 1, max(0, int(round(t_cur * src_fps))))
        while cur_idx <= want_idx:
            ok, raw = cap.read()
            if not ok:
                break
            last_raw = raw
            cur_idx += 1
        if last_raw is None:
            raise RuntimeError(f"Failed decoding A-Roll frame #{i} in {video_path}")
        raw_frames.append(last_raw.copy())
    cap.release()

    det = _get_yunet()
    det_idx, det_cx, det_cy = [], [], []
    for i in range(0, n_frames, 3):
        sm = cv2.resize(raw_frames[i], (540, 960), interpolation=cv2.INTER_AREA)
        _, faces = det.detect(sm)
        if faces is not None and len(faces) > 0:
            f = max(faces, key=lambda b: b[2] * b[3])
            det_idx.append(i)
            det_cx.append((f[0] + f[2] * 0.5) / 540.0)
            det_cy.append((f[1] + f[3] * 0.5) / 960.0)

    all_i = np.arange(n_frames, dtype=np.float64)
    if len(det_idx) >= 2:
        track_cx = np.interp(all_i, det_idx, det_cx)
        track_cy = np.interp(all_i, det_idx, det_cy)
        win = np.hanning(25)
        win /= win.sum()
        track_cx = np.convolve(np.pad(track_cx, (12, 12), mode="edge"), win, mode="valid")
        track_cy = np.convolve(np.pad(track_cy, (12, 12), mode="edge"), win, mode="valid")
    else:
        track_cx = np.full(n_frames, raw_face_cx, dtype=np.float64)
        track_cy = np.full(n_frames, raw_face_cy, dtype=np.float64)

    # Pre-compute floating-point window trajectories and smooth clamped centers
    H0, W0 = raw_frames[0].shape[:2]  # 3072, 1728
    # Anti-alias pre-scale factor (0.80 -> 1382x2458, ideal ~1.28x oversample for 1080x1920 INTER_CUBIC!)
    pre_s = 0.80
    Wp, Hp = int(round(W0 * pre_s)), int(round(H0 * pre_s))

    win_ws, win_hs, win_cxs, win_cys = [], [], [], []
    for i in range(n_frames):
        prog = i / float(max(1, n_frames - 1))
        z = 1.0 + (float(zoom_end) - 1.0) * keyframe_zoom_ease(prog)
        ch_f = min(float(Hp), max(1080.0 * pre_s, (float(base_crop_h) * pre_s) / z))
        cw_f = ch_f * (9.0 / 16.0)
        if cw_f > float(Wp):
            cw_f = float(Wp)
            ch_f = cw_f * (16.0 / 9.0)

        fx_px = float(track_cx[i]) * float(Wp)
        fy_px = float(track_cy[i]) * float(Hp)
        x0_f = max(0.0, min(float(Wp) - cw_f, fx_px - float(target_face_cx) * cw_f))
        y0_f = max(0.0, min(float(Hp) - ch_f, fy_px - float(target_face_cy) * ch_f))
        win_ws.append(cw_f)
        win_hs.append(ch_f)
        win_cxs.append(x0_f + 0.5 * cw_f)
        win_cys.append(y0_f + 0.5 * ch_f)

    frames = []
    for i in range(n_frames):
        pre_bgr = cv2.resize(raw_frames[i], (Wp, Hp), interpolation=cv2.INTER_AREA)
        fr = warp_subpixel_window(pre_bgr, W, H, win_cxs[i], win_cys[i], win_ws[i], win_hs[i])
        fr = polish_frame_bright(fr, mode="aroll", bottom_scrim=bottom_scrim)
        frames.append(fr)

    return frames


def compose_split_50_50(top_frames, bot_frames, divider_px=4):
    """Stack two (1080x960) frame lists into Hung's crisp 50/50 split screen."""
    n = min(len(top_frames), len(bot_frames))
    out = []
    for i in range(n):
        fr = np.vstack([top_frames[i], bot_frames[i]])
        if divider_px > 0:
            y_mid = H // 2
            cv2.line(fr, (0, y_mid), (W, y_mid), (245, 248, 250), divider_px)
        out.append(fr)
    return out


def compose_split_3tier(top_frames, mid_frames, bot_frames, divider_px=4):
    """Stack three (1080x640) frame lists into Hung's 1/3-1/3-1/3 3-tier aerial/ecosystem split."""
    n = min(len(top_frames), len(mid_frames), len(bot_frames))
    out = []
    for i in range(n):
        fr = np.vstack([top_frames[i], mid_frames[i], bot_frames[i]])
        if divider_px > 0:
            cv2.line(fr, (0, 640), (W, 640), (245, 248, 250), divider_px)
            cv2.line(fr, (0, 1280), (W, 1280), (245, 248, 250), divider_px)
        out.append(fr)
    return out


# ==============================================================================
# PHOTOREALISTIC ARCHITECTURAL CONTRACT SHOWCASE BUILDER (P4 & P6B)
# ==============================================================================
_CONTRACT_BASE_CACHE = {}

def _build_contract_master_canvas(mode="p4_ident"):
    """
    Build a high-res (1400x2488) sunlit architectural desk + ivory luxury contract document
    so we can push-in smoothly via float32 sub-pixel keyframe warp and illuminate clauses per frame.
    """
    CW, CH = 1400, 2488
    if mode in _CONTRACT_BASE_CACHE:
        return _CONTRACT_BASE_CACHE[mode].copy()

    yy, xx = np.mgrid[0:CH, 0:CW].astype(np.float32)
    beam = np.exp(-(((xx - CW * 0.35 + (yy - CH * 0.42) * 0.45) / (CW * 0.48)) ** 2))
    r = np.clip(62.0 + 38.0 * beam - 18.0 * ((yy / CH - 0.5) ** 2), 0, 255)
    g = np.clip(54.0 + 34.0 * beam - 16.0 * ((yy / CH - 0.5) ** 2), 0, 255)
    b = np.clip(46.0 + 26.0 * beam - 14.0 * ((yy / CH - 0.5) ** 2), 0, 255)
    bg = np.stack([r, g, b], axis=-1).astype(np.uint8)
    im = Image.fromarray(bg, mode="RGB").convert("RGBA")

    if mode == "p4_ident":
        dx0, dy0, dx1, dy1 = 105, 290, CW - 105, CH - 340
    else:
        CH = 1244
        im = im.crop((0, 0, CW, CH))
        dx0, dy0, dx1, dy1 = 90, 85, CW - 90, CH - 85

    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([dx0 + 14, dy0 + 22, dx1 + 14, dy1 + 22], radius=16, fill=(0, 0, 0, 145))
    sh = sh.filter(ImageFilter.GaussianBlur(22))
    im = Image.alpha_composite(im, sh)

    dr = ImageDraw.Draw(im)
    dr.rounded_rectangle([dx0, dy0, dx1, dy1], radius=12, fill=(252, 250, 244, 255), outline=(198, 162, 92, 255), width=4)
    dr.rounded_rectangle([dx0 + 18, dy0 + 18, dx1 - 18, dy1 - 18], radius=8, outline=(216, 188, 130, 180), width=2)

    f_crest = get_font(FONT_SANS_BOLD, 22)
    f_title = get_font(FONT_COND_BLACK, 48 if mode == "p4_ident" else 42)
    f_sub   = get_font(FONT_ITALIC_SER, 26 if mode == "p4_ident" else 23)
    f_sec   = get_font(FONT_SANS_BOLD, 27 if mode == "p4_ident" else 24)
    f_body  = get_font(FONT_SANS_REG, 24 if mode == "p4_ident" else 22)

    cx = CW // 2
    y_cur = dy0 + (62 if mode == "p4_ident" else 42)

    crest_txt = "PARKCITY HANOI  -  LE PARC PLACE"
    b_cr = f_crest.getbbox(crest_txt)
    dr.text((cx - (b_cr[2] - b_cr[0]) // 2, y_cur), crest_txt, font=f_crest, fill=(162, 124, 52, 255))
    y_cur += 40
    dr.line([(cx - 190, y_cur), (cx + 190, y_cur)], fill=(198, 162, 92, 220), width=2)
    y_cur += 24

    t1 = "HỢP ĐỒNG MUA BÁN CHỖ ĐỂ XE Ô TÔ"
    b_t1 = f_title.getbbox(t1)
    dr.text((cx - (b_t1[2] - b_t1[0]) // 2, y_cur), t1, font=f_title, fill=(24, 42, 68, 255))
    y_cur += (64 if mode == "p4_ident" else 52)

    t2 = "(Văn bản pháp lý độc lập đính kèm Căn hộ định danh tại Dự án Le Parc Place)"
    b_t2 = f_sub.getbbox(t2)
    dr.text((cx - (b_t2[2] - b_t2[0]) // 2, y_cur), t2, font=f_sub, fill=(92, 102, 118, 255))
    y_cur += (54 if mode == "p4_ident" else 42)

    dr.line([(dx0 + 55, y_cur), (dx1 - 55, y_cur)], fill=(210, 204, 190, 255), width=2)

    if mode == "p4_ident":
        y_cur += 36
        dr.text((dx0 + 65, y_cur), "ĐIỀU 1. THÔNG TIN XÁC ĐỊNH CHỖ ĐỖ XE Ô TÔ ĐỊNH DANH", font=f_sec, fill=(24, 42, 68, 255))
        y_cur += 46
        intro = (
            "Bên Bán và Bên Mua thống nhất xác lập quyền sở hữu và sử dụng chỗ đỗ xe ô tô\n"
            "định danh gắn liền với căn hộ theo thông số kỹ thuật cố định dưới đây:"
        )
        dr.multiline_text((dx0 + 65, y_cur), intro, font=f_body, fill=(68, 76, 88, 255), spacing=12)

        y_foot = 1580
        dr.line([(dx0 + 65, y_foot), (dx1 - 65, y_foot)], fill=(210, 204, 190, 255), width=2)
        note = (
            "ĐIỀU 2. CAM KẾT BÀN GIAO & SỬ DỤNG LÂU DÀI\n"
            "- Chỗ đỗ xe ô tô định danh được đánh số riêng trên thực địa tại Tầng 1 - Tầng 4 khối đế nổi.\n"
            "- Đảm bảo tối thiểu 01 chỗ đỗ ô tô cố định cho mỗi căn hộ, thông gió & ánh sáng tự nhiên.\n"
            "- Minh bạch toàn bộ vị trí, thời hạn, chi phí và điều kiện vận hành ngay khi ký Hợp đồng."
        )
        dr.multiline_text((dx0 + 65, y_foot + 30), note, font=f_body, fill=(68, 76, 88, 255), spacing=16)

        bx, by = dx1 - 235, dy1 - 165
        dr.ellipse([bx - 78, by - 78, bx + 78, by + 78], outline=(188, 52, 48, 155), width=4)
        dr.ellipse([bx - 66, by - 66, bx + 66, by + 66], outline=(188, 52, 48, 120), width=2)
        f_st = get_font(FONT_COND_BOLD, 22)
        b_s = f_st.getbbox("MẪU ĐỐI CHIẾU")
        dr.text((bx - (b_s[2] - b_s[0]) // 2, by - 14), "MẪU ĐỐI CHIẾU", font=f_st, fill=(188, 52, 48, 165))

    _CONTRACT_BASE_CACHE[mode] = im
    return im.copy()


def build_contract_p4_frames(n_frames, t_row1=4.54, t_row2=5.10, t_row3=5.88):
    """
    Scene 4 (VOICE CẢNH 4): Full 9:16 Contract Showcase with Sub-Pixel Keyframe Push-in (L10)
    onto the 3 rows ('căn hộ', 'tầng để xe', 'số lốt') illuminating synchronously with spoken words!
    """
    base_master = _build_contract_master_canvas("p4_ident")
    CW, CH = base_master.size
    dx0, dx1 = 165, CW - 165

    rows = [
        ("01. MÃ CĂN HỘ THAM CHIẾU", "Căn hộ B1 - 18.06  (Tòa B1 - Le Parc Place)", t_row1),
        ("02. TẦNG ĐỂ XE Ô TÔ NỔI", "Tầng 02 - Khối đế đỗ xe nổi (Tầng 1 - Tầng 4)", t_row2),
        ("03. SỐ LỐT ĐỖ ĐỊNH DANH", "Lốt đỗ số  P2 - A088  (Cố định trọn đời theo căn)", t_row3),
    ]
    f_lbl = get_font(FONT_SANS_BOLD, 25)
    f_tag = get_font(FONT_COND_BOLD, 23)

    frames = []
    for i in range(n_frames):
        t = i / float(FPS)
        canvas = base_master.copy()
        dr = ImageDraw.Draw(canvas)

        for r_idx, (lbl, val, t_trig) in enumerate(rows):
            ry0 = 885 + r_idx * 210
            ry1 = ry0 + 178
            raw_p = (t - t_trig) / 0.48 if t >= t_trig else 0.0
            active = ease_in_out_cubic(raw_p)

            if active > 0.01:
                fill_col = (
                    int(248 + 7 * active),
                    int(246 + 4 * active),
                    int(238 - 42 * active),
                    255
                )
                border_col = (18, 148, 212, int(255 * active)) if r_idx < 2 else (228, 148, 16, int(255 * active))
                dr.rounded_rectangle([dx0, ry0, dx1, ry1], radius=14, fill=fill_col, outline=border_col, width=5)
                dr.rounded_rectangle([dx0, ry0, dx0 + 16, ry1], radius=6, fill=border_col)
                px0, py0, px1, py1 = dx1 - 226, ry0 + 22, dx1 - 28, ry0 + 68
                dr.rounded_rectangle([px0, py0, px1, py1], radius=23, fill=border_col)
                bt = f_tag.getbbox("ĐỊNH DANH")
                tw_t, th_t = bt[2] - bt[0], bt[3] - bt[1]
                tx_t = px0 + (px1 - px0 - 30 - tw_t) // 2 - bt[0]
                ty_t = py0 + (py1 - py0 - th_t) // 2 - bt[1]
                dr.text((tx_t, ty_t), "ĐỊNH DANH", font=f_tag, fill=(255, 255, 255, 255))
                cx_k, cy_k = px1 - 28, (py0 + py1) // 2
                dr.line([(cx_k - 8, cy_k), (cx_k - 2, cy_k + 7), (cx_k + 9, cy_k - 7)], fill=(255, 255, 255, 255), width=3)
            else:
                dr.rounded_rectangle([dx0, ry0, dx1, ry1], radius=14, fill=(246, 244, 238, 255), outline=(212, 206, 192, 255), width=2)
                dr.rounded_rectangle([dx0, ry0, dx0 + 10, ry1], radius=4, fill=(198, 162, 92, 255))

            f_val_fit, _ = fit_font(FONT_COND_BLACK, val, 38, (dx1 - dx0) - 88)
            bl = f_lbl.getbbox(lbl)
            bv = f_val_fit.getbbox(val)
            hl, hv = bl[3] - bl[1], bv[3] - bv[1]
            gap_rv = 20
            tot_rv = hl + gap_rv + hv
            y_l = ry0 + (178 - tot_rv) // 2 - bl[1]
            y_v = ry0 + (178 - tot_rv) // 2 + hl + gap_rv - bv[1]
            dr.text((dx0 + 42, y_l), lbl, font=f_lbl, fill=(112, 92, 48, 255) if active < 0.5 else (14, 96, 152, 255))
            val_col = (24, 38, 58, 255) if active < 0.5 else ((12, 72, 132, 255) if r_idx < 2 else (196, 98, 8, 255))
            dr.text((dx0 + 42, y_v), val, font=f_val_fit, fill=val_col)

        bgr_full = cv2.cvtColor(np.array(canvas.convert("RGB")), cv2.COLOR_RGB2BGR)
        prog = i / float(max(1, n_frames - 1))
        kp = keyframe_zoom_ease(prog)
        z = 1.00 + 0.12 * kp
        cw_f = float(CW) / z
        ch_f = min(float(CH), cw_f * (16.0 / 9.0))
        cw_f = ch_f * (9.0 / 16.0)
        cy_focus = float(CH) * (0.47 + 0.04 * kp)
        cy_clamped = max(0.5 * ch_f, min(float(CH) - 0.5 * ch_f, cy_focus))

        fr = warp_subpixel_window(bgr_full, W, H, 0.5 * float(CW), cy_clamped, cw_f, ch_f)
        fr = polish_frame_bright(fr, mode="broll", bottom_scrim=0.22)
        frames.append(fr)

    return frames


def build_contract_p6_top_frames(n_frames, rel_triggers=(2.15, 2.95, 3.55, 4.35)):
    """
    Scene 6B Top 50% (1080x960): 4 Contract Clauses illuminating 1-by-1 with Sub-Pixel Keyframe Zoom (L10).
    """
    base_master = _build_contract_master_canvas("p6_clauses")
    CW, CH = base_master.size  # 1400 x 1244
    dx0, dx1 = 140, CW - 140

    clauses = [
        ("01. VỊ TRÍ CHỖ ĐỖ", "Xác định rõ tầng đỗ nổi (T1 - T4) & mã số lốt trên sơ đồ", rel_triggers[0]),
        ("02. THỜI HẠN SỬ DỤNG", "Quyền sử dụng lâu dài đồng bộ theo thời hạn Căn hộ", rel_triggers[1]),
        ("03. CHI PHÍ MINH BẠCH", "Quy định rõ ưu đãi tặng lốt đỗ & biểu phí quản lý vận hành", rel_triggers[2]),
        ("04. ĐIỀU KIỆN SỬ DỤNG", "Cam kết bàn giao, thẻ định danh riêng & nội quy an toàn", rel_triggers[3]),
    ]
    f_c1 = get_font(FONT_COND_BLACK, 31)

    frames = []
    for i in range(n_frames):
        t = i / float(FPS)
        canvas = base_master.copy()
        dr = ImageDraw.Draw(canvas)

        for idx, (c_title, c_desc, trig) in enumerate(clauses):
            ry0 = 335 + idx * 188
            ry1 = ry0 + 162
            act = ease_in_out_cubic((t - trig) / 0.45) if t >= trig else 0.0
            if act > 0.01:
                dr.rounded_rectangle([dx0, ry0, dx1, ry1], radius=12, fill=(255, 249, 226, 255), outline=(224, 152, 22, 255), width=4)
                dr.rounded_rectangle([dx0, ry0, dx0 + 14, ry1], radius=6, fill=(224, 152, 22, 255))
            else:
                dr.rounded_rectangle([dx0, ry0, dx1, ry1], radius=12, fill=(246, 244, 238, 255), outline=(212, 206, 192, 255), width=2)
                dr.rounded_rectangle([dx0, ry0, dx0 + 8, ry1], radius=4, fill=(198, 162, 92, 255))

            f_c2_fit, _ = fit_font(FONT_SANS_REG, c_desc, 22, (dx1 - dx0) - 80)
            bc1 = f_c1.getbbox(c_title)
            bc2 = f_c2_fit.getbbox(c_desc)
            hc1, hc2 = bc1[3] - bc1[1], bc2[3] - bc2[1]
            gap_c = 18
            tot_c = hc1 + gap_c + hc2
            yc1 = ry0 + (162 - tot_c) // 2 - bc1[1]
            yc2 = ry0 + (162 - tot_c) // 2 + hc1 + gap_c - bc2[1]
            dr.text((dx0 + 38, yc1), c_title, font=f_c1, fill=(196, 102, 8, 255) if act > 0.5 else (24, 42, 68, 255))
            dr.text((dx0 + 38, yc2), c_desc, font=f_c2_fit, fill=(52, 60, 72, 255))

        bgr_full = cv2.cvtColor(np.array(canvas.convert("RGB")), cv2.COLOR_RGB2BGR)
        prog = i / float(max(1, n_frames - 1))
        z = 1.00 + 0.08 * keyframe_zoom_ease(prog)
        cw_f = float(CW) / z
        ch_f = min(float(CH), cw_f * (960.0 / 1080.0))
        cw_f = ch_f * (1080.0 / 960.0)
        cy_clamped = max(0.5 * ch_f, min(float(CH) - 0.5 * ch_f, float(CH) * 0.52))

        fr = warp_subpixel_window(bgr_full, W, 960, 0.5 * float(CW), cy_clamped, cw_f, ch_f)
        frames.append(fr)

    return frames
