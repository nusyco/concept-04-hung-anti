# SỔ TAY QUY TẮC KHÓA CỨNG (LOCKED RULES `R1–R22` & `L1–L23`) — `concept-04-hung-anti`

> **TRẠNG THÁI CHỐT DUYỆT:** **ĐÃ DUYỆT ĐẠT (`v8` — Ngày 2026-11-14)** bởi Sếp Nguyễn Sỹ Cường trên dự án mẫu chuẩn **Le Parc Place – ParkCity Hanoi (Slot Đỗ Xe Ô Tô Định Danh)**.
>
> **QUY TẮC ƯU TIÊN HIỆU LỰC KHI TÁI SỬ DỤNG (`QUAN TRỌNG`):**
> - Tài liệu này lưu trữ **đầy đủ 100% lịch sử tiến hóa từ `v1` đến `v8` (`R1–R22` & `L1–L23`)** để A.I thấy rõ những lỗi cũ tuyệt đối không được tái phạm.
> - Khi có sự điều chỉnh qua các vòng, **quy tắc ở vòng sau luôn ghi đè quy tắc vòng trước** (cụ thể: **`L14–L23` (`v6 -> v8`) là chuẩn cuối cùng đang có hiệu lực thi hành**):
>   1. **Bộ Font chuẩn 1:1 (`L19` + `L22`, có sẵn trong `assets/fonts/`):**
>      - Chữ viết tay mềm mại trong Box (`Đối chiếu`, `Căn`) & KeyText hành lang (`Vị trí`): **`GreatVibes-Regular.ttf`** kết xuất nguyên cụm liền nét kèm nghiêng bút lông `2x` supersampled `shear_x = -0.22` (`condense_x = 1.0`, `stroke_boost = 0`).
>      - Chữ viết tay cọ phóng khoáng ở Hook/Chest (`Căn hộ`, `Hợp đồng`, `Làm rõ điều khoản`): **`Smooch-Regular.ttf`**.
>      - Chữ không chân cao thanh thoát chủ lực (`MUA BÁN`, `CHỖ ĐỂ XE`, `4 MỤC`, `TRONG HỢP ĐỒNG`, `SLOT Ô TÔ ĐỊNH DANH`): **`UTM Bebas.ttf`**.
>      - Chữ/Số khối siêu đậm (`SLOT`, `4`, Hotline `0986.254.566`): **`Anton-Regular.ttf`**.
>      - Chữ dẫn đứng/nghiêng & phụ đề ngoặc đơn: **`UTM Aptima.ttf`** *(CẤM dùng dấu gạch ngang dài Unicode `—` `U+2014` vì font gắn watermark bản quyền vào ký tự này — chỉ dùng `,` hoặc `-` ASCII!)*, **`UTM AptimaItalic.ttf`**, **`UTM AptimaBoldItalic.ttf`**.
>      - Tag đầu hộp `Carbon Pill` & Chữ cổ điển chân đế: **`Montserrat-ExtraBoldItalic.otf`** & **`UTM Trajan Pro Bold.ttf`**.
>   2. **Không làm Text 3D đùn khối dày hay dán tường lệch kiến trúc (`L17` + `L23` ghi đè `L11`):**
>      - Toàn bộ chữ 2D trên màn hình giữ `extrude_3d_px = 0`, `stroke_px = 0` (chỉ dùng gradient kim loại/xanh băng + vát sáng mỏng `bevel_3d` + glow dịu + bóng đổ định hướng).
>      - Với cảnh hành lang / nội thất góc nghiêng (như `P8C`), **không ép Text 3D lên vách tường**; sử dụng **Cụm KeyText Đa Màu Chơi Chữ 3 Tầng (`draw_corridor_keytext_p8c`)** đặt hài hòa ở `1/3` dưới (`cy_norm = 0.772`), giải phóng 100% kiến trúc và gương mặt.
>   3. **Quy tắc Hiện Chữ & Giữ Chữ Đủ Đọc (`L14 + L15 + L16` ghi đè `L12`):**
>      - **CHỈ các Cụm `KeyText` Phối Nhiều Màu Sắc** (`Hook P1`, `Câu hỏi nhấn 2 màu`, `Mid-Chest P5`, `Number-Stack P8A`, `Corridor KeyText P8C`, `CTA P9B`) mới hiện nối tiếp theo nhịp thoại (`2–4` nhịp mảng màu rõ ràng).
>      - **Toàn bộ Hộp `Carbon Pill`, Hộp `Split-Seam Olive Pill` và Phụ đề B-Roll đơn sắc:** Hiện **trọn vẹn 100% nội dung ngay từ đầu cảnh** (`0%` quét cắt nửa dòng kiểu `l1_steps`), đứng nét tối thiểu `1.8s – 4.5s` và chỉ thu `Ease-Out` trong **`6 frames` (`0.20s`)** cuối cảnh.
>   4. **Chuẩn Tọa Độ Hộp Kính Theo Chân Chữ Thực (`cap_y0 / cap_y1` — `L20 + L22`):**
>      - Hộp `Split-Seam Olive Pill` cố định **`844 × 184 px` (`R = 92`)**, neo theo `cap-top` & `baseline` để dấu nặng (`Ụ, Ợ, Ộ`) không bao giờ đẩy xô lệch dòng.
>      - Hộp `Carbon Pill` cố định **`884 × 196 px` (`R = 98`)**, viền cyan `#8CF4EA` mảnh, nền kính sọc chéo xuyên thấu `alpha = 0.58`, tag chương nằm ngoài mép phẳng trái trên (`x = x0 + 46..R`).
>   5. **Chuyển Động B-Roll & Âm Thanh Studio Đa Lớp (`L10 + L21`):**
>      - `100%` B-Roll, ảnh tĩnh và A-Roll dùng **`2-Stage Sub-Pixel Floating-Point Keyframe Affine Warp`** (`cv2.warpAffine` `INTER_CUBIC | WARP_INVERSE_MAP`, `0%` cắt mảng số nguyên gây giật cục).
>      - Âm thanh phối **50–60 file SFX độc bản (`0%` trùng lặp)** từ `theSOUNDS 1 & 2` + `HAY DÙNG` + `Ui Sound` + `Swoosh`, kết hợp **Dynamic BGM Ducking (`-2.8 dB` khi có giọng nói)**, chuẩn hóa tổng thể **`-14.8 LUFS` (`TP <= -1.2 dBTP`)**.

---

## I. NỀN TẢNG GỐC TỪ VIDEO MẪU (`BASELINE DNA R1 -> R22`)

- **R1 (Định dạng xuất):** Tỷ lệ dọc `9:16` (`1080×1920`), `30.00 fps`, `bt709`, H.264 chất lượng cao + AAC `48 kHz`.
- **R2 (Cấu trúc 3 phần):** Hook (`10–12%`) → Body phân chương bằng thẻ hộp kính (`76–80%`) → CTA + Brand Outro đen (`10–12%`).
- **R3 (Nhịp cắt cảnh):** Trung bình `2.8 – 3.8 giây/cảnh`; không để 1 cú máy tĩnh quá `6.5s`.
- **R4 (Cắt câu & Khoảng nghỉ):** Không cắt cụt âm tiết cuối câu (kiểm tra sóng âm `< -46 dBFS` + đệm đuôi `100–140 ms`); nghỉ giữa vế câu `150–350 ms`, nghỉ chuyển chương `450–750 ms`.
- **R5–R8 (4 Kiểu Chữ đặc trưng Hung Anti — Đã hiệu chỉnh theo `L1–L4` Sếp chốt):**
  1. *Editorial Kinetic Lockup* (`UTM AptimaBoldItalic` trắng + `SVN-Aaron Script` xanh băng phát sáng `#38BDF8` + `UTM Bebas` / `Anton-Regular` vàng kim lấp lánh `#FFF5A8 -> #F59E0B` hoặc xanh đại dương `#0284C7 -> #7DD3FC`, **tuyệt đối `0px` viền trắng dày**, chỉ dùng bóng đổ sắc nét + glow + vát cạnh sáng 3D mỏng `1.5–2px`).
  2. *Glassmorphic Carbon Pill Badge* (viên nang rộng `84% W`, cao `196px` tại `cy=82% H`, nền đen mờ sọc chéo carbon 45°, viền cyan `#88F2E8` `5px`, nhãn chương `Montserrat-ExtraBoldItalic` đặt sát mép trái trên `gap=8px`; bên trong dùng **`UTM Bebas.ttf`** cỡ lớn `74px` vàng kim dòng 1 + `52px` kem sáng dòng 2, khoảng cách quang học giữa 2 dòng cố định `14px`).
  3. *Minimal B-Roll Caption & Classical Gold Hero* (1 dòng `UTM AptimaBoldItalic` `48px` trắng tinh + bóng đổ cứng sắc nét `(4,4) blur=2` tại `cy=74.5% H`; cảnh số liệu đắt giá dùng số lớn `UTM Bebas` `166px` + `UTM Trajan Pro Bold` `62px/54px` vàng Champagne với khoảng cách dòng đều nhau tuyệt đối `14px`).
  4. *CTA Editorial Hero* (Dòng dẫn `UTM Bebas` `68px` xanh dương gradient **không viền**, số điện thoại `Anton-Regular` khổng lồ `112px` vàng–cam kim loại **không viền trắng dày**, dòng phụ tên chuyên viên `UTM AptimaBoldItalic` `44px` trắng sáng, cách dòng quang học đều nhau `14px`).
- **R9 (Né mặt & Vùng an toàn):** Lề ngang an toàn `>= 8% W`; chữ tuyệt đối không đè lên khuôn mặt người dẫn (`0% overlap`).
- **R10 (Đồng bộ Animation chữ):** Bật chữ khớp mili-giây phát âm từ khóa (`0..+60ms`): Pop Overshoot `10 frames` cho số/từ khóa lớn; mở ngang hộp kính `12 frames` + Glitch tiêu đề + Typewriter có con trỏ `|` cho dòng phụ.
- **R12 (A-Roll & Chuyển động máy):** Tâm mặt giữ ổn định tại `cy = 30%..39% H`; dùng `Slow Push-in (1.00× -> 1.08×)` mượt hoặc nhấn nhẹ `1.14×` ở câu chốt, cấm Zoom-Out lùi.
- **R13–R15 (B-Roll & Chia khung):** Kết hợp `~75–80%` B-Roll Full `9:16` (quay dọc 3K gốc) với `~20–25%` cảnh chia khung (`50/50` hai tầng kèm viên nang giữa tâm & `1/3-1/3-1/3` ba tầng cho footage Flycam ngang 16:9 để giữ độ nét tối đa); lọc sạch đoạn rung máy, giọng hậu trường và watermark.
- **R16–R18 (Chuyển cảnh & Outro):** Mở màn bằng `Radial Zoom-Blur (6f)`, chuyển chương lớn bằng `Double Warm Light-Leak Flash (9f)`, đan xen `Whip Blur (6f)` và `Hard Cut`; kết video bằng `2.8s` màn đen hiện logo `LE Parc Place` sang trọng.
- **R19–R20 (Âm thanh, BGM & SFX):** Tổng thể `-14.5 đến -15.5 LUFS`, True Peak `<= -1.0 dBTP`; nhạc nền Luxury Ambient thấp hơn giọng `-15 dB`, fade-out mượt ở Outro; chèn đa dạng SFX không lặp (*Bass Impact, Film-Burn Shimmer, Glass Slide, Typewriter Tick, Whip Swoosh*).
- **R21–R22 (Màu sắc Tươi sáng):** Nâng sáng trong trẻo & tươi tắn cho toàn bộ source (`High-Key Bright Fresh Grade`: mở shadows/midtones, cân bằng trắng sạch, da hồng ấm tự nhiên, cây xanh ParkCity tươi mát); phủ `Soft Bottom Scrim 20%` dưới phụ đề trắng trên B-Roll sáng.

---

## II. QUY TẮC KHÓA BỔ SUNG QUA CÁC VÒNG DUYỆT CỦA SẾP (`LOCKED FEEDBACK RULES`)

### Vòng 1 (`v1 -> v2` — Cập nhật 2026-11-11 theo chỉ đạo trực tiếp của Sếp)

- **L1 — Chuẩn hóa 100% Bộ Font chữ khớp Video tham chiếu:**
  - *Lỗi cũ cần tránh (`v1`):* Dùng `UTM Swiss 721 Black Condensed` (dáng chữ bè ngang, thô cứng), `GreatVibes-Regular` (nét mảnh yếu) và `Palatino Italic` (serif cổ chưa đúng chất hiện đại sang trọng của mẫu).
  - *Quy chuẩn mới Sếp chốt (`v2+`):* Khóa cứng đúng 5 font khớp từng nét chữ với video mẫu 4K của Hung Anti:
    1. **Condensed Display chủ lực (Hộp kính Carbon, Split Pill, Câu hỏi đầu trang, Tường hành lang, Dòng dẫn CTA):** `UTM Bebas.ttf` (cao, thanh thoát, sắc sảo).
    2. **Ultra-Bold Impact (Số liệu lớn Hook, Từ khóa nhấn mạnh, Số điện thoại Hotline CTA):** `Anton-Regular.ttf`.
    3. **Calligraphic Brush Script (Chữ viết tay cách điệu nhấn cảm xúc):** `SVN-Aaron Script.otf` (nét bút lông dày–mỏng sang trọng, bay bổng).
    4. **Humanist Editorial Italic (Phụ đề B-Roll, dòng dẫn mở ý, chú thích diện tích/thông số):** `UTM AptimaBoldItalic.ttf` (khớp 100% nét chữ *Bởi vì nhà đẹp trên hình* và *( Diện tích : 107m2 )* của video mẫu).
    5. **Luxury Classical Serif (Cảnh tôn vinh thông số kiến trúc/đỗ xe):** `UTM Trajan Pro Bold.ttf` + nhãn chương góc hộp kính `Montserrat-ExtraBoldItalic.otf`.

- **L2 — Bố cục Cụm chữ (Lockup) Chặt chẽ & Khoảng cách Dãn dòng Quang học Bằng nhau Tuyệt đối:**
  - *Lỗi cũ cần tránh (`v1`):* Đặt tọa độ từng dòng theo `cy` rời rạc khiến các dòng trong cụm bị hở xa nhau, khoảng cách giữa dòng 1–2 và dòng 2–3 lệch nhau thiếu liên kết; chữ trong hộp kính Carbon bị nhỏ lọt thỏm giữa hộp.
  - *Quy chuẩn mới Sếp chốt (`v2+`):*
    1. Bắt buộc đo **hộp mực thực tế của thân chữ (`ink_bbox`, tách riêng phần glow nền)** rồi xếp chồng bằng hàm khóa khoảng cách quang học đều nhau (`paste_equal_gap_stack`):
       - Cụm Kinetic Lockup (Hook, Điểm nhấn giữa khung, CTA 3 tầng): khoảng cách quang học giữa các tầng **bằng nhau tuyệt đối `11px – 13px`** (trên khung `1080×1920`); riêng chữ Script (`SVN-Aaron Script`) nghiêng nhẹ `5.5° – 6°` và gối nhẹ `4px` vào mép trên cụm chữ Display lớn giống hệt cụm *"Căn hộ hơn 11 TỶ"* và *"Căn 2PN"* của video mẫu.
       - Bên trong hộp kính `Carbon Pill` (`rộng 86% W = 928px, cao 188px`): tổng khối chữ (`UTM Bebas` `96px` vàng kim + `64px` kem sáng) chiếm `~75%` chiều cao hộp, cách nhau đúng **`14px`**, căn giữa tâm dọc tuyệt đối (đệm trên = đệm dưới, không để chữ nhỏ lọt thỏm).
       - Cụm `Dual-Wall Hành lang` và khối Hero ở `Hook`: tự động cân bằng chiều rộng 2 dòng (`match_font_size_to_width`) tạo khối chữ vuông vức kiểu kiến trúc, cách dòng cố định **`11px – 12px`**, đặt tại `cy = 44%–45.5% H` trên mảng tường sạch (né đèn trần).
       - Cụm `Luxury Gold Hero`: số lớn `UTM Bebas` `188px` + 2 dòng `UTM Trajan Pro Bold` `74px / 60px` vàng Champagne với khoảng cách dòng đều nhau tuyệt đối **`14px`**.

- **L3 — CẤM TUYỆT ĐỐI Viền chữ dày (`0px Thick Stroke`) — Nâng tầm Chữ Cách điệu Màu & Ánh sáng:**
  - *Lỗi cũ cần tránh (`v1`):* Bọc viền trắng dày `9px – 10px` quanh chữ ở Cảnh 5 và Cảnh CTA khiến chữ bị phồng thô kệch, rẻ tiền và rối mắt (Sếp đặc biệt ghét kiểu viền dày này).
  - *Quy chuẩn mới Sếp chốt (`v2+`):*
    1. **Khóa cứng `stroke_px = 0` trên toàn bộ mọi cụm chữ trong video** (tuyệt đối không bao giờ dùng viền trắng/đen dày bao quanh chữ).
    2. Tạo chiều sâu, độ tách nền và sự sang trọng bằng 4 kỹ thuật chuẩn điện ảnh từ video mẫu:
       - **Dải chuyển màu kim loại & hạt ánh kim (`Sparkling Metallic Gold` & `Royal-to-Ice Cyan Gradient`):** Vàng kim 3 điểm dừng (`#FFF7AD -> #F5B014 -> #FFE47A` kèm lớp hạt kim tuyến mịn cho con số/từ khóa Hero như số `11 TỶ`, `3` trong mẫu); Xanh lam ngọc (`#38BDF8 -> #0284C7` hoặc `#BAE6FD -> #38BDF8`) không viền.
       - **Vát cạnh sáng 3D tinh tế (`3D Specular Bevel 2px`):** Lớp highlight vàng kem nhạt lệch `(-2px, -2px)` tạo khối nổi 3D sắc sảo cho chữ Hero không cần viền.
       - **Quầng sáng màu dịu (`Soft Neon/Gold Outer Glow`):** Quầng xanh băng `#38BDF8` (`blur=11, alpha=185`) cho chữ Script / chữ trắng nhấn trong Split Pill; quầng vàng ấm `#F59E0B` (`blur=12, alpha=125`) cho chữ Vàng kim.
       - **Bóng đổ định hướng sắc nét (`Crisp Directional Drop Shadow`) + Lớp phủ tối mềm dưới nền (`Soft Scrim`):** Bóng đổ `(4, 5)` `blur=5, alpha=205` (riêng phụ đề B-Roll dùng bóng sắc `(4, 4) blur=2, alpha=225` đúng chuẩn mẫu) kết hợp dải Scrim tối êm sau lưng cụm chữ để chữ nổi bật 100% mà hoàn toàn không cần viền.

- **L4 — Bố cục Phân cấp Tương phản Cỡ chữ (Typographic Hierarchy & Asymmetric Lockup):**
  - *Lỗi cũ cần tránh (`v1`):* Các dòng trong cụm có cỡ chữ gần bằng nhau (ví dụ gộp cả tên và số điện thoại vào 1 dòng nhỏ `52px`), thiếu điểm nhấn thị giác mạnh.
  - *Quy chuẩn mới Sếp chốt (`v2+`):* Phải có sự đối lập rõ rệt giữa **Chữ Dẫn Nhỏ Tinh Tế (`42–48px` Italic/Script)** và **Chữ Hero Khổng Lồ (`96–166px` Display/Impact)**:
    - Hook mở màn: Kết hợp cụm khóa đồng trục tâm hoàn chỉnh (`── MUA CĂN HỘ ──` nhãn mảnh viền vàng + khối Hero vàng kim 3D cân bằng chiều rộng `SLOT ĐỖ XE / Ô TÔ ĐỊNH DANH` xếp khít `10px` + `✦ Tặng trọn đời ✦` Script xanh băng phát sáng căn giữa đồng trục).
    - CTA kết màn: Tách 3 tầng phân cấp rõ ràng, cách đều `13px`: Dòng 1 dẫn gọi hành động `UTM Bebas` `76px` xanh băng sáng (`Electric Ice-to-Sky`) → Dòng 2 Hotline khổng lồ **`0986.254.566`** `Anton-Regular` `122px` vàng–cam kim loại rực rỡ không viền → Dòng 3 định danh chuyên viên `UTM AptimaBoldItalic` `46px` trắng tinh khôi.

---

### Vòng 2 (`v2 -> v3` — Cập nhật 2026-11-12 theo chỉ đạo trực tiếp & 3 ảnh chụp đối chiếu của Sếp)

- **L5 — Nhịp độ Motion & Animation Chậm Rãi, Rõ Chuyển Động & 100% Có `Ease In - Out`:**
  - *Lỗi cũ cần tránh (`v2`):* Hiệu ứng bật chữ chỉ dài `8 frames` (`0.26s`), mở hộp kính `10 frames` (`0.33s` chỉ có `ease-out`), tắt chữ `5 frames` tuyến tính (`linear`) quá nhanh khiến mắt chưa kịp cảm nhận độ mượt của chuyển động.
  - *Quy chuẩn mới Sếp chốt (`v3+`):*
    1. **100% chuyển động xuất hiện (In) và biến mất (Out) bắt buộc dùng hàm nội suy `Ease-In-Out`** (`ease_in_out_cubic` kết hợp `ease_in_out_back` biên độ êm `1.032×`, vận tốc đầu = `0`, vận tốc cuối = `0`).
    2. **Kéo giãn thời lượng Animation chậm rãi, sang trọng để nhìn rõ chuyển động:**
       - Mở ngang hộp kính `Carbon Pill` / `Split Pill`: **`20 frames` (`0.67s`)** với `ease_in_out_cubic` nở đều từ chính tâm ra hai bên.
       - Xuất hiện từng tầng chữ (`Slide-Up 22px + Smooth Scale 0.88 -> 1.032 -> 1.00 + Opacity Fade`): **`20 frames` (`0.67s`)** cho mỗi tầng, độ trễ nối tiếp giữa các tầng (`stagger`) là **`7 – 8 frames` (`0.25s`)** để thấy rõ nhịp xếp lớp.
       - Thu chữ kết thúc cảnh (`Exit`): **`15 frames` (`0.50s`)** `ease_in_out_cubic` mờ dần êm ái kèm trượt nhẹ `-10px`.
       - Hiệu ứng sáng dòng Hợp đồng (`P4, P6B`): chuyển mượt trong **`14 frames` (`0.47s`)** `ease_in_out_cubic`.

- **L6 — Ghép Khối Cụm Chữ Đồng Trục, Liên Kết Chặt Chẽ & Ấn Tượng (Cohesive Editorial Lockup):**
  - *Lỗi cũ cần tránh (`v2` — Ảnh 1 Sếp chụp `P1`):* Xếp 4 dòng theo 3 trục căn lề khác nhau (`Mua căn hộ` căn trái, `Tặng trọn đời` xoay nghiêng `5.5°` thò đuôi sang trái chạm khung tranh, `SLOT ĐỖ XE` căn giữa sát tay áo người nói) làm cụm chữ rời rạc và cảm giác bị xô lệch.
  - *Quy chuẩn mới Sếp chốt (`v3+`):*
    1. Mọi cụm chữ nhiều tầng (`Hook P1`, `Mid-Chest P5`, `Gold Hero P8A`, `CTA P9B`) bắt buộc khóa trên **một trục đối xứng thống nhất (`Unified Center Axis`)**, không xoay nghiêng lệch trục gây thò thụt mép.
    2. Ghép các tầng thành một khối chữ chặt chẽ, cân bằng chiều rộng (`Slab-Justified`) và giữ khoảng thở tối thiểu **`>= 50px`** cách tay/người dẫn *(Lưu ý cập nhật tại `L9`: tuyệt đối không tự vẽ thêm nút phụ `[...]` hay đường kẻ cánh `──✦` không có trong video mẫu)*.

- **L7 — Căn Chỉnh Tuyệt Đối Chính Tâm Trong Mọi Ô Text Box (`0px` Lệch Trục):**
  - *Lỗi cũ cần tránh (`v2` — Ảnh 2 & Ảnh 3 Sếp chụp):*
    - Hộp `Carbon Pill` nở từ mép trái sang phải (khi mới mở bị lệch hẳn sang góc trái), dòng 2 gõ `Typewriter` từ trái sang phải kèm dấu `|` ở cuối làm chữ bị lệch tâm suốt lúc gõ và lệch sang phải khi gõ xong; nhãn chương `HỆ SINH THÁI` đặt lệch quá sát góc cong trái đè lên nền mái nhà trắng khó đọc.
    - Hộp `Split-Seam Olive Pill` đặt tọa độ cột trái/phải cố định (`lx_c=196, rx_c=602`) không tính độ rộng thực của chữ khiến tổng khối bị lệch sang phải.
  - *Quy chuẩn mới Sếp chốt (`v3+`, tinh chỉnh chuẩn mẫu tại `L9`):*
    1. **`Carbon Pill`:** Hộp nở đối xứng từ tâm `W // 2`; Dòng 1 & Dòng 2 luôn căn giữa tuyệt đối tại `W // 2` trong suốt quá trình trượt `Ease-In-Out` (bỏ dấu `|` thừa ở cuối dòng); nhãn chương đặt đúng vị trí chuẩn mẫu tại mép phẳng trên bên trái (`x = x0 + R`, xem chi tiết `L9`).
    2. **`Split-Seam Olive Pill`:** Tự động đo tổng chiều rộng thực tế `[Cột Trái + Khoảng Cách Cột + Cột Phải]` và đặt chính tâm `W // 2` trên từng khung hình (`left_margin == right_margin` tuyệt đối).

- **L8 — Khóa Vùng An Toàn Trong Phần Bo Tròn Của Mọi Ô Text Box (`0px` Tràn Viền Bo):**
  - *Lỗi cũ cần tránh (`v2` — Ảnh 2 & Ảnh 3 Sếp chụp):*
    - Trong `Split-Seam Olive Pill` (`2-4PN`), chữ `"Căn"` viết tay bị tràn nửa thân trên ra ngoài mép trên của ô xanh; chữ `"2"` bên trái và `"KHÔNG )"` bên phải tiến sát vào cung tròn hai đầu hộp.
    - Trong `Carbon Pill` (`ISPH - PARKCITY CLUB - THE LINC`), cho phép chiều rộng chữ `818px` trên hộp `928px` (bán kính bo `R = 94px`) khiến hai đầu dòng chữ đâm sát vào đường viền cong màu cyan.
  - *Quy chuẩn mới Sếp chốt (`v3+`):*
    1. **Công thức khóa chiều rộng phẳng tuyệt đối (`Safe Flat Chord`):** Với mọi ô Text Box dạng viên nang có chiều rộng $W_p$, chiều cao $H_p$ và bán kính góc bo $R = H_p / 2$, toàn bộ chữ bên trong **chỉ được phép nằm trong đoạn thẳng phẳng giữa hai tâm cung tròn trừ thêm đệm an toàn**:
       $$W_{\text{safe}} = W_p - 2R - 24\text{px}$$
       (Tương đương cách mép trái và mép phải của hộp tối thiểu **`R + 12px` = `108px – 114px`** — đảm bảo `0%` ký tự lọt vào vùng bo cong hai đầu!).
    2. **Công thức khóa chiều cao nội khu (`Safe Vertical Padding`):** Tổng chiều cao toàn bộ cụm chữ bên trong ô (tính cả chữ Script `"Căn"` / `"Đối chiếu"` + chữ số lớn + dấu tiếng Việt) bắt buộc `<= H_p - 44px` (đệm trên `>= 22px`, đệm dưới `>= 22px`), tuyệt đối không cho bất kỳ nét chữ nào nhô qua viền trên hoặc viền dưới của ô.

---

### Vòng 3 (`v3 -> v4` — Cập nhật 2026-11-12 theo chỉ đạo trực tiếp & ảnh chụp đối chiếu `Carbon Pill` của Sếp)

- **L9 — Tái Hiện Chuẩn Xác 100% Bố Cục Cụm Chữ & Hộp Kính Của Video Mẫu (`0%` Chi Tiết Tự Chế Rườm Rà):**
  - *Lỗi cũ cần tránh (`v3` — Ảnh Sếp chụp cảnh `P3` `ĐIỂM KHÁC BIỆT / SLOT Ô TÔ ĐỊNH DANH`):*
    1. Tự chế thêm nút nhãn nhỏ `[ĐIỂM KHÁC BIỆT]` đè lên viền trên của `Carbon Pill`, nút `[MUA CĂN HỘ]` / `[TÊN VĂN BẢN RÕ RÀNG]` và các đường gạch ngang kim cương `──✦` ở `Hook`, `Mid-Chest`, `Top Question`, `CTA` — không có trong video mẫu của Hung Anti, làm bố cục bị giả và nặng nề.
    2. Đổ nền hộp `Carbon Pill` quá đặc tối (`opacity = 0.87`) che khuất hậu cảnh; phóng cỡ chữ dòng 1 lên `82px` và ép khoảng cách 2 dòng còn `13px` khiến chữ vàng cao hẹp chật cứng ở giữa trong khi hai bên thừa khoảng trống lớn.
    3. Thêm viền sáng và vạch kẻ dọc `|` nhân tạo vào hộp `Split-Seam Olive Pill` (trong mẫu `t=27.0s` là viên nang xanh rêu mờ không viền, không vạch ngăn, dòng phụ `( Diện tích : 107m2 )` căn giữa dưới dòng tiêu đề phải).
  - *Quy chuẩn mới Sếp chốt (`v4+` — Đo chuẩn `1:1` trên lưới pixel `1080×1920` của `Hung-Le-Parc-Place.mp4`):*
    1. **Cấm tuyệt đối chi tiết đồ họa tự chế ngoài DNA mẫu:** Xóa bỏ `100%` các mini-button `[...]`, gạch chân kim cương và đường kẻ cánh `──✦`. Chỉ sử dụng thuần túy **tương phản phân cấp Typography + hiệu ứng kính mờ chuẩn mẫu**.
    2. **Thông số khóa cứng hộp `Carbon Pill` (`t=12.0s` & `t=19.5s` của mẫu):**
       - Kích thước viên nang: rộng **`880px` (`81.5% W`, `x = 100..980`)**, cao **`196px` (`R = 98px`, `cy = 81.5% H`)**, nở đối xứng từ tâm `W // 2` trong `20 frames` `Ease-In-Out`.
       - Chất liệu nền kính: **kính xám khói bán trong suốt (`alpha = 0.58`)** kết hợp vân sọc chéo carbon `45°` dịu nhẹ (`+14 lum`) và `GaussianBlur` nhẹ để vẫn nhìn xuyên thấu không gian sang trọng phía sau; viền xanh ngọc `#8CF4EA` thanh mảnh **`4.5px`** kèm quầng sáng nhẹ.
       - Nhãn chương (`ĐIỂM KHÁC BIỆT`, `GIÁ TRỊ THỰC TẾ`, `QUY MÔ ĐÔ THỊ`, `HỆ SINH THÁI`, `NHẬN TÀI LIỆU GỐC`): dùng font **`Montserrat-ExtraBoldItalic.otf` cỡ `48px`** màu Trắng tinh `#FFFFFF` có quầng xanh băng `#38BDF8` + bóng đổ sắc nét + lớp phủ tối cục bộ êm dưới chữ (`spot scrim`), đặt **ở bên ngoài phía trên mép phẳng trái của hộp** tại tọa độ khóa cứng **`ink_left = x0 + R = 198px`** (ngay điểm bắt đầu đoạn viền ngang thẳng, không bao giờ lơ lửng trên góc cong!) và **`ink_bottom = y0 - 14px`**.
       - Tỷ lệ chữ bên trong hộp (`Safe Flat Chord <= 660px`, cách hai đầu cong `>= 110px`):
         - Dòng 1: **`UTM Bebas.ttf` cỡ `66px`** (`ink_h ≈ 47px`) Vàng kim (`#FFE57F -> #F59E0B`).
         - Dòng 2: **`UTM Bebas.ttf` cỡ `50px`** (`ink_h ≈ 36px`) Trắng kem (`#FFFDF7`).
         - Khoảng cách quang học giữa Dòng 1 & Dòng 2: **`24px`** (thoáng đãng đúng chuẩn `26px` của mẫu!), đệm kính trên **`44px`**, đệm kính dưới **`45px`**.
    3. **Thông số khóa cứng hộp `Split-Seam Olive Pill` (`t=27.0s` của mẫu + kết hợp `L7, L8`):**
       - Viên nang xanh rêu mờ **không viền, không vạch ngăn dọc** (`rgba(54, 72, 50, 0.78)`, rộng `884px`, cao `192px`, `R = 96px`), tổng khối `[Cột Trái + Gap 36px + Cột Phải]` căn chính tâm `W // 2`, nằm gọn trong `Safe Flat Chord <= 668px` và chiều cao nội khu `<= 146px` (`0px` tràn viền!). Dòng chú thích ngoặc đơn `( ... )` căn giữa ngay dưới dòng tiêu đề cột phải.
    4. **Thông số khóa cứng 3 Cụm Chữ Tự Do (`Freestanding Editorial Clusters`):**
       - **`Hook P1` (chuẩn `t=1.5s` + `t=54.0s`):** 4 tầng thuần chữ đồng trục tâm `cx = 258px` (cách người nói `>= 68px`): Dòng 1 `UTM AptimaBoldItalic` `44px` trắng (`"Mua căn hộ"`) → Dòng 2 `SVN-Aaron Script` `78px` xanh băng phát sáng đặt ngang `0°` (`"Tặng trọn đời"`) → Khối Hero 2 dòng cân bằng chiều rộng `342px` `Anton-Regular` vàng kim 3D (`"SLOT ĐỖ XE"` / `"Ô TÔ ĐỊNH DANH"`), cách dòng đều `10px`.
       - **`Mid-Chest P5` (chuẩn `t=61.5s` bỏ viền dày theo `L3`):** Dòng 1 `UTM AptimaBoldItalic` `48px` trắng quầng xanh nhẹ (`"Tên văn bản rõ ràng"`) → Dòng 2 `UTM Bebas` `106px` xanh đại dương–băng (`"HỢP ĐỒNG MUA BÁN"`) → Dòng 3 ghép ngang cùng chiều rộng `Anton-Regular` `88px` cam–vàng kim (`"CHỖ ĐỂ XE"`) + `SVN-Aaron Script` `88px` xanh băng (`"riêng"`), căn tâm `W // 2`, cách dòng đều `12px`.
       - **`CTA P9B` (chuẩn `t=66.0s` bỏ viền dày theo `L3`):** 3 tầng thuần chữ căn tâm `W // 2`, cách đều `13px`: `UTM Bebas` `72px` xanh dương sáng (`"NHẬN MẶT BẰNG & MẪU HỢP ĐỒNG"`) → `Anton-Regular` `118px` cam–vàng kim 3D (`"0986.254.566"`) → `UTM AptimaBoldItalic` `42px` trắng (`"Nguyễn Nam - Tư vấn trực tiếp"`).

- **L10 — Bắt Buộc Dùng `Sub-Pixel Floating-Point Keyframe Zoom` Cho 100% B-Roll, Ảnh Tĩnh & A-Roll (`0%` Giật Cục):**
  - *Lỗi cũ cần tránh (`v1 -> v3`):* Dùng phép cắt mảng số nguyên `cw = int(round(base_w / z))` và `x0 = cx - cw // 2` trên từng khung hình. Khi zoom nhẹ (`1.00× -> 1.05×` trong `120–138 frames`), `cw` bị đứng yên 3–4 frame mới nhảy `1px`, đồng thời khi `cw` đổi chẵn/lẻ làm phép chia `cw // 2` giật tâm `±0.5px` qua lại gây hiện tượng rung/giật cục rõ rệt trên B-Roll.
  - *Quy chuẩn mới Sếp chốt (`v4+`):*
    1. **Cấm tuyệt đối `int(round(...))` array slicing để tạo chuyển động Zoom/Pan.**
    2. **Cơ chế `2-Stage Sub-Pixel Keyframe Affine Warp`:**
       - *Bước 1 (Khử răng cưa cố định):* Cắt vùng khung gốc cố định ở `zoom = 1.0` (`bx0, by0, base_w, base_h` bất biến suốt cảnh) và hạ mẫu chống răng cưa `cv2.INTER_AREA` về khung đệm `1.35×` (`W_ov, H_ov`). Đồng thời khóa bước nhảy frame nguồn hằng số (`stride = 1` cho nguồn `30.00 fps`, `stride = 2` cho nguồn `59.94 fps`) để triệt tiêu `100%` nhịp khựng lặp/bỏ frame.
       - *Bước 2 (Nội suy Keyframe số thực `float32` chính xác `0.0001 px`):* Tính hệ số phóng đại theo đường cong Keyframe mượt `z(t) = z_0 + (z_1 - z_0) \cdot \text{EaseInOutSine}(t)` (`1.00× -> 1.08×..1.10×`) và lấy mẫu bằng ma trận nghịch đảo tâm điểm ảnh thực:
         $$\text{cv2.warpAffine}(\text{ov\_bgr},\ M_{\text{inv}},\ (w_{\text{out}}, h_{\text{out}}),\ \text{flags}=\text{INTER\_CUBIC} \mid \text{WARP\_INVERSE\_MAP})$$
         Đảm bảo vận tốc phóng đại liên tục trên mọi frame (`0` frame đứng khựng, `0.000 px` lệch tâm chẵn/lẻ).

---

### Vòng 4 (`v4 -> v5` — Cập nhật 2026-11-12 theo 3 chỉ đạo & 4 ảnh đối chiếu Chữ 3D, Đồng bộ Thoại, Chơi Chữ của Sếp)

- **L11 — Hiệu Ứng Chữ 3D Khối Thực (`True 3D Extrusion` & `3D Corridor Perspective Homography`) Chuẩn Mẫu:**
  - *Lỗi cũ cần tránh (`v4` — Ảnh 1 Sếp chụp `P8C` đối chiếu Ảnh 2 `Hung t=49.5s`):*
    1. Chữ gắn tường hành lang (`VỊ TRÍ / ĐỖ XE`, `LỐI TỚI / THANG MÁY`) mới chỉ bóp mép `6.5%` phẳng lì như dán đề-can 2D, không có bề dày cạnh hông 3D, tô màu nửa trắng nửa vàng sai mẫu, và đặt đè sát đỉnh đầu nhân vật.
    2. Các con số và từ khóa Hero (`SLOT ĐỖ XE`, `MUA BÁN / CHỖ ĐỂ XE`, `4 TẦNG`, `0986.254.566`) mới chỉ có bóng mờ phẳng (`Drop Shadow`), thiếu khối đúc nổi 3D (`3D Block Extrusion`) sắc sảo như cụm `11 TỶ`, `3 ĐIỀU NÀY` trong video mẫu.
  - *Quy chuẩn mới Sếp chốt (`v5+` — Bóc tách 4K từ `Hung-Le-Parc-Place.mp4`):*
    1. **Chữ Tường Hành Lang 3D Phối Cảnh Điểm Tụ (`3D Architectural Wall Text` — chuẩn `t=49.5s`):**
       - **Màu & Font chuẩn mẫu:** Cả 2 dòng trên mỗi vách tường dùng thuần **`UTM Bebas.ttf` màu Trắng kiến trúc nguyên khối (`#FFFFFF -> #EDF2F7`)**, cân bằng độ rộng khối (`Slab-Justified`).
       - **Độ dày cạnh hông 3D thực (`12 – 15 lớp Extrusion`):** Đùn khối đặc hướng trực tiếp về **Điểm tụ hành lang `(VP_x, VP_y)`** (tường trái đùn sang phải-dưới `dx > 0`, tường phải đùn sang trái-dưới `dx < 0`), tô chuyển sắc xám đá kiến trúc (`#ABB3BF` sát mặt chữ → `#4B525E` ở đáy khối) + vát cạnh sáng mặt trước + bóng tiếp xúc mềm trên mặt tường (`Wall Contact Ambient Occlusion`).
       - **Biến đổi phối cảnh mặt phẳng `Homography` `36° – 42°`:** Cạnh gần ống kính giữ `100%` chiều cao, cạnh xa hội tụ về điểm tụ thu nhỏ còn **`64% – 66%`** chiều cao (cạnh trên dốc xuống `+17%..+18%`, cạnh dưới dốc lên `-17%..+18%`), bám khít đường phào chỉ tường thật và **cách đầu/thân người dẫn `100%` (`0px` chạm người)**.
    2. **Chữ Đúc Nổi 3D Cho Toàn Bộ Từ Khóa & Con Số Hero (`3D Cast-Gold & 3D Cobalt Extrusion`, vẫn giữ `0px` viền trắng dày theo `L3`):**
       - Khối chữ Vàng Kim Hero (`SLOT`, `ĐỖ XE`, `Ô TÔ ĐỊNH DANH`, `CHỖ ĐỂ XE`, `4`, `TẦNG`, `0986.254.566`): đùn **`7 – 10 lớp` khối 3D góc `(dx=+1, dy=+1)`** màu đồng cổ đậm (`#B4590A -> #481C03`) + vát sáng kim loại góc trái-trên `(-1, -1)` (`#FFFDF0`) + hạt ánh kim (`Sparkle`).
       - Khối chữ Xanh Dương Hero (`MUA BÁN`, `& CHỌN PHƯƠNG ÁN`): đùn **`7 – 8 lớp` khối 3D** màu xanh navy sâu (`#094C8C -> #031D38`) + vát sáng băng tuyết `#F0FAFF`.
       - Chữ chính trong hộp `Carbon Pill` & `Split Pill`: đùn nhẹ **`4 lớp` khối 3D** tạo chiều sâu nổi khối sang trọng trên nền kính mờ.

- **L12 — Quy Tắc "Thoại Đến Đâu Hiện Chữ Đến Đó" (`Millisecond Phrase-by-Phrase Sync`) & Đa Dạng 6 Kiểu Chuyển Động `Ease-In` / `Ease-Out`:**
  - *Lỗi cũ cần tránh (`v1 -> v4`):*
    1. Hiện cả cụm chữ nhiều mệnh đề cùng lúc hoặc chỉ lệch nhau `0.20s` cố định trước khi nhân vật đọc tới (ví dụ: chữ `"trọn đời"` hiện sớm `3.0s`; câu hỏi `"XE CỦA MÌNH SẼ ĐỖ Ở ĐÂU ?"` hiện sớm `3.2s`; dòng 2 của `Carbon Pill` hiện sớm `1.5s–2.8s`).
    2. Dùng lặp đi lặp lại duy nhất 1 kiểu trượt dọc `tier_motion` cho toàn bộ video gây cảm giác cứng nhắc, đơn điệu.
  - *Quy chuẩn mới Sếp chốt (`v5+`):*
    1. **Đồng bộ từng cụm từ theo mốc phát âm thực tế (`faster-whisper large-v3`, sai số `<= ±40ms`):** Bắt buộc tách cụm chữ thành các mảnh ngữ nghĩa (`Semantic Pieces`) và chỉ kích hoạt từng mảnh đúng khoảnh khắc người nói bắt đầu phát âm từ khóa đó (kể cả các vế bên trong `Carbon Pill`, `Split Pill`, `B-Roll Caption` và `Dual-Wall 3D`).
    2. **100% Hiệu ứng Chữ bắt buộc có cả `Ease-In` lúc xuất hiện VÀ `Ease-Out` lúc biến mất** (vận tốc đầu = `0`, vận tốc kết = `0` bằng `ease_in_out_cubic` / `ease_in_out_quart` / `ease_in_out_sine`).
    3. **Đa dạng hóa 6 kiểu Animation `Ease-In-Out` điện ảnh phối hợp linh hoạt theo vai trò chữ:**
       - `brush_wipe_lr`: Quét mở nét bút ngang từ trái sang phải (biên mờ lông vũ `44px` + trượt êm `-10px -> 0`) cho chữ viết tay `SVN-Aaron Script` và dòng liệt kê nối tiếp.
       - `mask_rise_up`: Trồi chữ từ mặt cắt vô hình tại chân dòng (`dy: +32px -> 0`, cắt biên mềm `12px`) cho dòng dẫn nghiêng `AptimaBoldItalic` và chữ cổ điển `Trajan`.
       - `pop_3d_depth`: Phóng khối chiều sâu trục Z có đệm đàn hồi êm (`scale: 0.72 -> 1.046 -> 1.00`, `Ease-In-Out` hai pha) cho các con số & từ khóa 3D Hero.
       - `glide_side_mask`: Trượt ngang khóa khớp từ vách cắt (`dx: ±38px -> 0`, `Ease-In-Out`) cho các mảnh ghép bên phải (`ĐỖ XE`, `MUA BÁN`, `TẦNG`, nhãn chương `Carbon Pill`).
       - `focus_rack_in`: Lấy nét quang học ống kính (`GaussianBlur r=7 -> 0` + `scale: 1.08 -> 1.00`, `Ease-In-Out`) cho câu hỏi nhấn & phụ đề B-Roll.
       - `wall_3d_glide`: Trượt phối cảnh dọc theo vector điểm tụ hành lang (`Ease-In-Out`) cho khối chữ tường 3D.

- **L13 — Nghệ Thuật Sắp Đặt "Chơi Chữ" Lồng Ghép Bất Đối Xứng (`Asymmetric Interlocking Wordplay`) Cho Cụm Chữ Tự Do (Cập Nhật & Nâng Cấp `L6`):**
  - *Lỗi cũ cần tránh (`v3 -> v4` — Ảnh 3 Sếp khoanh đỏ `P5` đối chiếu Ảnh 4 `Hung t=1.8s`):* Căn giữa cứng nhắc mọi dòng chữ tự do theo kiểu bia đối xứng (`Tên văn bản rõ ràng` / `HỢP ĐỒNG MUA BÁN` / `CHỖ ĐỂ XE riêng`), thiếu sự lồng ghép kích thước lớn–nhỏ đan cài nhau ("chơi chữ") đặc trưng của video mẫu.
  - *Quy chuẩn mới Sếp chốt (`v5+`):*
    1. **Phân tách rõ 2 chế độ bố cục:**
       - **Trong lòng hộp đóng kín (`Carbon Pill` & `Split-Seam Olive Pill`):** Giữ nguyên quy tắc căn chính tâm tuyệt đối và khóa vùng an toàn góc bo (`L7, L8, L9`).
       - **Trên các Cụm Chữ Tự Do (`Hook P1`, `Mid-Chest P5`, `Parking Hero P8A`, `CTA P9B`, `Question Lockups`):** Áp dụng **Bố cục Lồng Ghép Mảnh Ghép Bất Đối Xứng (`Tetris / Editorial Puzzle Wordplay`)** chuẩn DNA Hung Anti (`t=1.8s`, `t=4.5s`, `t=58.6s`, `t=61.8s`):
         - *Mẫu Lockup 1 (`Hook P1` — chuẩn `Khi mua / Căn hộ / hơn / 11 TỶ`):* Chữ `"Mua"` đặt gọn trong hốc trên bên phải của chữ cái hoa `"C"` bay bổng trong `"Căn hộ"`; chữ `"tặng"` lồng vào bậc tam cấp bên phải ngay dưới `"hộ"` và trên `"ĐỖ XE"`; chữ **`SLOT` 3D khổng lồ** đứng bên trái cao bằng tổng chiều cao `[tặng + ĐỖ XE]` bên phải; đáy khóa phẳng bằng thanh 3D `"Ô TÔ ĐỊNH DANH"` và chữ ký `"trọn đời"` lượn góc phải dưới.
         - *Mẫu Lockup 2 (`Mid-Chest P5` — chuẩn `t=58.6s` & `t=61.8s`):* Nhịp bước thang chéo `"Nhìn rõ"` (trái) → `"tên văn bản:"` (lùi phải); bên dưới ghép ngang bất đối xứng chữ viết tay xanh băng `"Hợp đồng"` (trái) khóa cạnh khối 3D xanh dương **`MUA BÁN`** (phải), đặt trên bệ chữ 3D vàng kim khổng lồ **`CHỖ ĐỂ XE`**.
         - *Mẫu Lockup 3 (`Parking Hero P8A` — chuẩn `3 | ĐIỀU / NÀY` tại `t=4.5s`):* Con số **`4` 3D khổng lồ (`214px`)** đứng bên trái, khóa chiều cao `1:1` với cụm 2 tầng **`TẦNG` / `ĐỖ XE NỔI`** bên phải, đặt trên dòng đế cổ điển `TỪ TẦNG 1 ĐẾN TẦNG 4`.
         - *Mẫu Lockup 4 (`CTA P9B`):* Cụm ghép ngang `[Script "Làm rõ điều khoản" + 3D Blue "& CHỌN PHƯƠNG ÁN"]` đặt bất đối xứng phía trên số Hotline 3D Vàng kim **`0986.254.566`**.


---

### Vòng 5 (`v5 -> v6` — Cập nhật 2026-11-12 theo 5 chỉ đạo chốt chi tiết & ảnh mẫu `Khi mua / Căn hộ / hơn / 11 TỶ` của Sếp)

> **Lưu ý hiệu lực ưu tiên:** Các quy tắc `L14 -> L18` dưới đây hiệu chỉnh trực tiếp và ghi đè các chi tiết bị làm quá tay ở `L11, L12, L13` của bản `v5`.

- **L14 — Chỉ Áp Dụng "Thoại Đến Đâu Hiện Chữ Đến Đó" Cho Cụm `KeyText` Đa Màu Sắc (Hiệu Chỉnh `L12`):**
  - *Lỗi cũ cần tránh (`v5`):* Áp dụng máy móc việc tách mảnh theo giọng nói cho TẤT CẢ mọi loại chữ (kể cả phụ đề B-Roll 1 màu, chữ bên trong `Carbon Pill` và `Split-Seam Olive Pill`), làm câu chữ bị vụn vặt, rối mắt.
  - *Quy chuẩn mới Sếp chốt (`v6+`):*
    1. **CHỈ áp dụng hiện nối tiếp theo nhịp thoại cho các Cụm `KeyText` Phối Nhiều Màu Sắc / Nhiều Font** (`Hook P1`, `Câu hỏi nhấn 2 màu P1 & P2B`, `Mid-Chest P5`, `Parking Hero P8A`, `3D Tường Hành Lang P8C`, `CTA P9B`), và mỗi cụm chỉ tách **tối đa `2 – 4` nhịp mảng màu rõ ràng** (không xé nhỏ thành 6–7 mảnh vụn).
    2. **Toàn bộ Phụ đề B-Roll đơn sắc, Hộp `Carbon Pill` và Hộp `Split-Seam Olive Pill`:** Hiện **nguyên khối trọn vẹn ngay từ đầu cảnh** với một chuyển động `Ease-In-Out` mượt mà duy nhất (`0%` tách vế câu B-Roll).

- **L15 — Tối Đa Hóa Thời Lượng Lưu Chữ Trên Khung Hình & Cấm Thu `Out` Quá Sớm:**
  - *Lỗi cũ cần tránh (`v5`):* Nhiều mảnh chữ hiện muộn ở cuối câu thoại nhưng lại bắt đầu chạy hiệu ứng `Out` sớm từ `14 – 15 frames` (`0.50s`) trước điểm cắt cảnh (ví dụ `P1` chỉ đọng lại `0.3s`, `P2B` câu hỏi chỉ đọng `0.1s`, `P7C` chỉ đọng `0.3s`), khiến người xem chưa kịp đọc và không đọng lại thông tin.
  - *Quy chuẩn mới Sếp chốt (`v6+`):*
    1. Đưa thời điểm mở cụm chữ lên sớm ngay đầu nhịp hình/ý thoại để sau khi mảnh cuối cùng xuất hiện xong, toàn bộ cụm chữ **bắt buộc đứng nét `100%` tối thiểu `1.80s – 4.50s`** cho người xem đọc trọn vẹn.
    2. Thu ngắn thời lượng `Ease-Out` cuối cảnh xuống đúng **`6 frames` (`0.20s`, `ease_in_out_cubic`)** sát mép chuyển cảnh (không làm mờ chữ sớm khi cảnh vẫn đang diễn ra).

- **L16 — Cấm Tuyệt Đối Hiệu Ứng Quét Cắt Nửa Dòng Chữ Trong Hộp Kính (Xử Lý Triệt Để Lỗi `1:04 – 1:06`):**
  - *Lỗi cũ cần tránh (`v5` tại `1:04 – 1:06` cảnh `P7E` & `P6B`):* Dùng `l1_steps` / `r2_steps` quét dừng từng đoạn ngắn trong hộp kính (để chữ `"ISPH -"` đứng cụt ngủn hơn 2 giây rồi mới quét tiếp `"PARKCITY CLUB - THE LINC"`), gây ức chế thị giác cho người xem.
  - *Quy chuẩn mới Sếp chốt (`v6+`):* Xóa bỏ `100%` hiệu ứng `l1_steps` / `r2_steps` cắt nửa dòng. Khi hộp `Carbon Pill` hoặc `Split-Seam Olive Pill` mở ra (`0.55s`), **cả Dòng 1 và Dòng 2 hiện đầy đủ 100% nội dung ngay từ đầu** (`d_tag=2, d_l1=4, d_l2=7`) để người xem cảm nhận trọn vẹn thông điệp ngay lập tức.

- **L17 — Chuẩn Hóa Chữ 3D Tường Hành Lang Khớp Tuyệt Đối Font, Độ Vát Khối & Phối Cảnh Của Video Mẫu (Hiệu Chỉnh `L11`):**
  - *Lỗi cũ cần tránh (`v5`):*
    1. Đùn khối 3D nâu/xanh đen dày `7–10px` kiểu WordArt cho cả các chữ 2D phẳng trên màn hình (`P1, P5, P8A, P9B`), khác với bề mặt chữ phẳng sắc nét của video mẫu.
    2. Ở cảnh hành lang 3D (`P8C`), kéo giãn dọc font `1.34×` làm méo dấu tiếng Việt, đặt dòng dưới dài hơn dòng trên làm ngược tỷ lệ lớn–nhỏ của mẫu (`CĂN HỘ / 2PN`), bóp phối cảnh đối xứng `19%` lệch đường chân trời và đùn khối xám xanh dày `16px` đứng tĩnh không ăn nhập với chuyển động máy quay.
  - *Quy chuẩn mới Sếp chốt (`v6+` — Đo trực tiếp 400% zoom trên `CĂN HỘ / 2PN` & `DIỆN TÍCH / 107M2` tại `t=49.6s`):**
    1. **Toàn bộ chữ 2D trên màn hình (`Hook, Mid-Chest, Pill, Gold Hero, CTA`):** Đặt **`extrude_3d_px = 0`** — dùng mặt chữ phẳng chuyển sắc kim loại/xanh băng sắc nét + bóng đổ mềm định hướng đúng chuẩn mẫu.
    2. **Chữ 3D Tường Hành Lang (`P8C`):**
       - **Font & Tỷ lệ phân cấp chuẩn mẫu:** Dùng **`UTM Bebas.ttf` nguyên bản `1.00×`** (không kéo giãn biến dạng dấu); biên tập cặp từ ngắn dòng dưới để dòng dưới tự động lớn gấp `1.45× – 1.62×` dòng trên giống hệt `CĂN HỘ / 2PN` và `DIỆN TÍCH / 107M2`: Tường trái **`TỪ VỊ TRÍ` / `ĐỖ XE`**, Tường phải **`DI CHUYỂN TỚI` / `THANG MÁY`**, khoảng cách dãn dòng khít **`9px`**.
       - **Hiệu ứng cạnh 3D chuẩn mẫu:** Mặt chữ trắng sáng tinh khiết `#FFFFFF`, cạnh vát khối 3D mảnh sắc nét **`5px`** tông xám nâu ấm (`rgb(112, 102, 94) -> rgb(66, 58, 52)` ăn khớp tông gỗ/tường kem của hành lang) hướng về tâm hành lang + bóng tiếp xúc sát mặt tường (`offset ±4px, +3px, blur=2.5px`).
       - **Phối cảnh đường chân trời & Camera Wall-Tracking:** Hội tụ đúng cao độ đường chân trời thực của ống kính (`cy ≈ 46% H`: cạnh trên nghiêng xuống `+7.5%`, khe giữa 2 dòng gần như nằm ngang `~0°`, cạnh dưới nghiêng lên `-8.5%`, thu hẹp chiều ngang `0.78×`); đồng thời **trượt phóng nhẹ theo vector điểm tụ hành lang (`scale 0.91 -> 1.08`)** khớp tốc độ tiến máy quay để chữ bám dính vào mặt tường thật.

- **L18 — Chuẩn Hóa Sắp Xếp Cụm Chữ & Độ Dãn Dòng Khít Sát Như Video Gốc Mẫu (Hiệu Chỉnh `L13`):**
  - *Lỗi cũ cần tránh (`v5`):* Để khoảng cách dòng giữa các tầng chữ quá thưa (`14px – 20px`), cỡ chữ dòng dẫn trắng hơi nhỏ và tách `Hook P1` thành 7 mảnh làm cụm chữ cao dàn trải hơn mẫu `Khi mua / Căn hộ / hơn / 11 TỶ`.
  - *Quy chuẩn mới Sếp chốt (`v6+` — Đo trên lưới `25px` của `Hung-Le-Parc-Place.mp4`):**
    1. **`Hook P1` (chuẩn `1:1` ảnh mẫu `Khi mua / Căn hộ / hơn / 11 TỶ`):** Gói gọn trong **4 nhịp màu sắc nét**, đỉnh chữ trắng `"Mua"` (`UTM AptimaBoldItalic` `48px`) cao ngang bằng đỉnh chữ hoa `"C"` của `"Căn hộ"` (`SVN-Aaron Script` `108px`, hở khít `3px` trên thân `"ăn hộ"`), chữ trắng `"tặng"` (`46px`) lồng khít vào hốc phải (`gap = 4px`), khóa chiều cao `1:1` giữa **`SLOT`** (trái) và `[tặng + 4px + ĐỖ XE]` (phải), thanh đế vàng **`Ô TÔ ĐỊNH DANH`** bám khít bên dưới với độ dãn dòng đúng **`5px`**.
    2. **`Mid-Chest P5` (chuẩn `1:1` `t=58.6s` & `t=61.8s`):** Dùng đồng bộ `UTM Bebas` cho các dòng chữ lớn để dấu tiếng Việt gọn gàng, cho phép ép **độ dãn dòng cực khít `4px – 5px`** giống hệt mẫu: Dòng 1 trắng nghiêng lớn (`56px` `"Nhìn rõ tên văn bản:"`) → cách `4px` → Dòng 2 ghép `[Script xanh băng "Hợp đồng" (98px) + Xanh đại dương UTM Bebas "MUA BÁN" (122px)]` → cách `5px` → Dòng 3 Vàng kim rực rỡ `UTM Bebas` `136px` **`"CHỖ ĐỂ XE"`**.
    3. **Độ dãn dòng trong các cụm còn lại:** `Carbon Pill` dãn dòng **`12px`** (chuẩn mẫu `t=12.2s`); `Split-Seam Olive Pill` chữ viết tay `"Căn"` / `"Đối chiếu"` gối khít `-4px` lên chữ số lớn, cột phải dãn dòng **`9px`**; `CTA` & `Question` dãn dòng khít **`6px – 8px`**.


- **L19 (Đối Chiếu Pixel 400% & Chủ Động Cài Đặt Bộ 6 Font Nguyên Bản 1:1 Theo Video Mẫu 4K — Cấm Dùng Font Na Ná):**
  - *Lỗi cũ ở v5 cần tránh:* Dùng `SVN-Aaron Script.otf` (nét bút lông dày, thiếu đuôi chữ `g` hình thoi và vòng lượn chéo chữ `C` của mẫu) cho chữ viết tay, và dùng `UTM AptimaBoldItalic.ttf` (quá đậm) cho chữ dẫn nghiêng khiến cảm giác thanh thoát chưa sát 100% với video gốc.
  - *Quy chuẩn khóa cứng v6:* Bóc tách đối chiếu ở mức zoom `400%` từng ký tự (`C, ă, n, h, ộ, D, ự, T, r, o, g, K, a, 1, 2, ?`) trên video gốc `Hung-Le-Parc-Place.mp4` (`2160×3840`), chủ động tải & cài đặt vào cả thư mục Engine (`03_ENGINE/fonts/`) lẫn hệ thống Windows (`%LOCALAPPDATA%\Microsoft\Windows\Fonts` + Registry `HKCU\...\Fonts`) đúng **6 file font nguyên bản 1:1**:
    1. **Script / Chữ ký nghệ thuật (`Căn hộ`, `Căn`, `Dự án`, `Trong`, `Hợp đồng`):** **`Smooch-Regular.ttf`** (trùng khớp 100% vòng lượn chéo chữ `C`, chữ `D` và đuôi móc hình thoi chữ `g` trong mẫu).
    2. **Chữ dẫn nghiêng thanh mảnh & Phụ đề trong ngoặc (`Khi mua`, `hơn`, `( Diện tích : 107m2 )`, phụ đề B-Roll):** **`UTM AptimaItalic.ttf`** (bản Regular Italic thanh mảnh, chữ `a` hai tầng chuẩn 1:1).
    3. **Chữ dẫn đứng giữa ngực (`không chỉ là`, `Gia đình mình`, `Nhìn rõ tên văn bản`):** **`UTM Aptima.ttf`** (đứng thẳng thanh thoát, có glow xanh nhạt nhẹ).
    4. **Chữ/Số khối siêu đậm (`11TỶ`, `SLOT`, `ĐỖ XE`, `4`, Hotline `0986.254.566`):** **`Anton-Regular.ttf`** (mũi ngang chữ `1`, thân khối đặc chuẩn CapCut gốc).
    5. **Chữ không chân hẹp cao (`MÔI TRƯỜNG SỐNG`, `2PN`, `107M2`, `SẼ NHƯ THẾ NÀO`, `MUA BÁN`, `CHỖ ĐỂ XE`):** **`UTM Bebas.ttf`** (đúng móc dấu `?`, số `2` và khối chữ 3D hành lang).
    6. **Tag nghiêng đầu hộp Pill (`THỨ NHẤT`) & Serif cổ điển chân đế (`CHỖ ĐỖ XE`):** **`Montserrat-ExtraBoldItalic.otf`** và **`UTM Trajan Pro Bold.ttf`**.

### Vòng 6 (Sếp duyệt `v6` -> Xuất `v7`)
- **L20 (Chuẩn Hóa Tọa Độ Tuyệt Đối 1:1 Hộp Text Box Chia Đôi Màn Hình `Split-Seam Olive Pill` & Hộp `Carbon Pill` Theo Thước Đo Pixel Mẫu 4K):**
  - *Lỗi cũ ở v6 cần tránh (Sếp chụp màn hình cảnh `P6B` đối chiếu trực tiếp cảnh `27.0s` của mẫu):*
    1. Hộp nền xanh ô-liu ở `v6` hơi bè ngang (`916px` thay vì `844px` của mẫu) làm thừa khoảng trống hai đầu.
    2. Cỡ chữ chính bên trái (`4 MỤC`, `2-4PN` cao `90–94px`) và dòng tiêu đề phải (`TRONG HỢP ĐỒNG` cao `56px`, `& BIỆT THỰ TRÊN KHÔNG` cao `46px`) bị nhỏ hơn mẫu; bóng đổ đen đậm (`alpha=215`) làm chữ hơi tối.
    3. Chữ viết tay góc trái (`Đối chiếu`, `Căn`) bị nhỏ và đè lẹm trực tiếp vào đầu chữ `4 MỤC` / `2-4PN` thay vì vươn cao lên khỏi mép trên hộp như mẫu.
    4. Căn dòng theo khung bao mực (`ink_bbox`) bị dấu nặng tiếng Việt (`Ụ` trong `MỤC`, `Ợ` trong `HỢP`) đẩy lệch: làm `4 MỤC` trồi lên đụng chữ viết tay, còn dòng phụ ngoặc đơn `( Vị trí - Thời hạn - Chi phí )` bị đẩy tụt xa khỏi dòng `TRONG HỢP ĐỒNG` và chữ nhỏ mảnh.
  - *Quy chuẩn khóa cứng v7 (đo lưới 20px trực tiếp trên khung `1080×1920` của mẫu `t=27.0s`):*
    1. **Kích thước hộp nền kính ô-liu:** Cố định **`full_w = 844px × ph = 184px`** (`x = 118 -> 962`, bo tròn bán kính `R = 92px`), neo theo mốc chân chữ thực (`cap-top & baseline`) thay vì `ink_bbox` để dấu nặng (`Ụ, Ợ, Ộ`) và dấu mũ (`Ồ, Ê`) **tuyệt đối không làm xô lệch khoảng cách dòng**.
    2. **Chữ chính cột trái (`4 MỤC`, `2-4PN`):** Chiều cao thân chữ hoa cố định **`122px`** (`y = y0 + 42 -> y0 + 164`, rộng `200–226px`), màu vàng kem sáng `#FFFBE6 -> #F6E48A`, bóng đổ cực nhẹ (`alpha = 90`).
    3. **Chữ viết tay xanh băng (`Căn`, `Đối chiếu` — font gốc 1:1 `Allison-Regular.ttf`):** Chữ cái đầu hoa (`C`, `Đ`) phóng lớn cao **`118–130px`** vươn hẳn lên phía trên mép hộp **`56px`** (`y_top = y0 - 56`, nét lượn trái bao ngoài vai chữ vàng, đuôi dưới xếp lớp sau vai trái chữ vàng y hệt mẫu `t=27.0s`), phần chữ thường (`ăn`, `ối chiếu`) nằm gọn dọc mép trên hộp (`y_bot = y0 + 30`), tạo **khoảng hở thoáng `12px`** phía trên `4 MỤC` / `2-4PN` (**0px đè lẹm lên mặt chữ vàng hay cột phải**).
    4. **Khoảng cách giữa 2 cột (`col_gap`):** Cố định **`38–40px`** từ mép phải chữ lớn cột trái tới mép trái cột phải (tổng khối rộng `<= 684px`, giữ biên an toàn `>= 80px` cách đều 2 đầu cong hộp `844px`).
    5. **Cột phải — Tiêu đề (`right_l1`) & Phụ đề ngoặc đơn (`right_l2`):**
       - Dòng 1 (`TRONG HỢP ĐỒNG`, `& BIỆT THỰ TRÊN KHÔNG`): Cao thân chữ hoa **`66px – 70px`** (`UTM Bebas` `88–96pt`, `baseline = y0 + 88`), mặt chữ trắng `#FFFFFF` kèm viền sáng xanh băng (`glow cyan`), rộng `<= 430px`.
       - Dòng 2 (`( Vị trí - Thời hạn - Chi phí )`, `( Đa dạng diện tích lựa chọn )`): Cỡ lớn đậm nét **`45pt – 47pt` `UTM AptimaBoldItalic.ttf`** (cao thân chữ hoa `32–34px` khớp chuẩn `( Diện tích : 107m2 )` của mẫu, rộng `92–96%` chiều ngang dòng 1), đặt cách chân `baseline` dòng 1 đúng **`18px`** (`cap_top = y0 + 106`), trắng tinh sắc nét.
    6. **Đồng bộ chuẩn tọa độ `cap_y1` cho hộp `Carbon Pill` (`884 × 196 px`):** Cố định `88pt` dòng vàng (`baseline = y0 + 98`) & `62pt` dòng trắng (`baseline = y0 + 166`) khớp chuẩn mẫu `t=12.2s`, triệt tiêu hoàn toàn hiện tượng dấu nặng dịch dòng.

### Vòng 7 (Sếp duyệt `v7` -> Xuất `v8`)
- **L21 (Thiết Kế Âm Thanh Đa Lớp Sống Động `50+` SFX Không Trùng Lặp Từ Kho `Bộ Bảo Hay Dùng\theSOUNDS 1 & 2` + Sidechain BGM Ducking):**
  - *Lỗi cũ ở v7 cần tránh:* Chỉ dùng 25 hiệu ứng đơn lẻ ở âm lượng nhỏ (`-18.5 dB -> -21.5 dB`) nên nhiều cảnh B-Roll, chuyển cảnh Light-Leak và lật hợp đồng bị thiếu điểm nhấn âm thanh.
  - *Quy chuẩn khóa cứng v8:* Khai thác trọn vẹn kho Studio `C:\About Me\TÀI NGUYÊN DỰNG\SFX\5. Sound Effect\Bộ Bảo Hay Dùng\theSOUNDS 1 & 2` phối hợp cùng `HAY DÙNG`, `Ui Sound`, `Swoosh`, `Transition Sound Effects` (**tổng cộng 52 SFX độc nhất, 0% lặp file**):
    1. **Lớp chuyển cảnh & dẫn dắt (Transitions & Risers, `-13.5 dB -> -15.0 dB`):** Phối `ShortRiser1..4.wav` mở đường + `Film Burn1..6.wav` / `Sunflare.wav` khớp từng frame nháy Light-Leak, và `Whip` / `Trifecta Whoosh` khớp từng nhát cắt Whip-Blur.
    2. **Lớp Foley thực cảnh & tài liệu (`-15.5 dB -> -23.0 dB`):** Tiếng sột soạt giấy hợp đồng `Paper (2..5).wav` khi mở văn bản `Hợp đồng mua bán chỗ để xe` (`P4, P6B, P9A`), tiếng chim hót không gian xanh `Birds.wav` nền nhẹ dưới công viên `77,4 ha` (`P3, P7A`).
    3. **Lớp nhấn Typography đa chất liệu (`-14.5 dB -> -16.5 dB`):** `Fabric Whoosh` / `Magic` cho nét cọ viết tay mềm mại; `Subtle Hit` / `Sun Ray` / `Pop Flash` cho cụm KeyText Vàng Gold; `Fluid Whoosh` / `Clean Whoosh` cho hộp Pill mở ngang; kết hợp **Sidechain Ducking nhạc nền (`-2.8 dB` khi có giọng đọc, nâng tự nhiên ở nhịp nghỉ)** giữ tổng thể chuẩn `-14.8 LUFS` vừa sang trọng vừa cuốn hút.
- **L22 (Font Chữ Viết Tay Siêu Mềm Mại Liền Mạch Trong Hộp Box — `GreatVibes-Regular.ttf` Nghiêng Calligraphic `-0.22`):**
  - *Lỗi cũ ở v7 cần tránh:* Tách rời chữ cái đầu (`Đ`, `C`) và phần sau (`ối chiếu`, `ăn`) bằng `Allison-Regular` kèm co ngang khiến nét chữ `Đối chiếu` hơi cứng và dựng đứng.
  - *Quy chuẩn khóa cứng v8:* Tải trực tiếp từ kho Google Fonts mở về `03_ENGINE/fonts/` và cài hệ thống bộ calligraphy mềm mại **`GreatVibes-Regular.ttf`** (kèm `Arizonia-Regular.ttf`), kết xuất siêu lấy mẫu `2x` với độ nghiêng bút lông mềm `shear_x = -0.22` **nguyên một cụm liền mạch không tách ký tự, không bóp ngang (`condense_x = 1.0`)**. Chữ hoa đầu (`Đ`, `C`) uốn lượn bay bổng vượt mép trên hộp `~48px`, nối liền nét tơ sang chữ thường (`ối chiếu`, `ăn`) cách đầu chữ vàng `11–12px` và cách cột phải `16px` thoáng mắt.
- **L23 (Thay Thế Text 3D Tường Hành Lang `P8C` Bằng Cụm `Multi-Color 2D KeyText Wordplay` Hài Hòa Đồng Bộ):**
  - *Lỗi cũ ở v7 cần tránh:* Góc máy thực tế cảnh `P8C` (`DJI_0148`) đứng nghiêng cạnh vòm trang trí, không phải hành lang đối xứng chính diện nên ép chữ 3D phối cảnh lên hai bên tường gây cảm giác lạc tông, thiếu ăn khớp với không gian.
  - *Quy chuẩn khóa cứng v8:* Gỡ bỏ khối 3D dán tường ở `P8C`, thay bằng cụm **KeyText 3 tầng đa sắc (`draw_corridor_keytext_p8c`)** đặt hài hòa ở vùng trống `1/3` dưới (`cy_norm = 0.772`), giữ trọn vòm đèn trang trí, gương mặt nhân vật và chiều sâu hành lang phía trên:
    - Tầng 1 (`UTM Aptima` `54pt` Trắng sáng, mở đầu cảnh): `"Khi chọn căn, cùng xem rõ"`
    - Tầng 2 (Khớp lời thoại `"vị trí đỗ xe"`): `"Vị trí"` (`GreatVibes` xanh băng phát sáng, hiệu ứng cọ quét) + `"ĐỖ XE"` (`UTM Bebas` `132pt` xanh dương đại dương)
    - Tầng 3 (Khớp lời thoại `"và lối di chuyển tới thang máy"`): `"& LỐI TỚI THANG MÁY"` (`UTM Bebas` `118pt` Vàng Gold ánh kim, giữ tĩnh trọn vẹn đến cuối cảnh `out_f = 6`).
