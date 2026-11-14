# Concept 04 · Hung Anti (`concept-04-hung-anti`)

**Skill A.I dựng và xuất thẳng video Bất Động Sản cao cấp dọc `9:16` (`1080×1920 @ 30fps`)** bằng **Standalone Direct MP4 Engine** (`Python + Pillow 2x Supersampling + OpenCV Sub-Pixel Affine Warp + FFmpeg H.264/AAC`), không phụ thuộc CapCut PC hay DaVinci Resolve.

---

## Điểm nhấn kỹ thuật (`Master Spec v8` — 23 Locked Rules `L1–L23`)

1. **Bộ 13 Font chuẩn `1:1` đóng gói sẵn (`assets/fonts/`):**
   - `GreatVibes-Regular.ttf` (`2x` Supersampling, `shear_x = -0.22`) cho chữ viết tay mềm như lụa liền nét trong Box (`Đối chiếu`, `Căn`) và KeyText cảm xúc (`Vị trí`).
   - `Smooch-Regular.ttf`, `UTM Bebas.ttf`, `Anton-Regular.ttf`, `UTM Aptima` (`Regular / Italic / BoldItalic`), `UTM Trajan Pro Bold.ttf`, `Montserrat-ExtraBoldItalic.otf`, `GoogleSans`.
   - Khóa cứng `0px` viền chữ dày (`stroke_px = 0`); tạo chiều sâu bằng Gradient kim loại ánh kim (`SUNSET_GOLD` + `sparkle`), Xanh Đại Dương (`OCEAN_SKY_BLUE`), Xanh Băng (`ICE_CYAN`), vát sáng mảnh `bevel_3d` và bóng đổ định hướng.
2. **Nghệ thuật sắp đặt chữ & Hộp kính chuẩn tọa độ chân chữ (`cap_y0 / cap_y1`):**
   - **Cụm `KeyText` Đa Màu Chơi Chữ Bất Đối Xứng:** Hiện nối tiếp theo đúng mili-giây người nói phát âm từ khóa (`Hook`, `Mid-Chest`, `Number-Stack`, `Corridor KeyText`, `CTA`).
   - **Hộp kính `Carbon Pill` (`884 × 196 px`) & `Split-Seam Olive Box` (`844 × 184 px`):** Neo cứng theo `baseline` miễn nhiễm với dấu nặng tiếng Việt (`Ụ, Ợ, Ộ`), mở nguyên khối trọn vẹn ngay đầu cảnh và giữ chữ đứng nét lâu dễ đọc (`out_f = 6`).
   - **Thẻ Hợp đồng / Pháp lý trực quan:** Sáng từng điều khoản mượt mà theo giọng đọc.
3. **Chuyển động `2-Stage Sub-Pixel Keyframe Affine Warp` (`0%` giật cục):**
   - Toàn bộ B-Roll, ảnh tĩnh và A-Roll reframe quanh khuôn mặt được nội suy tọa độ thực `float32` qua `cv2.warpAffine(..., INTER_CUBIC | WARP_INVERSE_MAP)`.
4. **Thiết kế âm thanh 59 lớp SFX Studio & Dynamic BGM Ducking:**
   - Phối 50–60 hiệu ứng âm thanh độc bản không trùng lặp (*ShortRiser, Film Burn, Sunflare, Subtle/Slow Hit, Sun Ray, Pop Flash, Fabric/Magic Brush, Paper Foley, Ambience*), nén động nhạc nền `-2.8 dB` dưới lời thoại, chuẩn hóa EBU R128 đạt **`-14.8 LUFS` (`TP <= -1.2 dBTP`)**.

---

## Cấu trúc thư mục

```text
concept-04-hung-anti/
├── SKILL.md                       # Tài liệu điều phối trung tâm cho A.I Agent
├── concept.json                   # Metadata định danh Concept
├── studio.json                    # Cấu hình Engine xuất thẳng MP4 (1080x1920 @ 30fps)
├── assets/
│   ├── fonts/                     # Trọn bộ 13 file font chuẩn 1:1
│   └── sfx-59-catalog.json        # Danh mục 59 SFX phân theo 6 nhóm âm thanh
├── references/
│   ├── locked-rules.md            # Toàn bộ thông số nền R1–R22 & 23 Quy tắc khóa L1–L23
│   ├── workflow.md                # Quy trình 5 bước triển khai & các lưu ý kỹ thuật
│   └── dna-hung-anti.md           # Hồ sơ giải phẫu thông số gốc 4K
└── scripts/
    ├── hung_engine.py             # Engine điều phối timeline, trộn âm 3 stem & xuất MP4
    ├── hung_gfx.py                # Thư viện đồ họa Typography 2x Supersampling & Transitions
    ├── hung_cards.py              # Thư viện Sub-Pixel Warp, Split 50/50 & 3-Tier, Thẻ Hợp đồng
    └── qa_audit.py                # Kiểm định tự động ffprobe, ebur128, 12-frame Typography & Whisper
```

---

## Cài đặt nhanh cho A.I Agent (Antigravity / Codex / Claude Code)

Clone trực tiếp vào thư mục `skills` toàn cục của Agent:

```bash
git clone https://github.com/nusyco/concept-04-hung-anti.git ~/.gemini/config/skills/concept-04-hung-anti
```

Khi sử dụng, gọi trực tiếp tên Skill **`[concept-04-hung-anti]`** kèm đường dẫn thư mục footage & kịch bản dự án.
