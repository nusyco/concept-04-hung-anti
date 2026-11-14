---
name: concept-04-hung-anti
description: "Skill dựng và xuất thẳng video Bất Động Sản cao cấp dọc 9:16 30fps chuẩn Concept 04 - Hung Anti (mẫu chuẩn đã duyệt đạt: Le Parc Place - ParkCity Hanoi v8) bằng Standalone Direct MP4 Engine (Python + Pillow 2x Supersampling + OpenCV Sub-Pixel Affine Warp + FFmpeg H.264/AAC, không cần mở CapCut hay DaVinci Resolve). Khóa trọn bộ 23 quy tắc thực chiến (L1-L23): 0px viền chữ dày, bộ 13 font chuẩn 1:1 đi kèm (UTM Bebas, Anton, GreatVibes viết tay liền nét mềm như lụa trong Box, Smooch, UTM Aptima, Trajan, Montserrat), cụm KeyText đa màu chơi chữ bất đối xứng hiện đúng nhịp thoại (kể cả cảnh hành lang P8C), hộp kính Carbon Pill & Split-Seam Olive Box hiện trọn vẹn giữ chữ lâu dễ đọc (out_f=6), thẻ Hợp đồng phát sáng từng điều khoản, B-Roll Keyframe Zoom mượt tuyệt đối 0% giật cục, 59 SFX Studio độc bản (theSOUNDS 1 & 2) kèm nén nhạc nền động (-2.8 dB) đạt chuẩn -14.8 LUFS. Dùng ngay khi Sếp gọi [concept-04-hung-anti] / Concept 04 / mẫu Hung Anti."
---

# Concept 04 - Hung Anti (Luxury Real Estate Editorial 9:16 @ 30fps — Standalone Direct MP4)

Bộ Skill chuẩn hóa toàn diện quy trình dựng video ngắn Bất Động Sản hạng sang dọc `9:16` (`1080×1920 @ 30.00 fps`) của **Phòng Truyền thông Media – ABM**, được đúc kết từ quá trình giải phẫu mẫu 4K `Hung-Le-Parc-Place.mp4` và **8 vòng tinh chỉnh thực chiến (`v1 -> v8`) đã được Sếp Nguyễn Sỹ Cường chính thức xác nhận “Duyệt đạt” ngày `2026-11-14`**.

- **Dự án mẫu chuẩn đã duyệt đạt (`v8`):** Le Parc Place – ParkCity Hanoi (*Slot đỗ xe ô tô định danh & Hợp đồng mua bán chỗ để xe riêng*).
- **Lưu trữ thành phẩm chuẩn đã duyệt:** [2026-11-14_Le-Parc-Place_Slot-Do-Xe-Dinh-Danh_v8_DA-DUYET.mp4](file:///c:/HUB_NUSYCO_%20A.I_AGENT/6.%20OUTPUT%20-%20L%C6%AFU%20TR%E1%BB%AE%20TH%C3%80NH%20QU%E1%BA%A2/MEDIA/2026-11-14_Concept-04-Hung-Anti_Le-Parc-Place_DA-DUYET/2026-11-14_Le-Parc-Place_Slot-Do-Xe-Dinh-Danh_v8_DA-DUYET.mp4)
- **Chế độ vận hành mặc định:** **Standalone Direct `.MP4` Engine** (`scripts/hung_engine.py` + `hung_gfx.py` + `hung_cards.py` + `qa_audit.py`) — kết xuất thẳng file Master `.MP4` + Bảng QA 24 Frame + Bảng QA 12 Cụm Typography + Kiểm định lời thoại `faster-whisper`, **không phụ thuộc CapCut PC hay DaVinci Resolve**.

> **Tính độc lập của Concept:** Concept này sở hữu hệ nhận diện riêng biệt (KeyText chơi chữ lồng ghép đa màu không viền, hộp kính Carbon sọc chéo viền cyan, hộp kính Ô-liu chia đôi màn hình có chữ viết tay lụa `GreatVibes`, thẻ hợp đồng sáng dòng trực quan, chuyển cảnh Light-Leak kép & Whip-Blur). Không trộn lẫn quy tắc của `concept-01-bds`, `concept-01-tran-duc` hay `concept-02-lam-phat-long`.

---

## 1. Luôn Đọc Trước Khi Triển Khai

1. [references/locked-rules.md](references/locked-rules.md): **Toàn bộ 22 thông số nền (`R1–R22`) và 23 Quy tắc Khóa Thực Chiến (`L1–L23`, `v1 -> v8`)** của Sếp, kèm bảng tổng hợp hiệu lực cuối cùng ở đầu file.
2. [references/workflow.md](references/workflow.md): Quy trình 5 bước thiết lập dự án mới, cách cấu hình timeline/chữ/SFX trong `hung_engine.py`, và **3 bẫy kỹ thuật bắt buộc tránh**.
3. [references/dna-hung-anti.md](references/dna-hung-anti.md): Hồ sơ đo đạc thông số gốc từ mẫu tham chiếu 4K.
4. [assets/sfx-59-catalog.json](assets/sfx-59-catalog.json): Danh mục 59 file SFX Studio chuẩn phân theo 6 nhóm âm thanh từ `theSOUNDS 1 & 2`.

---

## 2. Hệ Quy Chuẩn Cốt Lõi Đã Khóa Cứng (`Master Spec v8` — Tổng Hợp `L1 -> L23`)

### Nhóm A — Bộ Font Chuẩn `1:1` Đi Kèm & Phong Cách Bề Mặt Chữ (`L1, L3, L17, L19, L22`)
Toàn bộ 13 file font chuẩn đã được đóng gói sẵn trong `assets/fonts/` (tự động nạp bởi `hung_gfx.py`):
1. **Cấm tuyệt đối viền chữ dày & khối 3D thô (`L3, L17`):** Khóa cứng `stroke_px = 0` và `extrude_3d_px = 0` trên toàn bộ chữ 2D màn hình; tuyệt đối không tự vẽ thêm khung nút phụ `[...]` hay đường gạch cánh `──✦` ngoài DNA mẫu (`L9`). Tạo độ sang trọng và tách nền bằng **Gradient Kim Loại Ánh Kim (`SUNSET_GOLD` + `sparkle`) / Xanh Đại Dương (`OCEAN_SKY_BLUE`) / Xanh Băng (`ICE_CYAN`) + Vát sáng mảnh `bevel_3d` + Quầng Glow dịu + Bóng đổ định hướng + Lớp `Soft Spot Scrim` êm phía sau**.
2. **Phân vai chính xác từng Font chữ (`L19, L22`):**
   - **`GreatVibes-Regular.ttf` (`shear_x = -0.22`, `2x` supersampled):** Chữ viết tay mềm mại liền nét như lụa cho góc trái hộp `Split-Seam Olive Box` (`"Đối chiếu"`, `"Căn"`) và chữ nhấn cảm xúc trong cụm KeyText hành lang (`"Vị trí"`). Kết xuất nguyên từ liền mạch, `condense_x = 1.0`, tuyệt đối không tách rời ký tự đầu (`L22`).
   - **`Smooch-Regular.ttf`:** Chữ cọ phóng khoáng cho cụm Hook mở màn (`"Căn hộ"`), cụm giữa ngực (`"Hợp đồng"`) và CTA (`"Làm rõ điều khoản"`).
   - **`UTM Bebas.ttf`:** Chữ không chân cao thanh thoát chủ lực cho các từ khóa lớn (`"MUA BÁN"`, `"CHỖ ĐỂ XE"`, `"4 MỤC"`, `"TRONG HỢP ĐỒNG"`, `"SLOT Ô TÔ ĐỊNH DANH"`, `"& LỐI TỚI THANG MÁY"`).
   - **`Anton-Regular.ttf`:** Chữ/Số siêu đậm tạo sức nặng thị giác cho từ khóa trụ cột (`"SLOT"`, con số `"4"`, Hotline `"0986.254.566"`).
   - **`UTM Aptima.ttf` / `UTM AptimaItalic.ttf` / `UTM AptimaBoldItalic.ttf`:** Chữ dẫn mở ý, phụ đề B-Roll (`AptimaItalic` `47pt`) và dòng ngoặc đơn trong hộp Ô-liu (`AptimaBoldItalic` `46pt`). *(Cảnh báo: Tuyệt đối KHÔNG dùng dấu gạch ngang dài Unicode `—` `U+2014` với `UTM Aptima` vì chứa watermark ẩn; chỉ dùng `,` hoặc `-` ASCII!)*
   - **`Montserrat-ExtraBoldItalic.otf` & `UTM Trajan Pro Bold.ttf`:** Nhãn chương góc trái trên hộp `Carbon Pill` và dòng chân đế cổ điển sang trọng (`"TỪ TẦNG 1 ĐẾN TẦNG 4"`).

### Nhóm B — Nghệ Thuật Chơi Chữ `KeyText` & Hộp Kính Chuẩn Tọa Độ Chân Chữ (`L2, L4, L6–L9, L13, L18, L20, L23`)
1. **Cụm `KeyText` Đa Màu Chơi Chữ Bất Đối Xứng (`L13, L18, L23`):**
   - **`Hook P1` (`draw_hook_wordplay_p1`):** Lồng ghép khít sát kiểu mảnh ghép Tetris (`"Mua"` nằm gọn trong hốc chữ `"C"` của `"Căn hộ"`, khối `"SLOT"` khóa chiều cao `1:1` với `[tặng + ĐỖ XE]`, đáy khóa bằng `"Ô TÔ ĐỊNH DANH"` dãn dòng khít `5px`, đặt lệch trục trái `cx ≈ 258px` né trọn người dẫn).
   - **`Mid-Chest P5` (`draw_chest_wordplay_p5`):** 3 tầng khít `4–5px` (`"Nhìn rõ tên văn bản"` trắng → `"Hợp đồng"` Script xanh băng + `"MUA BÁN"` xanh dương → `"CHỖ ĐỂ XE"` vàng kim lớn).
   - **`Number-Stack P8A` (`draw_podium_wordplay_p8a`):** Con số `"4"` khổng lồ khóa chiều cao `1:1` với 2 dòng `"TẦNG / ĐỖ XE NỔI"` bên phải, đặt trên đế `Trajan` Champagne.
   - **`Corridor / Interior KeyText P8C` (`draw_corridor_keytext_p8c` — `L23`):** Không dán chữ 3D lên vách tường nghiêng gây lệch kiến trúc; sử dụng cụm KeyText 3 tầng đa màu hài hòa ở `1/3` dưới (`cy_norm = 0.772`: Dòng dẫn trắng → Viết tay xanh băng `GreatVibes` + Xanh dương `UTM Bebas` → Vàng Gold `UTM Bebas`), giữ thoáng 100% vòm kiến trúc và khuôn mặt.
   - **`CTA P9B` (`draw_cta_wordplay_p9b`):** Ghép ngang `[Script xanh băng + Xanh dương]` phía trên Hotline Vàng kim `Anton` `122pt` và dòng tên chuyên viên trắng tinh bên dưới.
2. **Hộp Kính `Carbon Pill` (`draw_carbon_pill_overlay` — `L7, L8, L9, L20`):**
   - Kích thước **`884 × 196 px` (`R = 98px`, `cy_norm = 0.818`)**, nở đối xứng từ tâm `W // 2`; nền kính xám khói xuyên thấu (`alpha = 0.58`) có sọc chéo carbon `45°` và viền cyan `#8CF4EA` mảnh.
   - Nhãn chương (`ĐIỂM KHÁC BIỆT`, `HỆ SINH THÁI`...) đặt bên ngoài phía trên đoạn viền phẳng trái; chữ bên trong khóa gọn trong `Safe Flat Chord <= 660px` (`0%` tràn viền cong) và neo theo `baseline` cố định (`y0 + 98` & `y0 + 166`) miễn nhiễm với dấu nặng tiếng Việt.
3. **Hộp Kính Ô-Liu Giữa Đường Chia `50/50` (`draw_split_seam_pill` — `L20, L22`):**
   - Kích thước **`844 × 184 px` (`R = 92px`, `cy_norm = 0.50`)**, kính xanh rêu mờ không viền; cột trái chữ hoa cao `122px` vàng kem sáng + chữ viết tay `GreatVibes` xanh băng vươn mềm lên mép trên hộp `~48px` (hở `12px` trên chữ vàng); cách `40px` sang cột phải gồm tiêu đề `UTM Bebas` trắng glow cyan (`baseline = y0 + 88`) và dòng ngoặc đơn `UTM AptimaBoldItalic` `46pt` (`cap_top = y0 + 106`).

### Nhóm C — Nhịp Chuyển Động `Ease-In-Out`, Đồng Bộ Thoại Chọn Lọc & Lưu Chữ Đủ Đọc (`L5, L12, L14–L16`)
1. **Phân định rõ 2 cơ chế xuất hiện chữ (`L14, L16`):**
   - **Cụm `KeyText` Đa Màu Sắc:** Hiện nối tiếp từng mảng màu đúng mili-giây người nói phát âm từ khóa tương ứng (`2–4` nhịp gãy gọn), phối hợp linh hoạt 5 kiểu chuyển động `Ease-In-Out` (`brush_wipe_lr`, `mask_rise_up`, `pop_3d_depth`, `glide_side_mask`, `focus_rack_in`, thời lượng `15–18 frames`).
   - **Hộp `Carbon Pill`, Hộp `Split-Seam Olive Box` & Phụ đề B-Roll đơn sắc:** Hiện **nguyên khối 100% nội dung ngay từ đầu cảnh** (`0%` cắt vụn câu hay quét dừng nửa dòng gây khó chịu).
2. **Giữ chữ đứng nét lâu & thu `Out` gọn cuối cảnh (`L15`):**
   - Mọi cụm chữ sau khi hiện đủ phải **giữ tĩnh 100% tối thiểu `1.5s – 4.5s`** để người xem đọc và ngấm thông tin; chỉ thu mờ `Ease-Out` trong đúng **`6 frames` (`0.20s`)** sát điểm cắt cảnh.

### Nhóm D — Sub-Pixel Keyframe Zoom, Màu Tươi Sáng & Âm Thanh 59 SFX Studio (`R4, R16–R22, L10, L21`)
1. **B-Roll & A-Roll Mượt Tuyệt Đối (`L10`):** `100%` chuyển động phóng nhẹ (`1.00× -> 1.06×..1.08×`) thực thi bằng ma trận số thực `cv2.warpAffine(..., INTER_CUBIC | WARP_INVERSE_MAP)` kết hợp `EaseInOutSine` — triệt tiêu hoàn toàn hiện tượng giật `1px` của phép cắt mảng nguyên.
2. **Chuyển Cảnh & Màu Sắc (`R16–R22`):** Mở màn bằng `Radial Zoom-Blur (6f)`, chuyển chương bằng `Double Warm Light-Leak Flash (9f)` đan xen `Whip-Blur (6f)`, kết bằng `Black Brand Outro (2.8s)`; chỉnh màu sáng trong, da ấm hồng tự nhiên, cây xanh tươi mát (`High-Key Bright Fresh Grade`).
3. **Thiết Kế Âm Thanh Đa Lớp (`L21`):**
   - Cắt thô giọng nói trọn câu trọn chữ (`< -46 dBFS` + đuôi thở `100–140ms`).
   - Phối **50–60 file SFX độc bản không trùng lặp** từ bộ Studio `theSOUNDS 1 & 2` (`ShortRiser` + `Film Burn`/`Sunflare` cho Light-Leak, `Subtle/Slow Hit` + `Sun Ray` + `Pop Flash` cho chữ Gold, `Fabric/Magic` cho nét bút viết tay, `Paper Foley` cho cảnh hợp đồng, `Birds` nhẹ cho cảnh công viên).
   - Tự động **Dynamic BGM Ducking (`-2.8 dB` khi có lời thoại)** và chuẩn hóa EBU R128 đạt **`-14.8 LUFS` (`True Peak <= -1.2 dBTP`)**.

---

## 3. Quy Trình Vận Hành Nhanh Cho Dự Án Mới

1. **Khởi tạo:** Tạo thư mục dự án trong `4. WORK - CÔNG VIỆC/Marketing/<Ten_Du_An>/`, copy `scripts/*.py` từ Skill vào `03_ENGINE/`.
2. **Bóc băng & Lập bảng phân cảnh:** Chạy `faster-whisper` lấy word timestamps trên toàn bộ A-Roll & Voiceover, kiểm sóng âm cắt thô trọn chữ, và cập nhật `pieces_spec`, phân cảnh `P1..Pn` cùng bảng `sfx_cues` trong `03_ENGINE/hung_engine.py` theo hướng dẫn tại [references/workflow.md](references/workflow.md).
3. **Kết xuất & Kiểm định tự động:**
   ```powershell
   & "C:\Users\NCPC\AppData\Local\Programs\Python\Python312\python.exe" "03_ENGINE\hung_engine.py" --version v1
   & "C:\Users\NCPC\AppData\Local\Programs\Python\Python312\python.exe" "03_ENGINE\qa_audit.py" --version v1
   ```
4. **Duyệt mắt 100% trước khi bàn giao:** Kiểm tra trực tiếp bằng mắt (`read_file`) trên cả `QA_KEY_TYPOGRAPHY_v1.jpg` và `QA_CONTACT_SHEET_v1.jpg` đối chiếu đủ `L1–L23`. Gửi Sếp ở trạng thái **Chờ duyệt**; nếu Sếp góp ý thêm, cập nhật vào `locked-rules.md` của dự án trước rồi xuất sang `v2` (không ghi đè bản cũ).

---

## 4. Cấu Trúc Thư Mục Của Skill `[concept-04-hung-anti]`

| Đường dẫn | Vai trò |
| :--- | :--- |
| `SKILL.md` | Tài liệu điều phối trung tâm & tổng hợp chuẩn `Master Spec v8` (`L1–L23`) |
| `concept.json`, `studio.json` | Metadata định danh Skill & cấu hình Standalone Direct MP4 (`1080×1920 @ 30fps`) |
| `references/locked-rules.md` | Sổ tay đầy đủ `R1–R22` & lịch sử khóa cứng 7 vòng thực chiến `L1–L23` (`v1 -> v8`) |
| `references/workflow.md` | Hướng dẫn lập trình phân cảnh, phối âm 59 SFX & 3 bẫy kỹ thuật cần tránh |
| `references/dna-hung-anti.md` | Hồ sơ bóc tách thông số gốc từ video tham chiếu 4K |
| `assets/fonts/` | Trọn bộ **13 file font chuẩn 1:1** (`UTM Bebas`, `Anton`, `GreatVibes`, `Smooch`, `UTM Aptima*`, `Trajan`, `Montserrat`, `GoogleSans`) |
| `assets/sfx-59-catalog.json` | Danh mục 59 hiệu ứng âm thanh Studio phân theo 6 vai trò |
| `scripts/hung_engine.py` | Engine điều phối timeline, trộn âm 3 stem + BGM ducking + 59 SFX & xuất thẳng `.MP4` |
| `scripts/hung_gfx.py` | Thư viện đồ họa `2x` Supersampling: KeyText đa màu, `Carbon Pill`, `Split-Seam Olive Box` (`GreatVibes`), Light-Leak & Whip-Blur |
| `scripts/hung_cards.py` | Thư viện `2-Stage Sub-Pixel Keyframe Affine Warp`, A-Roll face reframing, Split `50/50` & `3-Tier`, Thẻ Hợp đồng phát sáng |
| `scripts/qa_audit.py` | Công cụ kiểm định tự động: `ffprobe`, `ebur128` LUFS/TP, 12-frame Typography Audit & `faster-whisper` Speech Completeness |
