# QUY TRÌNH KỸ THUẬT & CẨM NANG VẬN HÀNH ENGINE (`concept-04-hung-anti`)

Tài liệu hướng dẫn chi tiết cách thiết lập và chạy bộ **Standalone Direct MP4 Engine** (`hung_engine.py`, `hung_gfx.py`, `hung_cards.py`, `qa_audit.py`) cho mọi dự án BĐS mới theo chuẩn **Concept 04 - Hung Anti** đã được Sếp duyệt đạt (`v8`).

---

## 1. Cấu trúc Thư mục Dự án Mới (Trong `4. WORK - CÔNG VIỆC`)

Khi triển khai dự án mới (ví dụ `4. WORK - CÔNG VIỆC/Marketing/<Ten_Du_An_Concept_04>`):

1. Tạo cấu trúc thư mục chuẩn:
   - `SOURCE/` — chứa các clip A-Roll quay dọc (DJI/Pocket 3) và file thu âm rời (`.wav`/`.mp3`) + kịch bản.
   - `03_ENGINE/` — copy toàn bộ `scripts/*.py` từ `SKILL_ROOT` sang đây (bộ font đã được tự động liên kết tới `SKILL_ROOT/assets/fonts/` hoặc copy thư mục `assets/fonts` thành `03_ENGINE/fonts`).
   - `04_OUTPUT/v1/` — chứa đầu ra `v1.mp4`, `QA_CONTACT_SHEET_v1.jpg`, `QA_KEY_TYPOGRAPHY_v1.jpg`, `v1_timeline_meta.json`.
2. Môi trường thực thi chuẩn trên máy Sếp:
   - Python: `& "C:\Users\NCPC\AppData\Local\Programs\Python\Python312\python.exe"`
   - Kho SFX: `C:\About Me\TÀI NGUYÊN DỰNG\SFX` (đặc biệt là `5. Sound Effect\Bộ Bảo Hay Dùng\theSOUNDS 1` & `theSOUNDS 2`).
   - Kho Nhạc nền: `C:\About Me\TÀI NGUYÊN DỰNG\NHẠC NỀN\02_LUXURY_AMBIENT_PIANO (Phong su Du an - Sa ban - Quang Son)`.

---

## 2. Quy trình 5 Bước Triển khai Thực Chiến

### Bước 1 — Bóc băng Word-Level (`faster-whisper`) & Đo Sóng Âm Cắt Thô (`R4`)
- Giải mã âm thanh sang `16kHz float32 numpy` qua FFmpeg pipe trước khi đưa vào `faster_whisper.WhisperModel("large-v3")` (tránh lỗi `PyAV metadata_errors` trên một số phiên bản thư viện).
- Xác định điểm `in_s` và số frame `n_frames` của từng phân đoạn thoại (`P1..Pn`) bằng cách kiểm tra kép:
  1. Mốc kết thúc từ cuối cùng trên kịch bản chữ.
  2. Mức năng lượng sóng âm thực tế rơi xuống `< -46 dBFS` cộng thêm đuôi ngân tự nhiên **`+100ms đến +140ms`** (`3–4 frames`) để tuyệt đối không bao giờ cắt cụt âm cuối.

### Bước 2 — Quy hoạch Phân Cảnh Hình Ảnh & Chuyển Động Sub-Pixel (`R13–R18`, `L10`)
- Phối hợp nhịp nhàng **~75% cảnh Full dọc `9:16`** (A-Roll reframed giữ tâm mặt `cy = 30%..36% H` + B-Roll dọc sắc nét) đan xen **~25% cảnh Chia Khung**:
  - `compose_split_50_50(top, bot, divider_px=4)`: dùng cho cặp Hợp đồng + Bảng mã căn (`P6B`), Nội thất trên/dưới (`P7C`), Đỗ xe nổi (`P8B`), Mặt bằng + Sảnh (`P9A`).
  - `compose_split_3tier(t1, t2, t3, divider_px=4)`: dùng cho đại cảnh Flycam ngang `16:9` (`P7B` Quy mô KĐT, `P7E` Hệ sinh thái tiện ích) — giúp giữ độ nét gốc 100%, không bị vỡ hạt do crop dọc quá sâu.
- Toàn bộ B-Roll và ảnh tĩnh bắt buộc trích xuất qua `extract_video_segment_frames` / `read_still_cropped` sử dụng **`2-Stage Sub-Pixel Keyframe Affine Warp`** (`cv2.warpAffine` `INTER_CUBIC | WARP_INVERSE_MAP`, đường cong `ease_in_out_sine` `1.00× -> 1.06×..1.08×`).

### Bước 3 — Thiết kế 5 Nhóm Đồ Họa Chữ Chuẩn Mẫu `v8` (`L1–L9`, `L13–L20`, `L22–L23`)
1. **Cụm `KeyText` Đa Màu Chơi Chữ Tự Do (`Hook P1`, `Mid-Chest P5`, `Number-Stack P8A`, `Corridor KeyText P8C`, `CTA P9B`):**
   - Áp dụng **hiện nối tiếp theo đúng từ khóa người nói phát âm** (`2–4` nhịp màu sắc nét, `in_f = 15..18f` `Ease-In-Out`), sau đó giữ đứng nét tối thiểu `1.4s – 2.5s` và chỉ thu `out_f = 6f` sát cuối cảnh (`L14, L15`).
   - Cảnh hành lang / nội thất góc xiên: dùng `draw_corridor_keytext_p8c` đặt ở `cy_norm = 0.772` thay vì dán chữ 3D lên tường (`L23`).
2. **Hộp Kính `Carbon Pill` (`draw_carbon_pill_overlay` — `884 × 196 px`, `cy_norm = 0.818`):**
   - Mở trọn vẹn cả hộp và 2 dòng chữ ngay từ đầu cảnh (`d_tag=2, d_l1=4, d_l2=7`, **cấm cắt nửa dòng `L16`**).
   - Neo cứng chân chữ `l1_base = y0 + 98`, `l2_base = y0 + 166` (`L20`).
3. **Hộp Kính Ô-Liu Giữa Đường Chia `50/50` (`draw_split_seam_pill` — `844 × 184 px`, `cy_norm = 0.50`):**
   - Chữ viết tay góc trái trên (`script_top`, ví dụ `"Đối chiếu"`, `"Căn"`) vẽ nguyên cụm liền mạch bằng **`GreatVibes-Regular.ttf`** nghiêng mềm `shear_x = -0.22` (`L22`), vươn nhẹ lên trên mép hộp `~48px` và cách đầu chữ vàng cột trái `12px`.
   - Cột trái chữ lớn (`4 MỤC`, `2-4PN`) cao thân chữ hoa `122px`; cột phải dòng 1 (`UTM Bebas` `88–96pt` trắng glow cyan) + dòng 2 ngoặc đơn (`UTM AptimaBoldItalic` `45–47pt` trắng tinh).
4. **Thẻ Hợp Đồng / Pháp Lý Thực Tế (`build_contract_p4_frames`, `build_contract_p6_top_frames`):**
   - Sáng từng điều khoản màu vàng kem ấm mượt mà (`14 frames` `Ease-In-Out`) khớp chính xác từng mốc đọc điều khoản trong lời thoại.
5. **Phụ đề B-Roll Đơn Sắc (`draw_minimal_broll_caption`):**
   - 1 dòng gọn gàng `UTM AptimaItalic` `47pt` trắng tinh + bóng đổ sắc `(3, 4) blur=2`, hiện nguyên câu bằng `focus_rack_in` ngay đầu cảnh và giữ đến `out_f = 6`.

### Bước 4 — Phối Âm 3 Stem + 50–60 SFX Studio + Dynamic BGM Ducking (`L21`)
- Chuẩn hóa giọng nói từng đoạn (`clean_and_level_voice`, lọc rumble `< 75–95Hz`, cân bằng giữa mic hiện trường DJI và thu âm phòng thu).
- Nén động nhạc nền Piano sang trọng (`-2.8 dB` mềm mại khi có giọng nói, mở thoáng ở khoảng nghỉ chuyển chương).
- Đặt **50–60 cue SFX không trùng file** (`assert spath not in used_sfx`) theo danh mục `assets/sfx-59-catalog.json`.
- Master cuối qua FFmpeg `loudnorm=I=-14.8:TP=-1.2:LRA=6.5` (`48.000 Hz Stereo`).

### Bước 5 — Xuất Master `.MP4` & Chạy Kiểm Định Tự Động (`qa_audit.py`)
```powershell
& "C:\Users\NCPC\AppData\Local\Programs\Python\Python312\python.exe" "03_ENGINE\hung_engine.py" --version v1
& "C:\Users\NCPC\AppData\Local\Programs\Python\Python312\python.exe" "03_ENGINE\qa_audit.py" --version v1
```
- Mở xem trực tiếp bằng mắt (`read_file`) cả `QA_KEY_TYPOGRAPHY_v1.jpg` (12 cụm chữ chủ đạo) và `QA_CONTACT_SHEET_v1.jpg` (24 frame toàn tuyến) trước khi bàn giao **Chờ duyệt** cho Sếp.

---

## 3. Các Bẫy Kỹ Thuật Bắt Buộc Tránh (`Critical Gotchas`)

1. **Bẫy Watermark Ẩn Trong `UTM Aptima.ttf` (`CỰC KỲ QUAN TRỌNG`):**
   - Trong bộ font `UTM Aptima.ttf`, ký tự gạch ngang dài Unicode em-dash `'—'` (`U+2014`) bị nhà thiết kế gắn thành một khối logo chữ bản quyền UTM nhiều dòng!
   - **Quy tắc bắt buộc:** Tuyệt đối chỉ dùng dấu phẩy `","` hoặc dấu gạch nối chuẩn ASCII `"-"` (`U+002D`) khi render bằng họ font `UTM Aptima`.
2. **Bẫy Dấu Nặng Tiếng Việt (`Ụ, Ợ, Ộ, Ệ`) Làm Nhảy Dòng Trong Hộp Kính:**
   - Không bao giờ căn vị trí dòng trong `Carbon Pill` hay `Split-Seam Olive Pill` theo trung tâm `ink_bbox` tổng, vì chữ có dấu nặng sẽ bị đẩy trồi lên trên `14–18px` đâm vào dòng trên.
   - Luôn luôn dùng thuộc tính `sp.cap_y0` (đỉnh thân chữ hoa không dấu) và `sp.cap_y1` (đường chân chữ `baseline`) đã có sẵn trong `RichSprite` của `hung_gfx.py`!
3. **Bẫy PowerShell Ăn Mất Dấu Ngoặc Kép `"` Trong `-c "..."`:**
   - Trên Windows PowerShell, ưu tiên viết script kiểm tra ngắn ra file `.py` trong thư mục `scratch/` thay vì truyền chuỗi phức tạp qua `python.exe -c`.
