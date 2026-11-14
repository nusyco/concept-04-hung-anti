import os
import math
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30

# ==============================================================================
# LOCKED FONT SUITE MATCHING HUNG-LE-PARC-PLACE 4K REFERENCE 1:1 (L1, L19, L22)
# ==============================================================================
_HERE    = os.path.dirname(os.path.abspath(__file__))
F_ASSETS = os.path.normpath(os.path.join(_HERE, "..", "assets", "fonts"))
F_LOCAL  = os.path.join(_HERE, "fonts")
F_USER   = os.path.join(os.environ.get("LOCALAPPDATA", r"C:\Users\NCPC\AppData\Local"), "Microsoft", "Windows", "Fonts")
F_WIN    = r"C:\Windows\Fonts"

def _resolve_font(filename, fallback_dir=F_USER):
    for d in (F_LOCAL, F_ASSETS, F_USER, F_WIN):
        cand = os.path.join(d, filename)
        if os.path.exists(cand):
            return cand
    return os.path.join(fallback_dir, filename)

FONT_BEBAS      = _resolve_font("UTM Bebas.ttf")
FONT_ANTON      = _resolve_font("Anton-Regular.ttf")
FONT_SCRIPT     = _resolve_font("Smooch-Regular.ttf")                     # Brush Script (`Căn hộ`, `Dự án`, `Trong`, `Hợp đồng`)
FONT_GREATVIBES = _resolve_font("GreatVibes-Regular.ttf")                 # Silky Flowing Calligraphy in Box (`Đối chiếu`, `Căn`, `Vị trí` — L22!)
FONT_ARIZONIA   = _resolve_font("Arizonia-Regular.ttf")                   # Soft Ribbon Calligraphy
FONT_ALLISON    = _resolve_font("Allison-Regular.ttf")
FONT_APTIMA_IT  = _resolve_font("UTM AptimaItalic.ttf")                   # Slender Humanist Italic (`Khi mua`, `hơn`, B-Roll captions)
FONT_APTIMA_BI  = _resolve_font("UTM AptimaBoldItalic.ttf")               # Medium-Bold Flared Italic (`( Diện tích : 107m2 )` in Olive Box!)
FONT_APTIMA_REG = _resolve_font("UTM Aptima.ttf")                         # Upright Humanist Sans (`Nhìn rõ tên văn bản`, `Khi chọn căn, cùng xem rõ` — NEVER use U+2014 em-dash!)
FONT_TRAJAN     = _resolve_font("UTM Trajan Pro Bold.ttf")                # Classical Wide Roman Display Serif (`CHỖ ĐỖ XE`, `TỪ TẦNG 1 ĐẾN TẦNG 4`)
FONT_TAG_IT     = _resolve_font("Montserrat-ExtraBoldItalic.otf")         # Pill Category Tag (`ĐIỂM KHÁC BIỆT`, `THỨ NHẤT`)
FONT_BOLD_SER   = _resolve_font("palab.ttf", F_WIN)
FONT_SANS_BOLD  = _resolve_font("GoogleSans-Bold.ttf")
FONT_SANS_REG   = _resolve_font("GoogleSans-Regular.ttf")
FONT_COND_BLACK = FONT_BEBAS
FONT_COND_BOLD  = FONT_BEBAS
FONT_ITALIC_SER = FONT_APTIMA_IT

_FONT_CACHE = {}
def get_font(path, size):
    key = (path, int(size))
    if key not in _FONT_CACHE:
        _FONT_CACHE[key] = ImageFont.truetype(path, int(size))
    return _FONT_CACHE[key]

def fit_font(path, text, max_size, max_width, min_size=20):
    sz = int(max_size)
    while sz > min_size:
        f = get_font(path, sz)
        bb = f.getbbox(text)
        if (bb[2] - bb[0]) <= max_width:
            return f, sz
        sz -= 2
    return get_font(path, min_size), min_size

def match_font_size_to_width(path, text, target_ink_w, min_size=24, max_size=260):
    """Find exact font size whose true glyph ink width matches target_ink_w."""
    best_sz = min_size
    best_diff = 999999
    for sz in range(min_size, max_size + 1, 1):
        f = get_font(path, sz)
        bb = f.getbbox(text)
        cw = max(8, (bb[2] - bb[0]) + 16)
        ch = max(8, (bb[3] - bb[1]) + 16)
        m = Image.new("L", (cw, ch), 0)
        ImageDraw.Draw(m).text((8 - bb[0], 8 - bb[1]), text, font=f, fill=255)
        xs = np.where(np.array(m) > 32)[1]
        w = (int(xs.max()) - int(xs.min()) + 1) if len(xs) > 0 else (bb[2] - bb[0])
        diff = abs(w - target_ink_w)
        if diff < best_diff:
            best_diff = diff
            best_sz = sz
        if w > target_ink_w and diff > best_diff:
            break
    return best_sz

def match_font_size_to_height(path, text, target_ink_h, min_size=36, max_size=280):
    """Find exact font size whose true pixel ink height matches target_ink_h."""
    best_sz = min_size
    best_diff = 999999
    for sz in range(min_size, max_size + 1, 1):
        f = get_font(path, sz)
        bb = f.getbbox(text)
        cw = max(8, (bb[2] - bb[0]) + 16)
        ch = max(8, (bb[3] - bb[1]) + 16)
        m = Image.new("L", (cw, ch), 0)
        ImageDraw.Draw(m).text((8 - bb[0], 8 - bb[1]), text, font=f, fill=255)
        ys = np.where(np.array(m) > 32)[0]
        h = (int(ys.max()) - int(ys.min()) + 1) if len(ys) > 0 else (bb[3] - bb[1])
        diff = abs(h - target_ink_h)
        if diff < best_diff:
            best_diff = diff
            best_sz = sz
        if h > target_ink_h and diff > best_diff:
            break
    return best_sz


# ==============================================================================
# 0. CINEMA MOTION & EASE-IN / LATE EASE-OUT INTERPOLATORS (L5, L14, L15)
# ==============================================================================
def ease_in_out_cubic(t):
    """True C1-continuous Ease-In-Out: zero start velocity, smooth mid acceleration, zero landing velocity."""
    t = max(0.0, min(1.0, float(t)))
    return 4.0 * t * t * t if t < 0.5 else 1.0 - ((-2.0 * t + 2.0) ** 3) * 0.5

def ease_in_out_quart(t):
    t = max(0.0, min(1.0, float(t)))
    return 8.0 * (t ** 4) if t < 0.5 else 1.0 - ((-2.0 * t + 2.0) ** 4) * 0.5

def ease_in_out_sine(t):
    t = max(0.0, min(1.0, float(t)))
    return 0.5 * (1.0 - math.cos(math.pi * t))

def ease_in_out_scale(local_age_f, dur_f=18, start_scale=0.89, peak_scale=1.028):
    """Smooth 2-phase Ease-In-Out scale with gentle luxury cushion."""
    if local_age_f < 0:
        return 0.0
    if local_age_f >= dur_f:
        return 1.0
    t = (local_age_f + 1) / float(dur_f)
    split = 0.72
    if t <= split:
        p = ease_in_out_cubic(t / split)
        return start_scale + (peak_scale - start_scale) * p
    else:
        p = ease_in_out_sine((t - split) / (1.0 - split))
        return peak_scale + (1.0 - peak_scale) * p

def tier_motion(age_f, rem_f, delay_f=0, in_f=18, out_f=6, rise_px=18.0, start_scale=0.92, peak_scale=1.022):
    local_age = age_f - delay_f
    if local_age < 0:
        return 0.0, 0.0, float(rise_px)
    if local_age < in_f:
        p_in = ease_in_out_cubic((local_age + 1) / float(in_f))
        op_in = p_in
        dy_in = float(rise_px) * (1.0 - p_in)
        sc_in = ease_in_out_scale(local_age, dur_f=in_f, start_scale=start_scale, peak_scale=peak_scale)
    else:
        op_in, dy_in, sc_in = 1.0, 0.0, 1.0

    if rem_f < out_f:
        p_out = ease_in_out_cubic(max(0.0, float(rem_f)) / float(max(1, out_f)))
        op = op_in * p_out
        dy = dy_in - 6.0 * (1.0 - p_out)
        sc = sc_in * (0.97 + 0.03 * p_out)
    else:
        op, dy, sc = op_in, dy_in, sc_in
    return op, sc, dy


# ==============================================================================
# 1. COLOR GRADING — HIGH-KEY BRIGHT FRESH LUXURY + SOFT LOCAL TEXT SCRIM
# ==============================================================================
def build_bright_lut_table(exposure_gain=1.14, gamma=0.88):
    x = np.arange(256, dtype=np.float32) / 255.0
    y = np.power(np.clip(x * exposure_gain, 0.0, 1.0), gamma)
    y = y * (1.0 - 0.08 * (y ** 3)) + 0.08 * y
    return np.clip(y * 255.0, 0, 255).astype(np.uint8)

_LUT_AR = build_bright_lut_table(1.16, 0.86)
_LUT_BR = build_bright_lut_table(1.07, 0.93)

def polish_frame_bright(bgr, mode="aroll", bottom_scrim=0.0):
    lut = _LUT_AR if mode == "aroll" else _LUT_BR
    out = cv2.LUT(bgr, lut).astype(np.float32)
    if mode == "aroll":
        out[:, :, 2] *= 1.035
        out[:, :, 1] *= 1.010
        out[:, :, 0] *= 0.975
    else:
        out[:, :, 2] *= 1.020
        out[:, :, 0] *= 0.990
    out = np.clip(out, 0, 255).astype(np.uint8)

    hsv = cv2.cvtColor(out, cv2.COLOR_BGR2HSV).astype(np.float32)
    sat_gain = 1.14 if mode == "aroll" else 1.10
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] * sat_gain, 0, 255)
    out = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

    if bottom_scrim > 0.001:
        y0 = int(H * (0.56 if bottom_scrim >= 0.45 else 0.66))
        t = np.linspace(0.0, 1.0, H - y0, dtype=np.float32)[:, None, None]
        alpha = bottom_scrim * (0.5 - 0.5 * np.cos(np.pi * t))
        out_f = out[y0:, :, :].astype(np.float32)
        out[y0:, :, :] = np.clip(out_f * (1.0 - alpha), 0, 255).astype(np.uint8)
    return out

def apply_soft_spot_scrim(bgr, cx, cy, rx=340, ry=185, strength=0.34):
    if strength <= 0.01:
        return bgr
    x0, x1 = max(0, int(cx - rx * 1.5)), min(W, int(cx + rx * 1.5))
    y0, y1 = max(0, int(cy - ry * 1.5)), min(H, int(cy + ry * 1.5))
    if x1 <= x0 or y1 <= y0:
        return bgr
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
    d2 = ((xx - cx) / float(rx)) ** 2 + ((yy - cy) / float(ry)) ** 2
    falloff = (strength * np.exp(-1.35 * d2))[:, :, None]
    roi = bgr[y0:y1, x0:x1].astype(np.float32)
    bgr[y0:y1, x0:x1] = np.clip(roi * (1.0 - falloff), 0, 255).astype(np.uint8)
    return bgr


# ==============================================================================
# 2. CLEAN FLAT-FACE LUXURY 2D TYPOGRAPHY ENGINE (L1–L3, L17, L18)
#    (extrude_3d_px = 0 on all 2D screen text so gradients & diacritics match Hung 1:1!)
# ==============================================================================
GOLD_METALLIC  = [(0.0, (255, 248, 138)), (0.48, (252, 202, 22)), (0.88, (230, 152, 8)), (1.0, (248, 198, 46))]
PILL_GOLD      = [(0.0, (255, 244, 136)), (0.55, (250, 196, 22)), (1.0, (232, 148, 10))]
CREAM_TO_GOLD  = [(0.0, (255, 252, 196)), (0.52, (252, 206, 42)), (1.0, (236, 162, 12))]
SUNSET_GOLD    = [(0.0, (255, 244, 142)), (0.48, (254, 192, 18)), (0.90, (238, 136, 8)), (1.0, (252, 204, 54))]
OCEAN_SKY_BLUE = [(0.0, (124, 214, 255)), (0.45, (28, 148, 242)), (0.92, (8, 96, 198)), (1.0, (22, 126, 224))]
CHAMPAGNE      = [(0.0, (255, 246, 194)), (0.55, (238, 202, 114)), (1.0, (212, 170, 82))]
CREAM_IVORY    = [(0.0, (255, 255, 255)), (1.0, (246, 243, 236))]
PURE_WHITE     = [(0.0, (255, 255, 255)), (1.0, (248, 250, 253))]
ARCH_WHITE_3D  = [(0.0, (255, 255, 255)), (0.72, (252, 252, 252)), (1.0, (244, 243, 241))]
ICE_CYAN       = [(0.0, (242, 254, 255)), (0.55, (164, 242, 255)), (1.0, (92, 226, 248))]
SCRIPT_CREAM   = [(0.0, (255, 254, 236)), (0.60, (255, 236, 168)), (1.0, (246, 206, 98))]


class RichSprite:
    """RGBA PIL sprite carrying exact glyph ink bounds PLUS diacritic-immune cap-body bounds (cap_y0..cap_y1)."""
    def __init__(self, im, ink_x0, ink_y0, ink_x1, ink_y1, cap_y0=None, cap_y1=None):
        self.im = im
        self.arr = np.array(im)
        self.width, self.height = im.size
        self.ink_x0 = float(ink_x0)
        self.ink_y0 = float(ink_y0)
        self.ink_x1 = float(ink_x1)
        self.ink_y1 = float(ink_y1)
        self.ink_w = max(1.0, self.ink_x1 - self.ink_x0)
        self.ink_h = max(1.0, self.ink_y1 - self.ink_y0)
        self.ink_cx = 0.5 * (self.ink_x0 + self.ink_x1)
        self.ink_cy = 0.5 * (self.ink_y0 + self.ink_y1)
        self.cap_y0 = float(ink_y0 if cap_y0 is None else cap_y0)
        self.cap_y1 = float(ink_y1 if cap_y1 is None else cap_y1)
        self.cap_h  = max(1.0, self.cap_y1 - self.cap_y0)
        self.cap_cy = 0.5 * (self.cap_y0 + self.cap_y1)
        self._blur_arr = None

    def get_blurred_arr(self):
        if self._blur_arr is None:
            self._blur_arr = cv2.GaussianBlur(self.arr, (13, 13), 4.4)
        return self._blur_arr


def make_gradient_rgb(w, h, stops, sparkle=False):
    arr = np.zeros((h, w, 3), dtype=np.float32)
    ys = np.linspace(0.0, 1.0, max(1, h))
    xp = [s[0] for s in stops]
    for c in range(3):
        fp = [s[1][c] for s in stops]
        arr[:, :, c] = np.interp(ys, xp, fp)[:, None]

    if sparkle:
        rng = np.random.RandomState(42)
        noise = rng.normal(0.0, 1.0, (max(2, h // 2), max(2, w // 2))).astype(np.float32)
        noise = cv2.resize(noise, (w, h), interpolation=cv2.INTER_CUBIC)
        sparkles = np.clip((noise - 0.82) * 26.0, -8.0, 32.0)
        arr[:, :, 0] = np.clip(arr[:, :, 0] + sparkles, 0, 255)
        arr[:, :, 1] = np.clip(arr[:, :, 1] + sparkles * 0.85, 0, 255)
        arr[:, :, 2] = np.clip(arr[:, :, 2] + sparkles * 0.40, 0, 255)

    return Image.fromarray(arr.astype(np.uint8), mode="RGB")


_SPRITE_CACHE = {}

def render_rich_sprite(
    text, font_path, font_size, grad_stops=PURE_WHITE,
    shadow_offset=(3, 4), shadow_blur=4, shadow_alpha=195,
    glow_color=None, glow_blur=11, glow_alpha=150,
    glow2_color=None, glow2_blur=4, glow2_alpha=0,
    bevel_3d=False, bevel_color=(255, 253, 232, 160),
    sparkle=False, tilt_deg=0.0, condense_x=1.0, stroke_boost=0, shear_x=0.0
):
    """
    Clean Flat-Face Reference 2D Typography Renderer (Locked Rules L3, L17, L18, L20, L21):
    0px thick outline, 0px dark WordArt extrusion — pure luminous metallic/cyan/ocean gradients
    + crisp directional drop shadow + soft ambient glow + diacritic-immune cap-body metrics!
    """
    cache_key = (
        text, font_path, int(font_size), tuple((s[0], tuple(s[1])) for s in grad_stops),
        shadow_offset, shadow_blur, shadow_alpha,
        glow_color, glow_blur, glow_alpha,
        glow2_color, glow2_blur, glow2_alpha,
        bevel_3d, bevel_color, sparkle, round(float(tilt_deg), 2), round(float(condense_x), 3),
        int(stroke_boost), round(float(shear_x), 3)
    )
    if cache_key in _SPRITE_CACHE:
        return _SPRITE_CACHE[cache_key]

    sb = max(0, int(stroke_boost))
    if abs(float(shear_x)) > 0.005:
        f2 = get_font(font_path, int(font_size) * 2)
        bb2 = f2.getbbox(text, stroke_width=sb * 2)
        tw2 = max(2, bb2[2] - bb2[0])
        th2 = max(2, bb2[3] - bb2[1])
        pad2 = max(72, max(shadow_blur, glow_blur) * 4 + 56)
        cw2, ch2 = tw2 + pad2 * 2, th2 + pad2 * 2
        ox2, oy2 = pad2 - bb2[0], pad2 - bb2[1]
        m2 = Image.new("L", (cw2, ch2), 0)
        ImageDraw.Draw(m2).text((ox2, oy2), text, font=f2, fill=255, stroke_width=sb * 2)
        sh_abs = abs(float(shear_x))
        extra_w2 = int(sh_abs * ch2) + 32
        M_sh = np.float32([[1.0, float(shear_x), (sh_abs * ch2 if shear_x < 0 else 0.0)], [0.0, 1.0, 0.0]])
        arr_sh = cv2.warpAffine(np.array(m2), M_sh, (cw2 + extra_w2, ch2), flags=cv2.INTER_CUBIC)
        cw, ch = max(8, arr_sh.shape[1] // 2), max(8, arr_sh.shape[0] // 2)
        glyph_mask = Image.fromarray(arr_sh).resize((cw, ch), Image.Resampling.LANCZOS)

        cm2 = Image.new("L", (max(240, int(font_size) * 4), ch2), 0)
        ImageDraw.Draw(cm2).text((40, oy2), "x", font=f2, fill=255)
        c_ys = np.where(np.array(cm2) > 32)[0]
        raw_cap_y0 = int(c_ys.min() // 2) if len(c_ys) > 0 else (pad2 // 2)
        raw_cap_y1 = int((c_ys.max() + 1) // 2) if len(c_ys) > 0 else ((pad2 + th2) // 2)
        pad, th = pad2 // 2, th2 // 2
    else:
        f = get_font(font_path, font_size)
        bb = f.getbbox(text, stroke_width=sb)
        tw = max(1, bb[2] - bb[0])
        th = max(1, bb[3] - bb[1])
        pad = max(36, max(shadow_blur, glow_blur) * 2 + 24)
        cw, ch = tw + pad * 2, th + pad * 2
        ox, oy = pad - bb[0], pad - bb[1]

        glyph_mask = Image.new("L", (cw, ch), 0)
        ImageDraw.Draw(glyph_mask).text((ox, oy), text, font=f, fill=255, stroke_width=sb)

        cap_probe = "HX" if any(ch_c.isupper() or ch_c.isdigit() for ch_c in text) else "x"
        cap_m = Image.new("L", ( max(120, int(font_size) * 3), ch), 0)
        ImageDraw.Draw(cap_m).text((20, oy), cap_probe, font=f, fill=255)
        c_ys = np.where(np.array(cap_m) > 32)[0]
        raw_cap_y0 = int(c_ys.min()) if len(c_ys) > 0 else pad
        raw_cap_y1 = (int(c_ys.max()) + 1) if len(c_ys) > 0 else (pad + th)

    if abs(float(condense_x) - 1.0) > 0.008:
        nw_c = max(16, int(round(cw * float(condense_x))))
        glyph_mask = glyph_mask.resize((nw_c, ch), Image.Resampling.BICUBIC)
        cw = nw_c

    gm_np = np.array(glyph_mask)
    g_ys, g_xs = np.where(gm_np > 32)
    if len(g_ys) > 0:
        gy0, gy1 = int(g_ys.min()), int(g_ys.max()) + 1
    else:
        gy0, gy1 = pad, pad + th

    # Map gradient across core cap height (or full ink height when no accents) so accents don't dull the top highlight!
    grad_y0 = min(gy0, raw_cap_y0)
    grad_y1 = max(gy1, raw_cap_y1)
    grad_rgb = make_gradient_rgb(cw, max(1, grad_y1 - grad_y0), grad_stops, sparkle=sparkle)
    full_rgb = Image.new("RGB", (cw, ch), grad_stops[-1][1])
    full_rgb.paste(grad_rgb, (0, grad_y0))
    fill_layer = full_rgb.convert("RGBA")
    fill_layer.putalpha(glyph_mask)

    if abs(tilt_deg) > 0.1:
        glyph_mask = glyph_mask.rotate(tilt_deg, resample=Image.Resampling.BICUBIC, expand=True)
        fill_layer = fill_layer.rotate(tilt_deg, resample=Image.Resampling.BICUBIC, expand=True)
        cw, ch = glyph_mask.size

    gm_np = np.array(glyph_mask)
    g_ys, g_xs = np.where(gm_np > 32)
    if len(g_ys) > 0:
        gy0, gy1 = int(g_ys.min()), int(g_ys.max()) + 1
        gx0, gx1 = int(g_xs.min()), int(g_xs.max()) + 1
    else:
        gy0, gy1, gx0, gx1 = 0, ch, 0, cw
    if abs(tilt_deg) > 0.1:
        raw_cap_y0, raw_cap_y1 = gy0, gy1

    canvas = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))

    # 1. Clean Directional Drop Shadow
    if shadow_alpha > 0:
        sh_m = glyph_mask.filter(ImageFilter.GaussianBlur(shadow_blur)) if shadow_blur > 0 else glyph_mask
        sh_rgba = np.zeros((ch, cw, 4), dtype=np.uint8)
        sh_rgba[:, :, 3] = np.clip(np.array(sh_m, dtype=np.float32) * (shadow_alpha / 255.0), 0, 255).astype(np.uint8)
        sh_layer = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
        sh_layer.paste(Image.fromarray(sh_rgba, mode="RGBA"), shadow_offset)
        canvas = Image.alpha_composite(canvas, sh_layer)

    # 2. Soft Ambient Glow
    if glow_color is not None and glow_alpha > 0:
        gl_m = glyph_mask.filter(ImageFilter.GaussianBlur(glow_blur))
        gl_rgba = np.zeros((ch, cw, 4), dtype=np.uint8)
        gl_rgba[:, :, :3] = glow_color
        gl_rgba[:, :, 3] = np.clip(np.array(gl_m, dtype=np.float32) * (glow_alpha / 255.0), 0, 255).astype(np.uint8)
        canvas = Image.alpha_composite(canvas, Image.fromarray(gl_rgba, mode="RGBA"))

    if glow2_color is not None and glow2_alpha > 0:
        gl2_m = glyph_mask.filter(ImageFilter.GaussianBlur(glow2_blur))
        gl2_rgba = np.zeros((ch, cw, 4), dtype=np.uint8)
        gl2_rgba[:, :, :3] = glow2_color
        gl2_rgba[:, :, 3] = np.clip(np.array(gl2_m, dtype=np.float32) * (glow2_alpha / 255.0), 0, 255).astype(np.uint8)
        canvas = Image.alpha_composite(canvas, Image.fromarray(gl2_rgba, mode="RGBA"))

    # 3. Delicate 1px Specular Highlight Rim (optional, ultra-clean)
    if bevel_3d:
        bev_rgba = np.zeros((ch, cw, 4), dtype=np.uint8)
        bev_rgba[:, :, :3] = bevel_color[:3]
        bev_rgba[:, :, 3] = np.clip(gm_np.astype(np.float32) * (bevel_color[3] / 255.0), 0, 255).astype(np.uint8)
        bev_layer = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
        bev_layer.paste(Image.fromarray(bev_rgba, mode="RGBA"), (-1, -1))
        canvas = Image.alpha_composite(canvas, bev_layer)

    # 4. Crisp Flat Front Glyph Face
    canvas = Image.alpha_composite(canvas, fill_layer)

    arr_a = np.array(canvas)[:, :, 3]
    ys, xs = np.where(arr_a > 2)
    if len(ys) > 0:
        cx0, cy0 = int(xs.min()), int(ys.min())
        cx1, cy1 = int(xs.max()) + 1, int(ys.max()) + 1
        canvas = canvas.crop((cx0, cy0, cx1, cy1))
        res = RichSprite(canvas, gx0 - cx0, gy0 - cy0, gx1 - cx0, gy1 - cy0, raw_cap_y0 - cy0, raw_cap_y1 - cy0)
    else:
        res = RichSprite(canvas, gx0, gy0, gx1, gy1, raw_cap_y0, raw_cap_y1)
    if len(_SPRITE_CACHE) < 768:
        _SPRITE_CACHE[cache_key] = res
    return res


# ==============================================================================
# 2B. AUTHENTIC 1:1 HUNG 3D CORRIDOR WALL SLAB ENGINE (t=49.6s — LOCKED RULE L17)
# ==============================================================================
_WALL3D_CACHE = {}

def render_3d_corridor_wall_slab(line_top, line_bot, side="left", flat_w=276, top_scale=1.22, bot_scale=1.34, bevel_px=6):
    """
    1:1 Pixel-Forensic Twin of Hung's 3D Corridor Wall Text (`CĂN HỘ / 2PN` & `DIỆN TÍCH / 107M2` at t=49.6s — L17):
      - Tall architectural `UTM Bebas.ttf` proportions matching `CĂN HỘ / 2PN` (`~380px` total height on left wall,
        `~295px` on right wall), with Row 2 guaranteed prominently taller & bolder than Row 1!
      - Ultra-tight `9px` optical vertical gap between Row 1 and Row 2 (measured on `CorrL_49.6s` & `CorrR_49.6s`!).
      - Horizon-aligned corridor wall perspective (`persp_w = 0.76 * flat_w`, top edge slopes down `+9.5%`,
        middle seam stays nearly horizontal, bottom edge slopes up `-9.5%`).
      - Authentic crisp `6px` warm-taupe/charcoal 3D side bevel (`rgb(122, 112, 104) -> rgb(64, 56, 50)`) pointing
        toward the hallway vanishing point + tight wall contact shadow (`blur=2.5px`, offset `(±4, +3)`).
    """
    key = (line_top, line_bot, side, int(flat_w), round(top_scale, 2), round(bot_scale, 2), int(bevel_px))
    if key in _WALL3D_CACHE:
        return _WALL3D_CACHE[key]

    SS = 2
    target_w = int(flat_w * SS)
    sz_t = match_font_size_to_width(FONT_BEBAS, line_top, target_w, min_size=60, max_size=360)
    sz_b = match_font_size_to_width(FONT_BEBAS, line_bot, target_w, min_size=80, max_size=460)
    ft = get_font(FONT_BEBAS, sz_t)
    fb = get_font(FONT_BEBAS, sz_b)

    bt = ft.getbbox(line_top)
    bb = fb.getbbox(line_bot)
    mt = Image.new("L", (target_w + 100, (bt[3] - bt[1]) + 80), 0)
    ImageDraw.Draw(mt).text((50 - bt[0], 40 - bt[1]), line_top, font=ft, fill=255)
    mb = Image.new("L", (target_w + 100, (bb[3] - bb[1]) + 80), 0)
    ImageDraw.Draw(mb).text((50 - bb[0], 40 - bb[1]), line_bot, font=fb, fill=255)

    at = np.array(mt)
    ab = np.array(mb)
    yt0, yt1 = np.where(at > 24)[0].min(), np.where(at > 24)[0].max() + 1
    xt0, xt1 = np.where(at > 24)[1].min(), np.where(at > 24)[1].max() + 1
    yb0, yb1 = np.where(ab > 24)[0].min(), np.where(ab > 24)[0].max() + 1
    xb0, xb1 = np.where(ab > 24)[1].min(), np.where(ab > 24)[1].max() + 1

    h_top = int(round((yt1 - yt0) * float(top_scale)))
    min_bot_ratio = 1.08 if len(line_bot) >= 8 else 1.28
    h_bot = max(int(round(h_top * min_bot_ratio)), int(round((yb1 - yb0) * float(bot_scale))))
    at_c = cv2.resize(at[yt0:yt1, xt0:xt1], (target_w, h_top), interpolation=cv2.INTER_CUBIC)
    ab_c = cv2.resize(ab[yb0:yb1, xb0:xb1], (target_w, h_bot), interpolation=cv2.INTER_CUBIC)

    gap_ss = 9 * SS
    slab_h = at_c.shape[0] + gap_ss + ab_c.shape[0]
    pad_ss = 52 * SS
    cw_ss = target_w + pad_ss * 2
    ch_ss = slab_h + pad_ss * 2

    flat_mask = np.zeros((ch_ss, cw_ss), dtype=np.uint8)
    flat_mask[pad_ss:pad_ss + at_c.shape[0], pad_ss:pad_ss + target_w] = at_c
    flat_mask[pad_ss + at_c.shape[0] + gap_ss:pad_ss + slab_h, pad_ss:pad_ss + target_w] = ab_c

    x0, y0 = float(pad_ss), float(pad_ss)
    x1, y1 = float(pad_ss + target_w), float(pad_ss + slab_h)
    src_q = np.float32([[x0, y0], [x1, y0], [x1, y1], [x0, y1]])

    persp_w = target_w * 0.76
    in_top = slab_h * 0.095
    in_bot = slab_h * 0.098
    if side == "left":
        dst_q = np.float32([
            [x0, y0],
            [x0 + persp_w, y0 + in_top],
            [x0 + persp_w, y1 - in_bot],
            [x0, y1],
        ])
    else:
        dst_q = np.float32([
            [x1 - persp_w, y0 + in_top],
            [x1, y0],
            [x1, y1],
            [x1 - persp_w, y1 - in_bot],
        ])

    M_p = cv2.getPerspectiveTransform(src_q, dst_q)
    warped_ss = cv2.warpPerspective(flat_mask, M_p, (cw_ss, ch_ss), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_CONSTANT, borderValue=0)

    cw, ch = cw_ss // SS, ch_ss // SS
    front_mask = cv2.resize(warped_ss, (cw, ch), interpolation=cv2.INTER_AREA)

    ys_f, xs_f = np.where(front_mask > 32)
    ix0, iy0 = int(xs_f.min()), int(ys_f.min())
    ix1, iy1 = int(xs_f.max()) + 1, int(ys_f.max()) + 1

    # Subtle surface-normal shading so underside bevel edges are slightly deeper warm charcoal than vertical side edges
    gx = cv2.Sobel(front_mask.astype(np.float32), cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(front_mask.astype(np.float32), cv2.CV_32F, 0, 1, ksize=3)
    gnorm = np.sqrt(gx * gx + gy * gy) + 1e-5
    ny = gy / gnorm
    shade_mod = cv2.GaussianBlur(1.0 + 0.14 * ny, (5, 5), 1.0)

    canvas = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    dir_x = 0.88 if side == "left" else -0.88
    dir_y = 0.34

    # 1. Crisp Tight Wall Contact Shadow (exact match to `4_Corr3D_LeftDetail` `2PN` & `5_Corr3D_RightDetail` `107M2`!)
    sh_dx = int(round((bevel_px + 2.2) * dir_x))
    sh_dy = int(round((bevel_px + 2.5) * 0.52))
    sh_blur = cv2.GaussianBlur(front_mask, (9, 9), 2.3).astype(np.float32)
    sh_rgba = np.zeros((ch, cw, 4), dtype=np.uint8)
    sh_rgba[:, :, :3] = (46, 38, 32)  # Warm walnut-wall shadow tone
    sh_rgba[:, :, 3] = np.clip(sh_blur * 0.48, 0, 255).astype(np.uint8)
    sh_layer = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    sh_layer.paste(Image.fromarray(sh_rgba, mode="RGBA"), (sh_dx, sh_dy))
    canvas = Image.alpha_composite(canvas, sh_layer)

    # 2. Crisp 5px Warm-Taupe / Charcoal 3D Bevel Extrusion (`rgb(122, 112, 104) -> rgb(68, 60, 54)`)
    c_near = np.array([124.0, 114.0, 106.0], dtype=np.float32)
    c_far  = np.array([68.0,  60.0,  54.0],  dtype=np.float32)
    fm_f = front_mask.astype(np.float32)

    n_sub = int(bevel_px * 2)  # Half-pixel steps for zero staircase aliasing!
    for s_idx in range(n_sub, 0, -1):
        k = s_idx * 0.5
        frac = (s_idx - 1) / float(max(1, n_sub - 1))
        tx = k * dir_x
        ty = k * dir_y
        M_k = np.float32([[1.0, 0.0, tx], [0.0, 1.0, ty]])
        m_k = cv2.warpAffine(fm_f, M_k, (cw, ch), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
        sh_k = cv2.warpAffine(shade_mod, M_k, (cw, ch), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=1.0)

        base_col = c_near * (1.0 - frac) + c_far * frac
        ext_rgba = np.zeros((ch, cw, 4), dtype=np.uint8)
        ext_rgba[:, :, :3] = np.clip(base_col[None, None, :] * sh_k[:, :, None], 0, 255).astype(np.uint8)
        ext_rgba[:, :, 3] = np.clip(m_k * 1.02, 0, 255).astype(np.uint8)
        canvas = Image.alpha_composite(canvas, Image.fromarray(ext_rgba, mode="RGBA"))

    # 3. Pure Bright Matte-Gloss White Front Face (`#FFFFFF`)
    grad_im = make_gradient_rgb(cw, max(1, iy1 - iy0), ARCH_WHITE_3D, sparkle=False)
    front_rgb = Image.new("RGB", (cw, ch), (246, 245, 243))
    front_rgb.paste(grad_im, (0, iy0))
    front_rgba = front_rgb.convert("RGBA")
    front_rgba.putalpha(Image.fromarray(front_mask, mode="L"))
    canvas = Image.alpha_composite(canvas, front_rgba)

    arr_a = np.array(canvas)[:, :, 3]
    ys, xs = np.where(arr_a > 2)
    cx0, cy0 = int(xs.min()), int(ys.min())
    cx1, cy1 = int(xs.max()) + 1, int(ys.max()) + 1
    canvas = canvas.crop((cx0, cy0, cx1, cy1))
    res = RichSprite(canvas, ix0 - cx0, iy0 - cy0, ix1 - cx0, iy1 - cy0)
    _WALL3D_CACHE[key] = res
    return res


# ==============================================================================
# 2C. SUB-PIXEL PASTE + SMOOTH EASE-IN / LATE 6-FRAME EASE-OUT CONTROLLERS (L15)
# ==============================================================================
def alpha_paste_ink(
    dst_bgr, rsp: RichSprite, ink_cx, ink_cy, scale=1.0, opacity=1.0, clip_box=None,
    wipe_lr_prog=None, wipe_feather_px=44.0, curtain_bottom_y=None, blur_mix=0.0
):
    if opacity <= 0.01 or scale <= 0.02:
        return dst_bgr
    if wipe_lr_prog is not None and wipe_lr_prog <= 0.005:
        return dst_bgr

    src_sharp = rsp.arr
    if blur_mix > 0.02:
        bm = min(1.0, float(blur_mix))
        src_blur = rsp.get_blurred_arr()
        src = cv2.addWeighted(src_sharp, 1.0 - bm, src_blur, bm, 0.0)
    else:
        src = src_sharp

    sh, sw = src.shape[:2]
    s = float(scale)

    x_tl_f = float(ink_cx) - rsp.ink_cx * s
    y_tl_f = float(ink_cy) - rsp.ink_cy * s
    nw_f = sw * s
    nh_f = sh * s

    bx0, by0, bx1, by1 = (0, 0, W, H) if clip_box is None else (
        max(0, int(clip_box[0])), max(0, int(clip_box[1])),
        min(W, int(clip_box[2])), min(H, int(clip_box[3]))
    )

    dx0 = max(bx0, int(math.floor(x_tl_f)) - 1)
    dy0 = max(by0, int(math.floor(y_tl_f)) - 1)
    dx1 = min(bx1, int(math.ceil(x_tl_f + nw_f)) + 1)
    dy1 = min(by1, int(math.ceil(y_tl_f + nh_f)) + 1)
    if dx1 <= dx0 or dy1 <= dy0:
        return dst_bgr

    if abs(s - 1.0) < 0.001 and abs(x_tl_f - round(x_tl_f)) < 0.02 and abs(y_tl_f - round(y_tl_f)) < 0.02:
        xi, yi = int(round(x_tl_f)), int(round(y_tl_f))
        ix0, iy0 = max(bx0, xi), max(by0, yi)
        ix1, iy1 = min(bx1, xi + sw), min(by1, yi + sh)
        if ix1 <= ix0 or iy1 <= iy0:
            return dst_bgr
        sub = src[iy0 - yi:iy1 - yi, ix0 - xi:ix1 - xi]
    else:
        inv_s = 1.0 / s
        tx = (dx0 - x_tl_f) * inv_s
        ty = (dy0 - y_tl_f) * inv_s
        M_inv = np.array([[inv_s, 0.0, tx], [0.0, inv_s, ty]], dtype=np.float32)
        sub = cv2.warpAffine(
            src, M_inv, (dx1 - dx0, dy1 - dy0),
            flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP,
            borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0)
        )
        ix0, iy0, ix1, iy1 = dx0, dy0, dx1, dy1

    a = (sub[:, :, 3:4].astype(np.float32) / 255.0) * float(opacity)

    if wipe_lr_prog is not None and wipe_lr_prog < 0.999:
        ink_left_dst = x_tl_f + rsp.ink_x0 * s - 8.0
        ink_span_dst = rsp.ink_w * s + 24.0
        edge_x = ink_left_dst + (ink_span_dst + wipe_feather_px) * float(wipe_lr_prog)
        xs_roi = np.arange(ix0, ix1, dtype=np.float32)[None, :, None]
        w_mask = np.clip((edge_x - xs_roi) / max(4.0, float(wipe_feather_px)), 0.0, 1.0)
        a = a * w_mask

    if curtain_bottom_y is not None:
        ys_roi = np.arange(iy0, iy1, dtype=np.float32)[:, None, None]
        c_mask = np.clip((float(curtain_bottom_y) - ys_roi) / 13.0, 0.0, 1.0)
        a = a * c_mask

    src_bgr = sub[:, :, [2, 1, 0]].astype(np.float32)
    roi = dst_bgr[iy0:iy1, ix0:ix1].astype(np.float32)
    dst_bgr[iy0:iy1, ix0:ix1] = np.clip(roi * (1.0 - a) + src_bgr * a, 0, 255).astype(np.uint8)
    return dst_bgr


def paste_animated_piece(
    dst_bgr, rsp: RichSprite, ink_cx, ink_cy, age_f, rem_f,
    delay_f=0, in_f=17, out_f=6, style="mask_rise_up",
    clip_box=None, slide_dir=1, vp_vec=(0.0, 0.0), base_scale=1.0
):
    """
    Studio Motion Controller (Locked Rules L5, L14, L15):
      - Smooth C1 Ease-In-Out entrance (`in_f = 16..18f`).
      - Holds 100% solid & crystal-sharp across the shot (`opacity = 1.0`), with a crisp, gentle
        `out_f = 6 frames` (`0.20s`) Ease-In-Out dissolve right at the transition so text NEVER exits too early!
    """
    local_age = age_f - delay_f
    if local_age < 0 or rem_f <= 0:
        return dst_bgr

    p_in_raw = min(1.0, (local_age + 1) / float(max(1, in_f)))
    p_out_raw = min(1.0, float(rem_f) / float(max(1, out_f)))
    p_out = ease_in_out_cubic(p_out_raw)

    dx, dy, sc, op = 0.0, 0.0, 1.0, 1.0
    wipe_p = None
    curtain_y = None
    blur_m = 0.0

    if style == "brush_wipe_lr":
        p_in = ease_in_out_cubic(p_in_raw)
        wipe_p = p_in
        dx = -9.0 * (1.0 - p_in)
        op = ease_in_out_sine(min(1.0, p_in_raw * 1.45)) * p_out
        dy = -4.0 * (1.0 - p_out)
        sc = 0.99 + 0.01 * p_out

    elif style == "mask_rise_up":
        p_in = ease_in_out_quart(p_in_raw)
        dy = 24.0 * (1.0 - p_in) - 5.0 * (1.0 - p_out)
        op = ease_in_out_sine(min(1.0, p_in_raw * 1.35)) * p_out
        if p_in_raw < 1.0:
            curtain_y = float(ink_cy) + rsp.ink_h * 0.56 + 10.0

    elif style == "pop_3d_depth":
        sc_in = ease_in_out_scale(local_age, dur_f=in_f, start_scale=0.80, peak_scale=1.032)
        p_in = ease_in_out_cubic(p_in_raw)
        dy = 10.0 * (1.0 - p_in) - 4.0 * (1.0 - p_out)
        sc = sc_in * (0.96 + 0.04 * p_out)
        op = ease_in_out_cubic(min(1.0, p_in_raw * 1.5)) * p_out

    elif style == "glide_side_mask":
        p_in = ease_in_out_cubic(p_in_raw)
        dx = (-28.0 * float(slide_dir)) * (1.0 - p_in) + (8.0 * float(slide_dir)) * (1.0 - p_out)
        op = ease_in_out_sine(min(1.0, p_in_raw * 1.35)) * p_out
        sc = (0.96 + 0.04 * p_in) * (0.98 + 0.02 * p_out)

    elif style == "focus_rack_in":
        p_in = ease_in_out_cubic(p_in_raw)
        blur_m = max(1.0 - p_in, 0.55 * (1.0 - p_out))
        sc = (1.045 - 0.045 * p_in) * (0.98 + 0.02 * p_out)
        dy = 6.0 * (1.0 - p_in) - 4.0 * (1.0 - p_out)
        op = ease_in_out_sine(p_in_raw) * p_out

    elif style == "wall_3d_glide":
        p_in = ease_in_out_cubic(p_in_raw)
        dx = vp_vec[0] * (1.0 - p_in)
        dy = vp_vec[1] * (1.0 - p_in)
        sc = (0.90 + 0.10 * p_in) * (1.0 + 0.02 * (1.0 - p_out))
        op = ease_in_out_cubic(min(1.0, p_in_raw * 1.30)) * p_out

    return alpha_paste_ink(
        dst_bgr, rsp, float(ink_cx) + dx, float(ink_cy) + dy,
        scale=sc * float(base_scale), opacity=op, clip_box=clip_box,
        wipe_lr_prog=wipe_p, curtain_bottom_y=curtain_y, blur_mix=blur_m
    )


# ==============================================================================
# 3. PERSISTENT HEADER LOGO & BLACK BRAND OUTRO (R18)
# ==============================================================================
_HEADER_RSP = None
def get_header_sprite():
    global _HEADER_RSP
    if _HEADER_RSP is None:
        cw, ch = 260, 110
        im = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
        dr = ImageDraw.Draw(im)
        f_le = get_font(FONT_SANS_REG, 18)
        f_pp = get_font(FONT_BOLD_SER, 36)
        f_pc = get_font(FONT_SANS_REG, 12)
        for dx, dy, col in [(1, 2, (0, 0, 0, 135)), (0, 0, (255, 255, 255, 240))]:
            b1 = f_le.getbbox("LE")
            dr.text(((cw - (b1[2] - b1[0])) // 2 + dx, 6 + dy), "LE", font=f_le, fill=col)
            b2 = f_pp.getbbox("Parc Place")
            dr.text(((cw - (b2[2] - b2[0])) // 2 + dx, 26 + dy), "Parc Place", font=f_pp, fill=col)
            sub_t = "P A R K C I T Y   H A N O I"
            b3 = f_pc.getbbox(sub_t)
            dr.text(((cw - (b3[2] - b3[0])) // 2 + dx, 72 + dy), sub_t, font=f_pc, fill=col)
        _HEADER_RSP = RichSprite(im, 0, 0, cw, ch)
    return _HEADER_RSP

def draw_header_logo(bgr, opacity=0.92):
    cx, cy = int(W * 0.855), int(H * 0.046)
    roi = bgr[max(0, cy - 45):min(H, cy + 45), max(0, cx - 110):min(W, cx + 110)]
    if roi.size > 0 and float(roi.mean()) > 175.0:
        apply_soft_spot_scrim(bgr, cx, cy, rx=118, ry=46, strength=0.26 * opacity)
    return alpha_paste_ink(bgr, get_header_sprite(), cx, cy, scale=1.0, opacity=opacity)

def render_black_outro_frame(local_f, total_f):
    bgr = np.zeros((H, W, 3), dtype=np.uint8)
    fade_in = ease_in_out_cubic((local_f + 1) / 22.0)
    op = fade_in * 0.96
    scale = 1.60 + 0.05 * ease_in_out_sine(local_f / float(max(1, total_f - 1)))
    alpha_paste_ink(bgr, get_header_sprite(), W // 2, int(H * 0.48), scale=scale, opacity=op)
    bar_w = int(180 * ease_in_out_cubic(max(0.0, (local_f - 4) / 22.0)))
    if bar_w > 4:
        cv2.line(bgr, (W // 2 - bar_w // 2, int(H * 0.548)), (W // 2 + bar_w // 2, int(H * 0.548)), (95, 190, 235), 2, cv2.LINE_AA)
    return bgr


# ==============================================================================
# 4. ARCHETYPE B — COHESIVE FULL-DISPLAY CARBON PILL & SPLIT-SEAM PILL (L7–L9, L14–L18)
#    (0% partial-line wipes! Tight 12px reference line spacing! Maximum solid hold!)
# ==============================================================================
_CARBON_STRIPES = None
def get_carbon_stripes(w, h):
    global _CARBON_STRIPES
    if _CARBON_STRIPES is None or _CARBON_STRIPES.shape[:2] != (h, w):
        yy, xx = np.mgrid[0:h, 0:w]
        phase = ((xx + yy) % 14).astype(np.float32) / 14.0
        _CARBON_STRIPES = 0.5 + 0.5 * np.cos(2.0 * math.pi * phase)
    return _CARBON_STRIPES


def draw_carbon_pill_overlay(
    bgr, age_f, rem_f, tag_top, line1_gold, line2_white, cy_norm=0.818,
    d_tag=2, d_l1=4, d_l2=7, out_f=6
):
    """
    1:1 Reference Carbon Pill (`1_CarbonPill_12.2s` — Locked Rules L7–L9, L14–L18):
      - Opens smoothly in 18f (`ease_in_out_cubic`) and displays FULL Line 1 & Line 2 right from the start!
      - Clean flat Gold (`72px`) + clean White (`52px`) with exact tight `12px` reference optical line spacing!
      - Holds 100% solid right until the final `6 frames` (`0.20s`).
    """
    fade_out = ease_in_out_cubic(min(1.0, max(0.0, float(rem_f) / float(max(1, out_f)))))
    if fade_out <= 0.02:
        return bgr

    full_w, pill_h = 884, 196
    R = pill_h // 2
    safe_flat_w = full_w - 2 * R + 16  # 704px safe chord zone (matches REF 12.2s 1:1!)

    exp_prog = ease_in_out_cubic((age_f + 1) / 18.0)
    cur_w = max(pill_h, int(round(pill_h + (full_w - pill_h) * exp_prog)))

    x0 = W // 2 - cur_w // 2
    x1 = x0 + cur_w
    cy = int(round(H * cy_norm))
    y0 = cy - R
    y1 = y0 + pill_h

    pw, ph = cur_w, pill_h
    pad_g = 12
    gw, gh = pw + pad_g * 2, ph + pad_g * 2

    mask_pil = Image.new("L", (pw * 2, ph * 2), 0)
    ImageDraw.Draw(mask_pil).rounded_rectangle([3, 3, pw * 2 - 4, ph * 2 - 4], radius=ph - 3, fill=255)
    mask = np.array(mask_pil.resize((pw, ph), Image.Resampling.LANCZOS), dtype=np.float32) / 255.0

    border_pil = Image.new("L", (gw * 2, gh * 2), 0)
    ImageDraw.Draw(border_pil).rounded_rectangle(
        [pad_g * 2 + 3, pad_g * 2 + 3, (gw - pad_g) * 2 - 4, (gh - pad_g) * 2 - 4],
        radius=ph - 3, outline=255, width=9
    )
    rim_1x = border_pil.resize((gw, gh), Image.Resampling.LANCZOS)
    rim_glow = np.array(rim_1x.filter(ImageFilter.GaussianBlur(5)), dtype=np.float32) / 255.0
    rim_core = np.array(rim_1x, dtype=np.float32) / 255.0

    roi = bgr[y0:y1, x0:x1].astype(np.float32)
    blurred = cv2.GaussianBlur(bgr[y0:y1, x0:x1], (17, 17), 0).astype(np.float32)
    mean_lum = float(blurred.mean())
    glass_alpha = 0.62 if mean_lum <= 125.0 else min(0.74, 0.62 + (mean_lum - 125.0) * 0.0013)

    s_off = (full_w - pw) // 2
    stripes = get_carbon_stripes(full_w, pill_h)[:, s_off:s_off + pw]
    smoked_carbon = blurred * 0.28 + np.array([18.0, 18.0, 16.0])[None, None, :] + (stripes[:, :, None] * 13.5)

    m3 = (mask[:, :, None]) * fade_out
    roi = roi * (1.0 - m3 * glass_alpha) + smoked_carbon * (m3 * glass_alpha)
    bgr[y0:y1, x0:x1] = np.clip(roi, 0, 255).astype(np.uint8)

    gx0, gy0 = max(0, x0 - pad_g), max(0, y0 - pad_g)
    gx1, gy1 = min(W, x1 + pad_g), min(H, y1 + pad_g)
    sx0, sy0 = gx0 - (x0 - pad_g), gy0 - (y0 - pad_g)
    sx1, sy1 = sx0 + (gx1 - gx0), sy0 + (gy1 - gy0)
    groi = bgr[gy0:gy1, gx0:gx1].astype(np.float32)
    gl_a = np.clip(rim_glow[sy0:sy1, sx0:sx1, None] * 0.34 * fade_out, 0.0, 1.0)
    cr_a = np.clip(rim_core[sy0:sy1, sx0:sx1, None] * 1.12 * fade_out, 0.0, 1.0)
    cyan_glow_bgr = np.array([235.0, 225.0, 110.0])[None, None, :]
    cyan_rim_bgr  = np.array([234.0, 244.0, 140.0])[None, None, :]
    groi = groi * (1.0 - gl_a) + cyan_glow_bgr * gl_a
    groi = groi * (1.0 - cr_a) + cyan_rim_bgr * cr_a
    bgr[gy0:gy1, gx0:gx1] = np.clip(groi, 0, 255).astype(np.uint8)

    # Exact REF 12.2s Carbon Pill font sizes & diacritic-immune baseline anchors (`MÔI TRƯỜNG SỐNG` 88pt, Line 2 62pt)!
    f1_probe = get_font(FONT_BEBAS, 88)
    w1_raw = max(1, f1_probe.getbbox(line1_gold)[2] - f1_probe.getbbox(line1_gold)[0])
    cond1 = min(1.0, max(0.80, (safe_flat_w - 8) / float(w1_raw)))
    sp_l1 = render_rich_sprite(
        line1_gold, FONT_BEBAS, 88, PILL_GOLD,
        shadow_offset=(3, 4), shadow_blur=4, shadow_alpha=210,
        glow_color=(245, 175, 20), glow_blur=7, glow_alpha=65,
        condense_x=cond1
    )

    f2_probe = get_font(FONT_BEBAS, 62)
    w2_raw = max(1, f2_probe.getbbox(line2_white)[2] - f2_probe.getbbox(line2_white)[0]) if line2_white else 1
    cond2 = min(1.0, max(0.80, (safe_flat_w - 4) / float(w2_raw)))
    sp_l2 = render_rich_sprite(
        line2_white, FONT_BEBAS, 62, CREAM_IVORY,
        shadow_offset=(2, 3), shadow_blur=3, shadow_alpha=210,
        condense_x=cond2
    )

    # Baseline-locked coordinates inside 196px Carbon Pill (`y0 + 98` & `y0 + 166` — immune to `Ị, Ợ` under-dots!)
    l1_base_target = float(y0 + 98)
    l2_base_target = float(y0 + 166)
    l1_icy = l1_base_target + (sp_l1.ink_cy - sp_l1.cap_y1)
    l2_icy = l2_base_target + (sp_l2.ink_cy - sp_l2.cap_y1)

    cur_safe_half = max(0, cur_w // 2 - R + 12)
    clip_inner = (W // 2 - cur_safe_half, y0 + 10, W // 2 + cur_safe_half, y1 - 8)

    if cur_safe_half > 40:
        paste_animated_piece(bgr, sp_l1, W * 0.5, l1_icy, age_f, rem_f, delay_f=d_l1, in_f=16, out_f=out_f, style="mask_rise_up", clip_box=clip_inner)
        if line2_white:
            paste_animated_piece(bgr, sp_l2, W * 0.5, l2_icy, age_f, rem_f, delay_f=d_l2, in_f=16, out_f=out_f, style="mask_rise_up", clip_box=clip_inner)

    if tag_top and age_f >= d_tag:
        _, sz_t = fit_font(FONT_TAG_IT, tag_top, 56, safe_flat_w - 20)
        sp_tag = render_rich_sprite(
            tag_top, FONT_TAG_IT, sz_t, PURE_WHITE,
            shadow_offset=(3, 4), shadow_blur=4, shadow_alpha=235,
            glow_color=(56, 189, 248), glow_blur=9, glow_alpha=185
        )
        x0_full = W // 2 - full_w // 2
        tag_ink_left = float(x0_full + 46)
        tag_icx = tag_ink_left + sp_tag.ink_w * 0.5
        tag_icy = float(y0 - 12) - sp_tag.ink_h * 0.5
        op_sc = ease_in_out_cubic(min(1.0, (age_f - d_tag + 1) / 14.0)) * fade_out
        apply_soft_spot_scrim(bgr, tag_icx, tag_icy, rx=sp_tag.ink_w * 0.65, ry=32, strength=0.32 * op_sc)
        paste_animated_piece(bgr, sp_tag, tag_icx, tag_icy, age_f, rem_f, delay_f=d_tag, in_f=15, out_f=out_f, style="glide_side_mask")

    return bgr


def draw_split_seam_pill(
    bgr, age_f, rem_f, script_top, big_left, right_l1, right_l2, cy_norm=0.502,
    d_sc=3, d_big=5, d_r1=7, d_r2=9, out_f=6
):
    """
    Exact 1:1 Pixel-Ruler Twin of Hung's Split-Seam Olive Pill (`t=27.0s` — Locked Rule L20):
      - Pill Box: `844 × 184 px` (`x = 118 -> 962`, `R = 92`), rich sage-olive frosted glass.
      - Left Big Hero (`4 MỤC`, `2-4PN`): Fixed `122px` cap-body height (`y0 + 42 -> y0 + 164`), warm cream-yellow,
        completely immune to `Ụ` under-dots!
      - Top-Left Ice-Cyan Script (`Căn`, `Đối chiếu` in `Smooch-Regular`): Giant initial capital (`122px` tall)
        rising `56px` ABOVE `y0`, while lowercase sits along `y0` (`ink_bottom = y0 + 30`), leaving a clean `12px`
        gap above `big_left` with `0px` overlap!
      - Column Gap: Fixed `40px` (`x` right of `big_left` -> `x` left of `right_l1`).
      - Right Line 1 (`TRONG HỢP ĐỒNG`, `& BIỆT THỰ TRÊN KHÔNG`): Tall `69px` cap-body (`96pt` `UTM Bebas`,
        `baseline = y0 + 88`), glowing Ice-White, immune to `Ợ` under-dot & `Ồ` circumflex!
      - Right Line 2 (`( Vị trí - Thời hạn - Chi phí )`): Large `46–48pt` `UTM AptimaItalic` placed at exact
        `18px` below `right_l1` baseline (`top = y0 + 106`), spanning ~93% of `right_l1` width!
    """
    fade_out = ease_in_out_cubic(min(1.0, max(0.0, float(rem_f) / float(max(1, out_f)))))
    if fade_out <= 0.02:
        return bgr

    full_w, ph = 844, 184
    R = ph // 2

    exp_prog = ease_in_out_cubic((age_f + 1) / 18.0)
    cur_w = max(ph, int(round(ph + (full_w - ph) * exp_prog)))
    x0 = W // 2 - cur_w // 2
    x1 = x0 + cur_w
    cy = int(round(H * cy_norm))
    y0 = cy - R
    y1 = y0 + ph

    mask_pil = Image.new("L", (cur_w * 2, ph * 2), 0)
    ImageDraw.Draw(mask_pil).rounded_rectangle([3, 3, cur_w * 2 - 4, ph * 2 - 4], radius=ph - 3, fill=255)
    mask = (np.array(mask_pil.resize((cur_w, ph), Image.Resampling.LANCZOS), dtype=np.float32) / 255.0)[:, :, None] * fade_out

    roi = bgr[y0:y1, x0:x1].astype(np.float32)
    blurred = cv2.GaussianBlur(bgr[y0:y1, x0:x1], (21, 21), 0).astype(np.float32)
    mean_lum_sp = float(blurred.mean())
    if mean_lum_sp > 175.0:
        olive_glass = blurred * 0.12 + np.array([52.0, 78.0, 62.0])[None, None, :] * 0.88
        glass_op = 0.88
    else:
        olive_glass = blurred * 0.22 + np.array([56.0, 82.0, 66.0])[None, None, :] * 0.78
        glass_op = 0.84
    roi = roi * (1.0 - mask * glass_op) + olive_glass * (mask * glass_op)
    bgr[y0:y1, x0:x1] = np.clip(roi, 0, 255).astype(np.uint8)

    # 1. Left Big Hero (`170pt` UTM Bebas = exact `121px` cap height, bold meaty stems, width <= 216px!)
    _, sz_big_fit = fit_font(FONT_BEBAS, big_left, 170, int(216 / 0.78))
    sz_big = max(158, sz_big_fit)
    fb_probe = get_font(FONT_BEBAS, sz_big)
    wb_raw = max(1, fb_probe.getbbox(big_left)[2] - fb_probe.getbbox(big_left)[0])
    cond_big = min(1.0, 216.0 / float(wb_raw))
    sb_big = 1 if cond_big < 0.88 else 0
    sp_big = render_rich_sprite(
        big_left, FONT_BEBAS, sz_big,
        [(0.0, (255, 252, 198)), (1.0, (248, 229, 138))],
        shadow_offset=(2, 2), shadow_blur=3, shadow_alpha=95,
        condense_x=cond_big, stroke_boost=sb_big
    )

    # 2. Right Column Line 1 (`96pt` UTM Bebas like `CÓ THÊM STUDY` `70px` cap-height, guaranteed <= 430px wide!)
    _, sz_r1_fit = fit_font(FONT_BEBAS, right_l1, 96, int(430 / 0.80))
    sz_r1 = max(88, sz_r1_fit)
    fr1_probe = get_font(FONT_BEBAS, sz_r1)
    wr1_raw = max(1, fr1_probe.getbbox(right_l1)[2] - fr1_probe.getbbox(right_l1)[0])
    cond_r1 = min(1.0, 430.0 / float(wr1_raw))
    sb_r1 = 1 if cond_r1 < 0.86 else 0
    sp_r1 = render_rich_sprite(
        right_l1, FONT_BEBAS, sz_r1, PURE_WHITE,
        shadow_offset=(2, 2), shadow_blur=3, shadow_alpha=85,
        glow_color=(36, 196, 238), glow_blur=8, glow_alpha=205,
        glow2_color=(160, 242, 252), glow2_blur=2, glow2_alpha=150,
        condense_x=cond_r1, stroke_boost=sb_r1
    )

    # 3. Right Column Line 2 (`UTM AptimaBoldItalic` at `46pt` = exact `33px` cap-height & crisp medium-bold white stroke matching `( Diện tích : 107m2 )`!)
    target_r2_maxw = min(414, int(sp_r1.ink_w * 0.96))
    _, sz_r2_fit = fit_font(FONT_APTIMA_BI, right_l2, 47, int(target_r2_maxw / 0.80))
    sz_r2 = max(44, sz_r2_fit)
    fr2_probe = get_font(FONT_APTIMA_BI, sz_r2)
    wr2_raw = max(1, fr2_probe.getbbox(right_l2)[2] - fr2_probe.getbbox(right_l2)[0])
    cond_r2 = min(1.0, float(target_r2_maxw) / float(wr2_raw))
    sp_r2 = render_rich_sprite(
        right_l2, FONT_APTIMA_BI, sz_r2, PURE_WHITE,
        shadow_offset=(1, 2), shadow_blur=2, shadow_alpha=125,
        condense_x=cond_r2
    )

    # 4. Exact Horizontal Group Layout (`col_gap = 38px`, centered cleanly inside `844px` pill `x = 118 -> 962`!)
    col_gap = 38.0
    right_w = max(sp_r1.ink_w, sp_r2.ink_w)
    group_w = sp_big.ink_w + col_gap + right_w  # Max 216 + 38 + 430 = 684px -> >=80px safe margin on BOTH ends!
    group_x0 = W * 0.5 - group_w * 0.5 + 4.0

    big_icx = group_x0 + sp_big.ink_w * 0.5
    rx_c    = group_x0 + sp_big.ink_w + col_gap + right_w * 0.5

    # 5. Exact Diacritic-Immune Vertical Coordinates matching REF `t=27.0s` 1:1!
    big_cap_top_target = float(y0 + 42)
    big_icy = big_cap_top_target + (sp_big.ink_cy - sp_big.cap_y0)

    r1_base_target = float(y0 + 88)
    r1_icy = r1_base_target + (sp_r1.ink_cy - sp_r1.cap_y1)

    r2_cap_top_target = float(y0 + 106)  # Exact `18px` below `r1_baseline` (`y = 960 -> 978` in REF)!
    r2_icy = r2_cap_top_target + (sp_r2.ink_cy - sp_r2.cap_y0)

    cur_safe_half = max(0, cur_w // 2 - 44)
    if cur_safe_half < 60:
        return bgr
    clip_inner = (W // 2 - cur_safe_half, y0 + 2, W // 2 + cur_safe_half, y1 - 2)
    clip_sc    = (W // 2 - cur_safe_half - 24, y0 - 84, W // 2 + cur_safe_half + 18, y1 - 2)

    # 6. Silky Flowing Calligraphic Ribbon in Box (`GreatVibes-Regular` with `-0.22` forward calligraphic slant — Locked Rule L21!):
    #    Rendered as ONE continuous, soft, connected handwritten word (`Đối chiếu`, `Căn`) with ZERO character splitting
    #    and ZERO horizontal squishing: initial capital (`Đ`, `C`) sweeps gracefully `~48px` ABOVE `y0`, while lowercase
    #    baseline (`cap_y1`) anchors cleanly at `y0 + 30` (`12px` clear gap above `big_left`)!
    if script_top:
        max_sc_w = int(sp_big.ink_w + (44 if len(script_top) <= 4 else 32))
        target_sc_sz = 114 if len(script_top) <= 4 else 86
        _, sz_sc = fit_font(FONT_GREATVIBES, script_top, target_sc_sz, max_sc_w)
        sz_sc = max(70, sz_sc)
        sp_sc = render_rich_sprite(
            script_top, FONT_GREATVIBES, sz_sc,
            [(0.0, (246, 255, 255)), (0.62, (192, 248, 255)), (1.0, (138, 236, 252))],
            shadow_offset=(1, 2), shadow_blur=2, shadow_alpha=(95 if mean_lum_sp > 175.0 else 65),
            glow_color=(20, 188, 236), glow_blur=10, glow_alpha=235,
            glow2_color=(165, 246, 255), glow2_blur=3, glow2_alpha=145,
            shear_x=-0.22
        )
        sc_left = group_x0 - (14.0 if len(script_top) <= 4 else 24.0)
        sc_icx  = sc_left + sp_sc.ink_w * 0.5
        sc_base_target = float(y0 + (33 if len(script_top) <= 4 else 30))
        sc_icy  = sc_base_target + (sp_sc.ink_cy - sp_sc.cap_y1)
        if mean_lum_sp > 175.0 and age_f >= d_sc:
            op_sc_bg = ease_in_out_cubic(min(1.0, (age_f - d_sc + 1) / 14.0)) * fade_out
            apply_soft_spot_scrim(bgr, sc_icx - 22.0, y0 - 14.0, rx=88, ry=34, strength=0.26 * op_sc_bg)
        paste_animated_piece(bgr, sp_sc, sc_icx, sc_icy, age_f, rem_f, delay_f=d_sc, in_f=16, out_f=out_f, style="brush_wipe_lr", clip_box=clip_sc)

    paste_animated_piece(bgr, sp_big, big_icx, big_icy, age_f, rem_f, delay_f=d_big, in_f=16, out_f=out_f, style="pop_3d_depth", clip_box=clip_inner)

    if script_top:
        clip_sc_top = (clip_sc[0], clip_sc[1], clip_sc[2], y0 + 40)
        paste_animated_piece(bgr, sp_sc, sc_icx, sc_icy, age_f, rem_f, delay_f=d_sc, in_f=16, out_f=out_f, style="brush_wipe_lr", clip_box=clip_sc_top)

    paste_animated_piece(bgr, sp_r1, rx_c, r1_icy, age_f, rem_f, delay_f=d_r1, in_f=16, out_f=out_f, style="glide_side_mask", clip_box=clip_inner)
    paste_animated_piece(bgr, sp_r2, rx_c, r2_icy, age_f, rem_f, delay_f=d_r2, in_f=16, out_f=out_f, style="mask_rise_up", clip_box=clip_inner)
    return bgr


# ==============================================================================
# 5. ARCHETYPE A — SELECTIVE MULTI-COLOR KEYTEXT CLUSTERS WITH EXACT 1:1 HUNG LINE SPACING (L14, L15, L17, L18)
# ==============================================================================
def draw_hook_wordplay_p1(bgr, age_f, rem_f):
    """
    1:1 Pixel Twin of Sếp's Reference Screenshot `Hook_1.8s` (`Khi mua / Căn hộ / hơn / 11 TỶ` — L14, L15, L17, L18):
      - Giant sweeping capital `"C"` (`152px` Script) + `"ăn hộ"` (`88px` Script) so `"Mua"` (`48px` White Italic)
        nestles cleanly in the upper-right pocket above `"ăn hộ"` (`4px` clear gap, `0px` overlap!) with its top
        aligned on the EXACT SAME Y-LINE as the top of giant `"C"`!
      - Clean flat-face Gold `UTM Bebas` `[Giant "SLOT" | "tặng" / "ĐỖ XE"]` + tight `4px` `"Ô TÔ ĐỊNH DANH"`.
      - Fully revealed by `t = 2.20s` -> HOLDS 100% SOLID FOR `1.83 FULL SECONDS` (`out_f = 6`)!
    """
    fade_scrim = ease_in_out_cubic(min(1.0, (age_f + 1) / 14.0)) * ease_in_out_cubic(min(1.0, max(0.0, float(rem_f) / 6.0)))
    apply_soft_spot_scrim(bgr, 242, int(H * 0.515), rx=235, ry=230, strength=0.52 * fade_scrim)

    sp_mua = render_rich_sprite(
        "Mua", FONT_APTIMA_IT, 48, PURE_WHITE,
        shadow_offset=(3, 4), shadow_blur=4, shadow_alpha=235,
        glow_color=(56, 189, 248), glow_blur=8, glow_alpha=125
    )
    # Exact Hung `Hook_1.8s` dual-stack symmetry: Giant `Smooch` `'C'` on left + stacked `'Mua'` over `Smooch` `'ăn hộ'` on right (`0px` overlap!)
    sp_anho = render_rich_sprite(
        "ăn hộ", FONT_SCRIPT, 88, ICE_CYAN,
        shadow_offset=(2, 3), shadow_blur=4, shadow_alpha=190,
        glow_color=(14, 165, 233), glow_blur=12, glow_alpha=235,
        glow2_color=(155, 242, 255), glow2_blur=4, glow2_alpha=195
    )
    target_C_h = int(round(sp_mua.ink_h + 2.0 + sp_anho.ink_h + 14.0))
    sz_C = match_font_size_to_height(FONT_SCRIPT, "C", target_C_h, min_size=120, max_size=220)
    sp_C = render_rich_sprite(
        "C", FONT_SCRIPT, sz_C, ICE_CYAN,
        shadow_offset=(2, 3), shadow_blur=4, shadow_alpha=190,
        glow_color=(14, 165, 233), glow_blur=13, glow_alpha=235,
        glow2_color=(155, 242, 255), glow2_blur=4, glow2_alpha=195
    )
    sp_tang = render_rich_sprite(
        "tặng", FONT_APTIMA_IT, 46, PURE_WHITE,
        shadow_offset=(3, 4), shadow_blur=4, shadow_alpha=235,
        glow_color=(56, 189, 248), glow_blur=8, glow_alpha=125
    )
    sp_doxe = render_rich_sprite(
        "ĐỖ XE", FONT_ANTON, 82, GOLD_METALLIC,
        shadow_offset=(3, 4), shadow_blur=4, shadow_alpha=220,
        glow_color=(245, 178, 22), glow_blur=9, glow_alpha=95,
        sparkle=True
    )

    # Exact Hung `11 | hơn / TỶ` height-lock using `FONT_ANTON` (`tặng` tucked tightly above `ĐỖ XE`, `SLOT` matching total height!)
    gap_notch = -8.0  # Compensates for `Ỗ` accent height so `tặng` kisses cleanly `4px` above `Đ, X, E`!
    target_slot_h = int(round(sp_tang.ink_h + gap_notch + sp_doxe.ink_h))
    sz_slot = match_font_size_to_height(FONT_ANTON, "SLOT", target_slot_h, min_size=90, max_size=195)
    sp_slot = render_rich_sprite(
        "SLOT", FONT_ANTON, sz_slot, GOLD_METALLIC,
        shadow_offset=(4, 5), shadow_blur=5, shadow_alpha=225,
        glow_color=(245, 178, 22), glow_blur=10, glow_alpha=105,
        sparkle=True
    )

    col_gap = 10.0
    hero_total_w = sp_slot.ink_w + col_gap + sp_doxe.ink_w

    sz_oto = match_font_size_to_width(FONT_BEBAS, "Ô TÔ ĐỊNH DANH", hero_total_w, min_size=46, max_size=88)
    sp_oto = render_rich_sprite(
        "Ô TÔ ĐỊNH DANH", FONT_BEBAS, sz_oto, GOLD_METALLIC,
        shadow_offset=(3, 4), shadow_blur=4, shadow_alpha=215,
        glow_color=(245, 178, 22), glow_blur=8, glow_alpha=85,
        sparkle=True
    )

    x_left = 54.0
    x_right = x_left + hero_total_w

    slot_cy = float(H * 0.525)
    slot_top = slot_cy - sp_slot.ink_h * 0.5
    slot_bot = slot_cy + sp_slot.ink_h * 0.5
    slot_cx  = x_left + sp_slot.ink_w * 0.5

    doxe_cx  = x_right - sp_doxe.ink_w * 0.5
    doxe_cy  = slot_bot - sp_doxe.ink_h * 0.5

    tang_cx  = doxe_cx + 2.0
    tang_cy  = slot_top + sp_tang.ink_h * 0.5

    # Giant `Smooch` `'C'` sweeps down-left beside `'SLOT'` top while `'Mua'` sits cleanly `4px` above `'ăn hộ'` (`0px` overlap!)
    anho_bot = slot_top - 4.0
    anho_cy  = anho_bot - sp_anho.ink_h * 0.5
    anho_top = anho_cy - sp_anho.ink_h * 0.5

    C_cx     = x_left - 12.0 + sp_C.ink_w * 0.5
    anho_cx  = (C_cx + sp_C.ink_w * 0.5 - 16.0) + sp_anho.ink_w * 0.5

    mua_bot  = anho_top - 3.0
    mua_cy   = mua_bot - sp_mua.ink_h * 0.5
    mua_cx   = anho_cx + 2.0
    C_cy     = (mua_cy - sp_mua.ink_h * 0.5) + sp_C.ink_h * 0.5 - 2.0

    # Tight optical gap to bottom Gold bar `"Ô TÔ ĐỊNH DANH"` (compensating `Ô` accent)
    oto_top  = slot_bot + 2.0
    oto_cy   = oto_top + sp_oto.ink_h * 0.5
    oto_cx   = x_left + hero_total_w * 0.5

    paste_animated_piece(bgr, sp_mua,  mua_cx,  mua_cy,  age_f, rem_f, delay_f=0,  in_f=15, out_f=6, style="mask_rise_up")
    paste_animated_piece(bgr, sp_C,    C_cx,    C_cy,    age_f, rem_f, delay_f=14, in_f=15, out_f=6, style="brush_wipe_lr")
    paste_animated_piece(bgr, sp_anho, anho_cx, anho_cy, age_f, rem_f, delay_f=17, in_f=16, out_f=6, style="brush_wipe_lr")
    paste_animated_piece(bgr, sp_tang, tang_cx, tang_cy, age_f, rem_f, delay_f=29, in_f=15, out_f=6, style="glide_side_mask", slide_dir=1)
    paste_animated_piece(bgr, sp_slot, slot_cx, slot_cy, age_f, rem_f, delay_f=50, in_f=17, out_f=6, style="pop_3d_depth")
    paste_animated_piece(bgr, sp_doxe, doxe_cx, doxe_cy, age_f, rem_f, delay_f=53, in_f=16, out_f=6, style="glide_side_mask", slide_dir=1)
    paste_animated_piece(bgr, sp_oto,  oto_cx,  oto_cy,  age_f, rem_f, delay_f=56, in_f=16, out_f=6, style="mask_rise_up")
    return bgr


def draw_question_wordplay_p1(bgr, age_f, rem_f):
    """2-Color KeyText Question in P1 (`4.04s - 6.00s`) with tight `5px` reference line spacing & `out_f=6`."""
    fade_sc = ease_in_out_cubic(min(1.0, (age_f + 1) / 12.0)) * ease_in_out_cubic(min(1.0, max(0.0, float(rem_f) / 6.0)))
    cy = int(H * 0.765)
    apply_soft_spot_scrim(bgr, W // 2, cy, rx=445, ry=140, strength=0.44 * fade_sc)

    sp_q1 = render_rich_sprite(
        "Anh chị có", FONT_APTIMA_IT, 54, PURE_WHITE,
        shadow_offset=(3, 4), shadow_blur=4, shadow_alpha=230,
        glow_color=(56, 189, 248), glow_blur=9, glow_alpha=165
    )
    sp_q2 = render_rich_sprite(
        "TIN ĐƯỢC KHÔNG ?", FONT_BEBAS, 108, GOLD_METALLIC,
        shadow_offset=(4, 5), shadow_blur=5, shadow_alpha=225,
        glow_color=(245, 178, 22), glow_blur=11, glow_alpha=115,
        sparkle=True
    )

    q2_cx = W * 0.5 + 14.0
    q2_cy = cy + 20.0
    q1_cx = (q2_cx - sp_q2.ink_w * 0.5) + sp_q1.ink_w * 0.5
    q1_cy = q2_cy - sp_q2.ink_h * 0.5 + 4.0 - sp_q1.ink_h * 0.5

    paste_animated_piece(bgr, sp_q1, q1_cx, q1_cy, age_f, rem_f, delay_f=0,  in_f=14, out_f=6, style="focus_rack_in")
    paste_animated_piece(bgr, sp_q2, q2_cx, q2_cy, age_f, rem_f, delay_f=16, in_f=16, out_f=6, style="pop_3d_depth")
    return bgr


def draw_chest_wordplay_p5(bgr, age_f, rem_f, cy_norm=0.668):
    """
    1:1 Pixel Twin of Hung's Mid-Chest KeyText (`Chest_61.8s` `Gia đình mình / SẼ NHƯ THẾ NÀO / Trong 10 NĂM TỚI?` — L14, L15, L17, L18):
      - Compensates for Vietnamese diacritic tips (`Ỗ, Ể`) & Script descenders (`p, g`) so the TRUE cap-to-cap
        optical line spacing is tight (`4px`) like `Chest_61.8s`!
    """
    fade_scrim = ease_in_out_cubic(min(1.0, (age_f + 1) / 14.0)) * ease_in_out_cubic(min(1.0, max(0.0, float(rem_f) / 6.0)))
    cy = int(H * cy_norm)
    apply_soft_spot_scrim(bgr, W // 2, cy, rx=465, ry=195, strength=0.48 * fade_scrim)

    sp_lead = render_rich_sprite(
        "Nhìn rõ tên văn bản", FONT_APTIMA_REG, 58, PURE_WHITE,
        shadow_offset=(3, 4), shadow_blur=4, shadow_alpha=230,
        glow_color=(56, 189, 248), glow_blur=10, glow_alpha=175
    )
    sp_hd = render_rich_sprite(
        "Hợp đồng", FONT_SCRIPT, 116, ICE_CYAN,
        shadow_offset=(2, 3), shadow_blur=4, shadow_alpha=195,
        glow_color=(14, 165, 233), glow_blur=12, glow_alpha=235,
        glow2_color=(150, 242, 255), glow2_blur=4, glow2_alpha=195
    )
    sp_mb = render_rich_sprite(
        "MUA BÁN", FONT_BEBAS, 130, OCEAN_SKY_BLUE,
        shadow_offset=(3, 4), shadow_blur=5, shadow_alpha=225,
        glow_color=(38, 168, 245), glow_blur=10, glow_alpha=125,
        bevel_3d=True, bevel_color=(225, 248, 255, 150)
    )
    sp_cdx = render_rich_sprite(
        "CHỖ ĐỂ XE", FONT_BEBAS, 148, SUNSET_GOLD,
        shadow_offset=(4, 5), shadow_blur=5, shadow_alpha=230,
        glow_color=(245, 172, 18), glow_blur=11, glow_alpha=120,
        bevel_3d=True, bevel_color=(255, 252, 220, 150), sparkle=True
    )

    pair_gap = 14.0
    row_mid_w = sp_hd.ink_w + pair_gap + sp_mb.ink_w
    x_row_left = W * 0.5 - row_mid_w * 0.5
    x_row_right = x_row_left + row_mid_w

    # Anchor off `sp_mb` cap height and tuck `Ỗ, Ể` accents cleanly under `MUA BÁN` (`gap23 = -10px` on ink bbox = `4px` cap-to-accent gap!)
    mb_h = sp_mb.ink_h
    gap12 = -2.0
    gap23 = -10.0

    tot_h = sp_lead.ink_h + gap12 + mb_h + gap23 + sp_cdx.ink_h
    y_top0 = float(cy) - tot_h * 0.5

    lead_cy = y_top0 + sp_lead.ink_h * 0.5
    lead_cx = x_row_left + 44.0 + sp_lead.ink_w * 0.5

    mid_cy  = y_top0 + sp_lead.ink_h + gap12 + mb_h * 0.5
    hd_cx   = x_row_left + sp_hd.ink_w * 0.5
    mb_cx   = x_row_right - sp_mb.ink_w * 0.5

    cdx_cy  = y_top0 + sp_lead.ink_h + gap12 + mb_h + gap23 + sp_cdx.ink_h * 0.5
    cdx_cx  = x_row_right - sp_cdx.ink_w * 0.5 - 4.0

    paste_animated_piece(bgr, sp_lead, lead_cx, lead_cy,     age_f, rem_f, delay_f=0,  in_f=15, out_f=6, style="mask_rise_up")
    paste_animated_piece(bgr, sp_hd,   hd_cx,   mid_cy + 2,  age_f, rem_f, delay_f=24, in_f=16, out_f=6, style="brush_wipe_lr")
    paste_animated_piece(bgr, sp_mb,   mb_cx,   mid_cy,      age_f, rem_f, delay_f=29, in_f=16, out_f=6, style="glide_side_mask", slide_dir=1)
    paste_animated_piece(bgr, sp_cdx,  cdx_cx,  cdx_cy,      age_f, rem_f, delay_f=44, in_f=17, out_f=6, style="pop_3d_depth")
    return bgr


def draw_podium_wordplay_p8a(bgr, age_f, rem_f, cy_norm=0.775):
    """
    1:1 Clean Champagne-Gold Hero Lockup (`Hook2_4.5s` `3 | ĐIỀU / NÀY` + `3_GoldHero_37.6s` `1140 / CHỖ ĐỖ XE` — L17, L18):
      - Clean flat-face Gold & Champagne (`0px` heavy brown extrusion!), tight `7px` & `10px` optical gaps!
      - 2 crisp beats (`4 TẦNG ĐỖ XE NỔI` -> `TỪ TẦNG 1 ĐẾN TẦNG 4`) + generous solid hold (`out_f = 6`).
    """
    fade_sc = ease_in_out_cubic(min(1.0, (age_f + 1) / 14.0)) * ease_in_out_cubic(min(1.0, max(0.0, float(rem_f) / 6.0)))
    cy = int(H * cy_norm)
    apply_soft_spot_scrim(bgr, W // 2, cy, rx=445, ry=200, strength=0.42 * fade_sc)

    sp_tang = render_rich_sprite(
        "TẦNG", FONT_BEBAS, 102, CHAMPAGNE,
        shadow_offset=(3, 4), shadow_blur=4, shadow_alpha=215,
        glow_color=(245, 204, 98), glow_blur=10, glow_alpha=115
    )
    sp_dxn = render_rich_sprite(
        "ĐỖ XE NỔI", FONT_BEBAS, 88, CREAM_TO_GOLD,
        shadow_offset=(3, 4), shadow_blur=4, shadow_alpha=215,
        glow_color=(245, 204, 98), glow_blur=10, glow_alpha=110
    )

    gap_r = 7.0  # Tight 7px reference stack gap!
    right_h = sp_tang.ink_h + gap_r + sp_dxn.ink_h
    right_w = max(sp_tang.ink_w, sp_dxn.ink_w)

    sz_4 = match_font_size_to_height(FONT_ANTON, "4", int(round(right_h)), min_size=120, max_size=260)
    sp_4 = render_rich_sprite(
        "4", FONT_ANTON, sz_4, GOLD_METALLIC,
        shadow_offset=(4, 5), shadow_blur=5, shadow_alpha=225,
        glow_color=(245, 185, 28), glow_blur=12, glow_alpha=125,
        sparkle=True
    )

    col_gap = 18.0
    top_w = sp_4.ink_w + col_gap + right_w
    _, sz_sub = fit_font(FONT_TRAJAN, "TỪ TẦNG 1 ĐẾN TẦNG 4", 50, int(W * 0.84))
    sp_sub = render_rich_sprite(
        "TỪ TẦNG 1 ĐẾN TẦNG 4", FONT_TRAJAN, sz_sub, CHAMPAGNE,
        shadow_offset=(3, 4), shadow_blur=4, shadow_alpha=215,
        glow_color=(245, 204, 98), glow_blur=9, glow_alpha=120
    )

    gap_ped = 11.0
    tot_h = right_h + gap_ped + sp_sub.ink_h
    top_y0 = float(cy) - tot_h * 0.5

    x0 = W * 0.5 - top_w * 0.5
    c4_x = x0 + sp_4.ink_w * 0.5
    c4_y = top_y0 + right_h * 0.5

    rx_left = x0 + sp_4.ink_w + col_gap
    tang_cx = rx_left + sp_tang.ink_w * 0.5
    tang_cy = top_y0 + sp_tang.ink_h * 0.5

    dxn_cx  = rx_left + sp_dxn.ink_w * 0.5
    dxn_cy  = top_y0 + right_h - sp_dxn.ink_h * 0.5

    sub_cx  = W * 0.5
    sub_cy  = top_y0 + right_h + gap_ped + sp_sub.ink_h * 0.5

    paste_animated_piece(bgr, sp_4,    c4_x,    c4_y,    age_f, rem_f, delay_f=0,  in_f=16, out_f=6, style="pop_3d_depth")
    paste_animated_piece(bgr, sp_tang, tang_cx, tang_cy, age_f, rem_f, delay_f=4,  in_f=15, out_f=6, style="glide_side_mask", slide_dir=1)
    paste_animated_piece(bgr, sp_dxn,  dxn_cx,  dxn_cy,  age_f, rem_f, delay_f=8,  in_f=15, out_f=6, style="glide_side_mask", slide_dir=1)
    paste_animated_piece(bgr, sp_sub,  sub_cx,  sub_cy,  age_f, rem_f, delay_f=22, in_f=16, out_f=6, style="mask_rise_up")
    return bgr


def draw_dual_wall_3d_callout(
    bgr, age_f, rem_f,
    left_top="VỊ TRÍ", left_big="ĐỖ XE",
    right_top="LỐI TỚI", right_big="THANG MÁY",
    d_right=22, total_hold_f=98
):
    """
    1:1 Camera-Tracked 3D Corridor Dual-Wall Callout (`CorrL_49.6s` & `CorrR_49.6s` — Locked Rule L17):
      - Bold architectural `UTM Bebas` proportions (`~360px` tall left wall slab, `~285px` tall right wall slab),
        tight `9px` row gap, subtle `6px` warm-taupe/charcoal 3D bevel + tight wall contact shadow!
      - Smooth Camera Forward-Walk Wall Tracking along `DJI_0148` (`14.35s -> 18.75s`).
    """
    prog_walk = max(0.0, min(1.0, float(age_f) / float(max(1, total_hold_f))))
    walk_ease = 0.45 * ease_in_out_sine(prog_walk) + 0.55 * prog_walk

    # Placed cleanly in the upper corridor wall (`ly = 562px`) so bottom of `ĐỖ XE` clears presenter's head by >70px (L2 Face-Safe)!
    lx = 222.0 - 24.0 * walk_ease
    ly = 562.0 - 10.0 * walk_ease
    l_scale = 0.95 + 0.09 * walk_ease

    fade_l = ease_in_out_cubic(min(1.0, (age_f + 1) / 15.0)) * ease_in_out_cubic(min(1.0, max(0.0, float(rem_f) / 6.0)))
    apply_soft_spot_scrim(bgr, lx, ly, rx=165, ry=195, strength=0.22 * fade_l)

    sp_left_3d = render_3d_corridor_wall_slab(
        left_top, left_big, side="left", flat_w=272, top_scale=1.18, bot_scale=1.36, bevel_px=6
    )
    paste_animated_piece(
        bgr, sp_left_3d, lx, ly, age_f, rem_f,
        delay_f=0, in_f=18, out_f=6, style="wall_3d_glide",
        vp_vec=(32.0, 8.0), base_scale=l_scale
    )

    if age_f >= d_right:
        rx = 858.0 + 20.0 * walk_ease
        ry = 695.0 - 8.0 * walk_ease
        r_scale = 0.95 + 0.09 * walk_ease

        fade_r = ease_in_out_cubic(min(1.0, (age_f - d_right + 1) / 15.0)) * ease_in_out_cubic(min(1.0, max(0.0, float(rem_f) / 6.0)))
        apply_soft_spot_scrim(bgr, rx, ry, rx=160, ry=175, strength=0.20 * fade_r)
        sp_right_3d = render_3d_corridor_wall_slab(
            right_top, right_big, side="right", flat_w=274, top_scale=1.18, bot_scale=1.22, bevel_px=6
        )
        paste_animated_piece(
            bgr, sp_right_3d, rx, ry, age_f, rem_f,
            delay_f=d_right, in_f=18, out_f=6, style="wall_3d_glide",
            vp_vec=(-28.0, 8.0), base_scale=r_scale
        )
    return bgr


def draw_corridor_keytext_p8c(bgr, age_f, rem_f, cy_norm=0.772):
    """
    Harmonious Multi-Color 2D KeyText Wordplay Lockup for Corridor Scene P8C (Locked Rule L22):
      - Replaces non-symmetric 3D wall blocks with the signature luxury KeyText language of P1 & P5:
          Row 1 (`UTM Aptima` 54pt Pure White + soft Cyan glow):  "Khi chọn căn — cùng xem rõ"
          Row 2 (`GreatVibes` Silky Cyan Calligraphy + `UTM Bebas` 134pt Ocean-Sky-Blue): "Vị trí" + "ĐỖ XE"
          Row 3 (`UTM Bebas` 122pt Metallic Sunset-Gold + sparkle): "& LỐI TỚI THANG MÁY"
      - Speech-synced word-for-word to P8C voice ("Khi chọn căn..." -> "vị trí đỗ xe" -> "và lối di chuyển tới thang máy"),
        leaving the lit arch, presenter, and corridor perspective 100% clean & unobstructed!
    """
    fade_scrim = ease_in_out_cubic(min(1.0, (age_f + 1) / 14.0)) * ease_in_out_cubic(min(1.0, max(0.0, float(rem_f) / 6.0)))
    cy = int(H * cy_norm)
    apply_soft_spot_scrim(bgr, W // 2, cy, rx=475, ry=205, strength=0.54 * fade_scrim)

    sp_lead = render_rich_sprite(
        "Khi chọn căn, cùng xem rõ", FONT_APTIMA_REG, 54, PURE_WHITE,
        shadow_offset=(3, 4), shadow_blur=4, shadow_alpha=230,
        glow_color=(56, 189, 248), glow_blur=10, glow_alpha=170
    )
    sp_vt = render_rich_sprite(
        "Vị trí", FONT_GREATVIBES, 112, ICE_CYAN,
        shadow_offset=(2, 3), shadow_blur=4, shadow_alpha=185,
        glow_color=(14, 165, 233), glow_blur=11, glow_alpha=230,
        glow2_color=(160, 246, 255), glow2_blur=3, glow2_alpha=175,
        shear_x=-0.20
    )
    sp_dx = render_rich_sprite(
        "ĐỖ XE", FONT_BEBAS, 132, OCEAN_SKY_BLUE,
        shadow_offset=(3, 4), shadow_blur=5, shadow_alpha=225,
        glow_color=(38, 168, 245), glow_blur=10, glow_alpha=130,
        bevel_3d=True, bevel_color=(225, 248, 255, 150)
    )
    sp_lttm = render_rich_sprite(
        "& LỐI TỚI THANG MÁY", FONT_BEBAS, 118, SUNSET_GOLD,
        shadow_offset=(4, 5), shadow_blur=5, shadow_alpha=230,
        glow_color=(245, 172, 18), glow_blur=11, glow_alpha=125,
        bevel_3d=True, bevel_color=(255, 252, 220, 150), sparkle=True
    )

    pair_gap = 22.0
    row_mid_w = sp_vt.ink_w + pair_gap + sp_dx.ink_w
    x_mid_left = W * 0.5 - row_mid_w * 0.5

    lead_top = float(cy) - 168.0
    lead_icy = lead_top + sp_lead.ink_h * 0.5
    lead_icx = W * 0.5

    dx_cap_top = lead_top + sp_lead.ink_h + 12.0
    dx_icy = dx_cap_top + (sp_dx.ink_cy - sp_dx.cap_y0)
    dx_base = dx_cap_top + sp_dx.cap_h

    vt_icy = (dx_base - 8.0) + (sp_vt.ink_cy - sp_vt.cap_y1)
    vt_icx = x_mid_left + sp_vt.ink_w * 0.5
    dx_icx = x_mid_left + sp_vt.ink_w + pair_gap + sp_dx.ink_w * 0.5

    lttm_cap_top = dx_base + 22.0
    lttm_icy = lttm_cap_top + (sp_lttm.ink_cy - sp_lttm.cap_y0)
    lttm_icx = W * 0.5

    paste_animated_piece(bgr, sp_lead, lead_icx, lead_icy, age_f, rem_f, delay_f=2,  in_f=15, out_f=6, style="mask_rise_up")
    paste_animated_piece(bgr, sp_vt,   vt_icx,   vt_icy,   age_f, rem_f, delay_f=48, in_f=16, out_f=6, style="brush_wipe_lr")
    paste_animated_piece(bgr, sp_dx,   dx_icx,   dx_icy,   age_f, rem_f, delay_f=53, in_f=16, out_f=6, style="glide_side_mask", slide_dir=1)
    paste_animated_piece(bgr, sp_lttm, lttm_icx, lttm_icy, age_f, rem_f, delay_f=78, in_f=17, out_f=6, style="pop_3d_depth")
    return bgr


# ==============================================================================
# 6. ARCHETYPE C & D — COHESIVE SINGLE-LINE B-ROLL CAPTIONS, 2-COLOR QUESTION & CTA (L14–L18)
# ==============================================================================
def draw_minimal_broll_caption(bgr, age_f, rem_f, text, cy_norm=0.755, style="focus_rack_in", out_f=6):
    """
    Complete Cohesive Single-Line B-Roll Caption (Locked Rules L14 & L15):
    Appears smoothly as ONE whole readable line right from the start of the shot and holds until final `6f`!
    """
    _, sz = fit_font(FONT_APTIMA_IT, text, 47, int(W * 0.88))
    sp = render_rich_sprite(text, FONT_APTIMA_IT, sz, PURE_WHITE, shadow_offset=(3, 4), shadow_blur=2, shadow_alpha=230)
    return paste_animated_piece(bgr, sp, W * 0.5, H * cy_norm, age_f, rem_f, delay_f=0, in_f=16, out_f=out_f, style=style)


def draw_progressive_broll_caption(bgr, age_f, rem_f, parts_spec, cy_norm=0.755, out_f=6):
    """Kept as clean cohesive full-line wrapper per Locked Rule L14 (no choppy multi-part B-Roll splitting!)."""
    if not parts_spec:
        return bgr
    full_str = " ".join(p[0] for p in parts_spec)
    return draw_minimal_broll_caption(bgr, age_f, rem_f, full_str, cy_norm=cy_norm, style="focus_rack_in", out_f=out_f)


def draw_top_question_wordplay(bgr, age_f, rem_f, line1_white, line2_gold, d_l2=15, cy_norm=0.205, out_f=6):
    """
    2-Color KeyText Top Question Lockup (`P2B` `XE CỦA MÌNH / SẼ ĐỖ Ở ĐÂU ?` — L14, L15, L17, L18):
    Clean flat-face White + Gold `UTM Bebas`, tight `6px` reference optical gap, holds solid until final `6f`!
    """
    fade_sc = ease_in_out_cubic(min(1.0, (age_f + 1) / 14.0)) * ease_in_out_cubic(min(1.0, max(0.0, float(rem_f) / float(max(1, out_f)))))
    cy = int(H * cy_norm)
    apply_soft_spot_scrim(bgr, W // 2, cy, rx=455, ry=130, strength=0.40 * fade_sc)

    sp1 = render_rich_sprite(
        line1_white, FONT_BEBAS, 76, PURE_WHITE,
        shadow_offset=(3, 4), shadow_blur=4, shadow_alpha=230,
        glow_color=(56, 189, 248), glow_blur=10, glow_alpha=155
    )
    sp2 = render_rich_sprite(
        line2_gold, FONT_BEBAS, 102, GOLD_METALLIC,
        shadow_offset=(4, 5), shadow_blur=5, shadow_alpha=230,
        glow_color=(245, 178, 22), glow_blur=11, glow_alpha=120,
        sparkle=True
    )

    gap = 6.0  # Tight 6px Hung optical gap!
    tot_h = sp1.ink_h + gap + sp2.ink_h
    y1 = cy - tot_h * 0.5 + sp1.ink_h * 0.5
    y2 = y1 + sp1.ink_h * 0.5 + gap + sp2.ink_h * 0.5

    x2 = W * 0.5 + 10.0
    x1 = (x2 - sp2.ink_w * 0.5) + sp1.ink_w * 0.5

    paste_animated_piece(bgr, sp1, x1, y1, age_f, rem_f, delay_f=0,    in_f=15, out_f=out_f, style="mask_rise_up")
    paste_animated_piece(bgr, sp2, x2, y2, age_f, rem_f, delay_f=d_l2, in_f=16, out_f=out_f, style="pop_3d_depth")
    return bgr


def draw_cta_wordplay_p9b(bgr, age_f, rem_f, cy_norm=0.760):
    """
    1:1 Clean Reference CTA KeyText (`6_CTA_66.2s` — Locked Rules L14, L15, L17, L18):
      - Clean flat-face Gold Hotline `0986.254.566` (`0px` heavy brown extrusion!), tight `7px` optical line spacing!
      - 3 clean color beats synced to P9B speech, holding 100% solid right up to `out_f = 6` (`> 2.5s - 4.2s` hold!).
    """
    fade_sc = ease_in_out_cubic(min(1.0, (age_f + 1) / 14.0)) * ease_in_out_cubic(min(1.0, max(0.0, float(rem_f) / 6.0)))
    cy = int(H * cy_norm)
    apply_soft_spot_scrim(bgr, W // 2, cy, rx=475, ry=205, strength=0.46 * fade_sc)

    sp_sc = render_rich_sprite(
        "Làm rõ điều khoản", FONT_SCRIPT, 82, ICE_CYAN,
        shadow_offset=(2, 3), shadow_blur=4, shadow_alpha=195,
        glow_color=(14, 165, 233), glow_blur=11, glow_alpha=225,
        glow2_color=(145, 240, 255), glow2_blur=3, glow2_alpha=185
    )
    sp_bl = render_rich_sprite(
        "& CHỌN PHƯƠNG ÁN", FONT_BEBAS, 76, OCEAN_SKY_BLUE,
        shadow_offset=(3, 4), shadow_blur=4, shadow_alpha=225,
        glow_color=(38, 168, 245), glow_blur=10, glow_alpha=130,
        bevel_3d=True, bevel_color=(228, 248, 255, 150)
    )
    sp_ph = render_rich_sprite(
        "0986.254.566", FONT_ANTON, 122, SUNSET_GOLD,
        shadow_offset=(4, 5), shadow_blur=5, shadow_alpha=230,
        glow_color=(245, 168, 20), glow_blur=12, glow_alpha=125,
        sparkle=True
    )
    sp_sub = render_rich_sprite(
        "Nguyễn Nam - Tư vấn trực tiếp", FONT_APTIMA_IT, 46, PURE_WHITE,
        shadow_offset=(3, 4), shadow_blur=3, shadow_alpha=230
    )

    top_gap = 14.0
    top_w = sp_sc.ink_w + top_gap + sp_bl.ink_w
    top_x0 = W * 0.5 - top_w * 0.5
    top_h = max(sp_sc.ink_h, sp_bl.ink_h)

    gap12 = 7.0  # Tight 7px reference CTA optical gap!
    gap23 = 8.0
    tot_h = top_h + gap12 + sp_ph.ink_h + gap23 + sp_sub.ink_h
    y_top0 = float(cy) - tot_h * 0.5

    top_cy = y_top0 + top_h * 0.5
    ph_cy  = y_top0 + top_h + gap12 + sp_ph.ink_h * 0.5
    sub_cy = y_top0 + top_h + gap12 + sp_ph.ink_h + gap23 + sp_sub.ink_h * 0.5

    sc_cx = top_x0 + sp_sc.ink_w * 0.5
    bl_cx = top_x0 + sp_sc.ink_w + top_gap + sp_bl.ink_w * 0.5

    paste_animated_piece(bgr, sp_ph,  W * 0.5, ph_cy,      age_f, rem_f, delay_f=2,  in_f=17, out_f=6, style="pop_3d_depth")
    paste_animated_piece(bgr, sp_sub, W * 0.5, sub_cy,     age_f, rem_f, delay_f=10, in_f=16, out_f=6, style="mask_rise_up")
    paste_animated_piece(bgr, sp_sc,  sc_cx,   top_cy + 2, age_f, rem_f, delay_f=28, in_f=16, out_f=6, style="brush_wipe_lr")
    paste_animated_piece(bgr, sp_bl,  bl_cx,   top_cy,     age_f, rem_f, delay_f=56, in_f=16, out_f=6, style="glide_side_mask", slide_dir=1)
    return bgr


draw_hook_left_cluster = draw_hook_wordplay_p1
draw_chest_sticker_cluster = draw_chest_wordplay_p5
draw_dual_wall_callout = draw_dual_wall_3d_callout
draw_luxury_gold_hero = draw_podium_wordplay_p8a
draw_cta_sticker = draw_cta_wordplay_p9b


# ==============================================================================
# 7. SIGNATURE TRANSITIONS (R16, R17)
# ==============================================================================
def apply_radial_zoom_blur(bgr, strength=0.18, steps=7):
    if strength <= 0.005:
        return bgr
    acc = bgr.astype(np.float32)
    for i in range(1, steps):
        s = 1.0 + strength * (i / float(steps))
        nw, nh = int(round(W * s)), int(round(H * s))
        up = cv2.resize(bgr, (nw, nh), interpolation=cv2.INTER_LINEAR)
        x0, y0 = (nw - W) // 2, (nh - H) // 2
        acc += up[y0:y0 + H, x0:x0 + W].astype(np.float32)
    return np.clip(acc / float(steps), 0, 255).astype(np.uint8)

def apply_double_light_leak(bgr, rel_idx):
    weights = {-4: 0.28, -3: 0.78, -2: 0.35, -1: 0.92, 0: 0.86, 1: 0.62, 2: 0.38, 3: 0.16, 4: 0.06}
    w = weights.get(rel_idx, 0.0)
    if w <= 0.01:
        return bgr
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    g1 = np.exp(-(((xx - W * 0.72) / (W * 0.65)) ** 2 + ((yy - H * 0.28) / (H * 0.55)) ** 2))
    g2 = np.exp(-(((xx - W * 0.22) / (W * 0.55)) ** 2 + ((yy - H * 0.75) / (H * 0.50)) ** 2))
    flare_i = np.clip((0.45 + 0.75 * g1 + 0.55 * g2) * w, 0.0, 1.0)[:, :, None]
    burn_bgr = np.array([120.0, 218.0, 255.0], dtype=np.float32)[None, None, :]
    f_img = bgr.astype(np.float32) / 255.0
    f_burn = (burn_bgr / 255.0) * flare_i
    screened = 1.0 - (1.0 - f_img) * (1.0 - f_burn)
    lifted = np.clip(screened + 0.22 * (w ** 2), 0.0, 1.0)
    return (lifted * 255.0).astype(np.uint8)

def apply_whip_blur(prev_bgr, next_bgr, prog_0_to_1, direction="vertical"):
    p = 0.5 - 0.5 * math.cos(math.pi * prog_0_to_1)
    if direction == "vertical":
        shift = int(round(H * p))
        comp = np.vstack([prev_bgr[shift:, :, :], next_bgr[:shift, :, :]]) if 0 < shift < H else (next_bgr if p >= 0.5 else prev_bgr)
        ksize = 45
        kernel = np.zeros((ksize, ksize), dtype=np.float32)
        kernel[:, ksize // 2] = 1.0 / ksize
    else:
        shift = int(round(W * p))
        comp = np.hstack([prev_bgr[:, shift:, :], next_bgr[:, :shift, :]]) if 0 < shift < W else (next_bgr if p >= 0.5 else prev_bgr)
        ksize = 45
        kernel = np.zeros((ksize, ksize), dtype=np.float32)
        kernel[ksize // 2, :] = 1.0 / ksize
    return cv2.filter2D(comp, -1, kernel)
