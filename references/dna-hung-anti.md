# HỒ SƠ GIẢI PHẪU 100% DNA & BỘ QUY TẮC GỐC — `concept-4-hung-anti`

- **Video tham chiếu:** `C:\Users\NCPC\Downloads\Hung-Le-Parc-Place.mp4`
- **Phương pháp đo đạc:** Giải mã toàn bộ `2.119` khung hình gốc `2160×3840` (`4K UHD 9:16`), đo tọa độ pixel trên lưới thước `4K`, nhận diện giọng nói mức từng từ bằng `faster-whisper large-v3` (`244` từ / `16` phân đoạn), phân tích độ lớn âm thanh `FFmpeg ebur128`, tách kênh `Mid/Side (L±R)` và lọc 4 dải tần số để bắt chính xác các điểm nổ `SFX`, kết hợp `YuNet` dò khuôn mặt xuyên suốt 100% thời lượng.
- **Thư mục dữ liệu đo kiểm gốc:** `01_DNA_FORENSICS/` (gồm `forensics_summary.json`, `ref_transcript.json`, `clean_shots_4k.json`, 3 bảng `shots_contact_sheet`, 3 bảng `grid_1sec`, và 13 ảnh cắt thước đo pixel `4k_crops/`).

---

## PHẦN I — BÁO CÁO ĐO ĐẠC KỸ THUẬT 7 NHÓM YẾU TỐ DNA

### 1. Cấu trúc & Nhịp độ tổng thể (Pacing & Structure)

- **Thông số kỹ thuật gốc:**
  - Độ phân giải: **`2160 × 3840 px`** (tỷ lệ dọc `9:16` chuẩn 4K; quy đổi tỷ lệ 1:2 sang Full HD `1080 × 1920 px`).
  - Tốc độ khung hình: **`30.00 fps`** (`r_frame_rate = 30/1`, progressive, `bt709`, H.264 `21.8 Mbps`).
  - Tổng thời lượng: **`70.633 giây`** (`2.119 frames`), trong đó phần nội dung chính dài **`67.40 giây`** (`f=0..2021`) và màn kết đen thương hiệu (Brand Outro) dài **`3.23 giây`** (`f=2022..2118`).
- **Cấu trúc kịch bản 3 phần:**
  1. **HOOK (`0.00s – 7.93s` | `7.93s` ~ `11.2%` thời lượng):**
     - `0.00s – 4.57s`: A-Roll toàn thân người dẫn bước đi cạnh hồ bơi, tung câu mở đầu đánh thẳng vào phân khúc tài chính & sự tò mò (*"Khi mua căn hộ hơn 11 tỷ, em sẽ để ý 3 điều này trước tiên"*).
     - `4.57s – 7.93s`: Chuyển Zoom-Blur sang 2 cú Flycam đại cảnh khu đô thị để đặt vấn đề (*"Bởi vì nhà đẹp trên hình chưa chắc đã là nơi phù hợp để sống lâu dài"*).
  2. **BODY (`7.93s – 63.33s` | `55.40s` ~ `78.4%` thời lượng):** Chia thành **3 Luận điểm đánh số (`THỨ NHẤT` – `THỨ HAI` – `THỨ BA`) + Khúc Tổng kết thông số & Cảm xúc**:
     - *Luận điểm 1 (`7.93s – 16.07s`)*: A-Roll ngồi phân tích + thẻ hộp kính `THỨ NHẤT: MÔI TRƯỜNG SỐNG` → B-Roll chia 3 tầng (`1/3-1/3-1/3`) + Flycam cổng chào ParkCity.
     - *Luận điểm 2 (`16.07s – 28.20s`)*: A-Roll đứng trong phòng khách căn hộ mẫu + thẻ hộp kính `THỨ HAI: CẤU TRÚC CĂN HỘ` → B-Roll chia đôi khung hình (`50/50`) phòng khách/phòng ngủ kèm hộp kính giữa tâm `Căn 2PN | CÓ THÊM STUDY`.
     - *Luận điểm 3 (`28.20s – 38.67s`)*: B-Roll mặt đứng sảnh tòa nhà + thẻ hộp kính `THỨ BA: NHỮNG THỨ ÍT XUẤT HIỆN TRONG QUẢNG CÁO` → B-Roll hầm/tầng đỗ xe ô tô kèm chữ câu hỏi trên cao `Ô TÔ SẼ ĐỂ Ở ĐÂU ?` và cụm số liệu vàng kim `1140 CHỖ ĐỖ XE ĐỊNH DANH`.
     - *Khúc Tổng kết dự án & Giá trị dài hạn (`38.67s – 63.33s`)*: Chuỗi B-Roll phối cảnh công viên hồ, mặt đứng tháp ngày/đêm (`38.67s – 47.07s`) → A-Roll bước dọc hành lang căn hộ kèm chữ gắn tường hai bên `CĂN HỘ 2PN` / `DIỆN TÍCH 107M2` / `GIÁ KHOẢNG 11,4 TỶ` (`47.07s – 54.97s`) → A-Roll trung cảnh ngoài trời chốt tư duy mua nhà 10 năm tới (`54.97s – 63.33s`).
  3. **CTA & OUTRO (`63.33s – 70.63s` | `7.30s` ~ `10.4%` thời lượng):**
     - `63.33s – 67.40s` (`4.07s`): A-Roll cận trung nhìn thẳng ống kính mời tham quan thực tế + cụm chữ CTA cỡ đại `LIÊN HỆ NGAY / 0961919603`.
     - `67.40s – 70.63s` (`3.23s`): Nền đen tuyệt đối `#000000` hiển thị lần lượt logo dự án (`LE Parc Place`) và logo đơn vị phân phối (`NEXT HOME`).
- **Tần suất đổi cảnh & Quy tắc cắt khoảng nghỉ:**
  - Tổng cộng **21 cú máy thực tế** trên `70.63s` → **Trung bình `3.36 giây/cảnh`** (riêng phần B-Roll trung bình **`2.45 giây/cảnh`**, dao động từ `0.83s` đến `4.47s`; phần A-Roll giữ nhịp điềm tĩnh hơn, từ **`4.07s` đến `8.37s/cảnh`**).
  - **Cắt khoảng nghỉ cực gọn:** Trên toàn bộ `244` từ trong `67s` nói, chỉ có duy nhất **9 khoảng nghỉ `>= 120 ms`**.
    - Giữa các vế câu liên tiếp: cắt sát chỉ chừa **`140 ms – 360 ms`** (không để khoảng chết thừa nhưng tuyệt đối giữ nguyên âm đuôi).
    - Giữa các chương lớn (trước `Thứ nhất`, `Thứ hai`, `Tổng kết`, `CTA`): chừa nhịp thở **`440 ms – 800 ms`** để chèn hiệu ứng chuyển cảnh Light Leak + tiếng `Whoosh/Shimmer`.

---

### 2. Hệ thống Chữ & Hiệu ứng Chữ (Typography & Text Animation)

Điểm nhận diện đắt giá nhất của **Concept 04 - Hung Anti** là **KHÔNG dùng độc một kiểu chữ lặp đi lặp lại**, mà phân vai thành **4 Hệ Typography chuyên biệt (4 Archetypes)** tùy theo chức năng từng cảnh, kèm thanh nhận diện góc trên (Header Brand Bar):

#### (0) Thanh Logo Nhận Diện Cố Định Ở Mép Trên (`Header Brand Bar`)
- Duy trì xuyên suốt từ `0.00s` đến `67.40s`:
  - Góc trái trên: `x = 120..595 px` (`5.6%..27.5% W`), `y = 125..185 px` (`3.3%..4.8% H`).
  - Góc phải trên:Logo dự án `LE Parc Place - PARKCITY HANOI` trắng tinh tế tại `x = 1670..2065 px` (`77.3%..95.6% W`), `y = 85..245 px` (`2.2%..6.4% H`).

#### (A) Kiểu 1 — Cụm Chữ Kinetic Nghệ Thuật Đặt Lệch Cạnh Người Dẫn / Giữa Ngực (`Editorial Kinetic Cluster`)
- **Ứng dụng:** Ở cảnh Hook mở màn (`0–4.5s`), cảnh hành lang (`48–54.5s`) và cảnh đúc kết cảm xúc (`55–63s`).
- **Bố cục 3 tầng bất đối xứng & Phối 3 nhóm Font:**
  1. **Tầng dẫn (Lead-in):** Font có chân nghiêng thanh lịch (*Serif Italic* — kiểu `Playfair Display Bold Italic` / `Georgia Bold Italic`), màu trắng `#FFFFFF` hoặc xanh băng nhạt, cỡ chữ tương đối **`2.6% – 3.0% H`** (`100–115 px` ở 4K; `50–58 px` ở 1080p).
  2. **Chữ nhấn mềm (Script Accent):** Font viết tay bay bổng (*Calligraphy Script* — kiểu `Great Vibes`), màu xanh băng sáng `#A5F3FC` kèm quầng sáng **Cyan Outer Glow `#38BDF8`** (`blur 18px` ở 4K), cỡ chữ **`4.2% – 5.2% H`**, đặt đè nhẹ `10–15%` lên đầu chữ chính tạo chiều sâu lớp lang.
  3. **Từ khóa / Con số Hero (Hero Number / Keyword):** Font không chân hẹp siêu đậm (*Condensed ExtraBold/Black* — kiểu `Oswald Bold` / `Barlow Condensed ExtraBold` / `Anton`):
     - Với con số tài chính/thứ tự lớn (`11 TỶ`, `3 ĐIỀU NÀY`, `11,4 TỶ`): Cao tới **`7.8% – 9.8% H`** (`300–375 px` ở 4K; `150–188 px` ở 1080p), phủ **dải chuyển màu Vàng Kim Ánh Kim (`#FFF3B0 -> #F5B400 -> #D97706`)** kèm viền vát nổi 3D sáng `#FFFBEB` và bóng đổ mềm (`offset +10,+12 px`, `alpha 65%`).
     - Với câu chốt cận trung đặt trước ngực áo trắng (`SẼ NHƯ THẾ NÀO` / `10 NĂM TỚI?`): Dùng **Viền Sticker Trắng Dày `18 px` ở 4K (`9 px` ở 1080p)** bọc ngoài chữ Gradient **Xanh Dương Đậm (`#0B3B8C -> #0EA5E9`)** ở dòng 1 và **Cam Vàng Rực (`#EA580C -> #FACC15`)** ở dòng 2, đặt tại vùng `y = 53.4% – 66.7% H` (nằm gọn dưới micro cổ áo `y=50.5%` và trên thắt lưng, tuyệt đối không chạm cằm/mặt!).
  - **Biến thể Hành lang 2 bên (`Dual-Wall Callout`, `48–50.5s`):** Khi người dẫn bước chính giữa khung (`cx ~ 52%`), đặt 2 cụm chữ trắng Condensed Bold ép nhẹ phối cảnh dọc hai mảng tường trái (`x = 9%..31% W`) và phải (`x = 71%..94% W`), `y = 40%..58% H`.

#### (B) Kiểu 2 — Hộp Kính Viền Xanh Cyan Có Vân Chéo (`Glassmorphic Carbon Pill Badge`)
- **Ứng dụng:** Đánh dấu các chương/luận điểm chính (`THỨ NHẤT`, `THỨ HAI`, `THỨ BA`) và nhãn thông tin chính giữa cảnh chia đôi `50/50`.
- **Thông số đo pixel chính xác (trên hệ `2160×3840`):**
  - **Khung viên nang (Stadium Capsule):** `x = 195 .. 1965 px` (`9.0% .. 91.0% W`, rộng **`82.0% W`**), `y = 2955 .. 3355 px` (`77.0% .. 87.4% H`, cao **`10.4% H`** = `400 px` ở 4K / `200 px` ở 1080p), bo tròn bán nguyệt hai đầu (`border_radius = height / 2`).
  - **Nền & Viền hộp:** Nền đen xám bán trong suốt (`rgba(18, 22, 26, 0.58)`) có phủ lớp **vân sọc chéo 45° (`diagonal carbon hatch`, bước sọc `28 px` ở 4K, `alpha 12%`)** + viền phát sáng **Ice-Cyan `#99F6E4` / `#7DD3FC`** dày **`10–12 px` ở 4K (`5–6 px` ở 1080p)**.
  - **Nhãn chương trên mép hộp (`THỨ NHẤT / THỨ HAI / THỨ BA`):** Chữ trắng in hoa đậm nghiêng (`Bold Italic`), cao **`2.3% H`** (`88 px` ở 4K / `44 px` ở 1080p), đặt tựa sát mép trên bên trái hộp kính (`x ~ 16% W`, `y = 73.5%..76.2% H`).
  - **2 dòng chữ bên trong hộp:**
    - Dòng 1 (Tiêu đề chính): Font Condensed Bold in hoa, phủ **Gradient Vàng Gold (`#FFE082 -> #F59E0B`)**, cao **`3.12% H`** (`120 px` ở 4K / `60 px` ở 1080p).
    - Dòng 2 (Câu hỏi/ý phụ): Font Condensed Bold in hoa màu **Trắng Kem `#FFFDF5`**, cao **`2.34% H`** (`90 px` ở 4K / `45 px` ở 1080p).
    - Khoảng cách dãn dòng quang học giữa đáy Dòng 1 và đỉnh Dòng 2: **`55 px` ở 4K (`27.5 px` ở 1080p ~ `1.43% H`)**.
  - **Biến thể đặt giữa đường ranh giới Split 50/50 (`t=25–28s`):** Hộp viên nang màu rêu xám mờ (`rgba(42, 62, 42, 0.68)`, không viền cyan) đặt chính giữa `y = 44.8% .. 55.1% H` che khít đường cắt ngang `50%`, bên trái là chữ lớn `Căn 2PN`, bên phải là `CÓ THÊM STUDY / (Diện tích: 107m2)`.

#### (C) Kiểu 3 — Phụ Đề Đơn Tối Giản & Chữ Số Liệu Sang Trọng Trên Cảnh B-Roll (`Minimal B-Roll Caption & Luxury Gold Hero`)
- **Phụ đề dẫn chuyện trên B-Roll (`t=5–8s, 14–16s, 39–47s, 51–52.5s`):**
  - Chỉ **1 dòng duy nhất** căn giữa tại **`y = 72.5% – 75.0% H`** (hoặc `88% H` khi né tòa tháp ban đêm), lề an toàn hai bên `>= 10% W`.
  - Font *Bold Italic Serif/Humanist* màu trắng tinh `#FFFFFF`, cao **`2.14% H`** (`82 px` ở 4K / `41 px` ở 1080p), bóng đổ đen sắc gọn (`offset +8,+8 px` ở 4K, `rgba(0,0,0,0.75)`), **không thanh nền**, giúp phô diễn tối đa vẻ đẹp cảnh quay B-Roll.
- **Chữ Số Liệu / Câu Hỏi B-Roll Cao Cấp (`t=33s` & `t=36–38.6s`):**
  - Câu hỏi đặt vùng tối phía trên (`y = 16%..20% H`): Font Condensed Bold trắng `Ô TÔ SẼ ĐỂ Ở ĐÂU ?` (`3.4% H`).
  - Cụm số liệu sang trọng đặt vùng dưới (`y = 69.7%..94.1% H`): Số lớn `1140` (`9.1% H`) + 2 dòng Serif cổ điển in hoa vàng Champagne `#E5C158` (`CHỖ ĐỖ XE / ĐỊNH DANH`, cao `3.5% H`, có glow vàng dịu).

#### (D) Kiểu 4 — Cụm Chữ Kêu Gọi Hành Động Cỡ Đại & Màn Đen Kết (`CTA Sticker & Black Outro`)
- Đặt tại `y = 63.0% .. 75.1% H` trên A-Roll cận trung:
  - Dòng 1: `LIÊN HỆ NGAY` (Condensed Bold xanh dương `#1D4ED8 -> #06B6D4`, cao `4.17% H`).
  - Dòng 2: Số điện thoại hotline cao **`7.55% H`** (`290 px` ở 4K / `145 px` ở 1080p), rộng `85.2% W`, phủ Gradient Cam–Vàng `#EA580C -> #FACC15` bọc **viền trắng dày `20 px` ở 4K (`10 px` ở 1080p)**.
- **Quy tắc Animation & Đồng bộ mili-giây với giọng nói:**
  - Chữ chính bật ra **đúng thời điểm phát âm từ khóa (`offset 0 ms đến +60 ms`)**:
    - Con số/Từ khóa lớn: **Scale Pop Overshoot** trong `10–12 frames` (`0% -> 65% -> 112% bounce kèm tia sáng vàng -> 100%`).
    - Hộp kính chương: Viên nang trượt mở ngang trong `12 frames (0.40s)` → Tiêu đề vàng hiện kiểu **Glitch/Slice ngang** trong `10 frames (0.33s)` → Dòng phụ chạy **Typewriter từng ký tự kèm con trỏ đứng `|`** khớp tốc độ đọc câu hỏi!
    - Phụ đề đơn trên B-Roll: **Fade-in mượt `5 frames (0.17s)`** đúng âm tiết đầu của vế câu và tắt ngay khi dứt câu.

---

### 3. Cách xử lý Cảnh người nói (A-Roll) & Chuyển động máy

- **Tỷ lệ đa dạng cỡ cảnh A-Roll (không đứng một góc nhàm chán):**
  1. *Toàn thân bước đi / đứng (Wide Full-Body Shot — Hook `0–4.5s` & Phòng khách `16–23s` & Hành lang `47–55s`)*: Chiều cao khuôn mặt chiếm **`6.2% – 11.8% H`**, tâm mặt đặt lệch nhẹ sang phải (`cx = 58.3% – 61.9% W`, `cy = 29.5% – 39.4% H`) để nhường toàn bộ khoảng trống bên trái (`x = 8%..48% W`) cho cụm chữ Kinetic!
  2. *Trung cảnh ngồi / đứng ngoài trời (Medium Waist-Up Shot — `8–13s`, `55–67.4s`)*: Chiều cao khuôn mặt chiếm **`11.6% – 15.1% H`**, tâm mặt giữ ổn định gần trục giữa (`cx = 51.8% – 59.5% W`, `cy = 32.6% – 37.9% H`).
- **Chuyển động máy & Zoom trên A-Roll:**
  - **Không dùng Snap-Zoom giật cục liên tục** mà dùng **Slow Push-in mượt mà (`1.07× – 1.12×` xuyên suốt câu nói)** trên các cảnh trung (`Shot 04: fh 0.116 -> 0.130`, `Shot 17: fh 0.135 -> 0.144`, `Shot 18: fh 0.142 -> 0.151`), kết hợp chuyển động bước tiến tự nhiên của nhân vật (`Shot 16: fh 0.062 -> 0.119`).
  - **Tuyệt đối không Zoom-Out lùi giả tạo** trên cảnh đang nói (chỉ dùng hiệu ứng Radial Zoom-Blur `6 frames` ở đầu/cuối điểm cắt).

---

### 4. Cách sắp xếp Cảnh minh họa (B-Roll) & Bố cục khung hình

- **Tỷ lệ thời lượng A-Roll vs B-Roll (tính trên `67.40s` nội dung trước Outro):**
  - **A-Roll (có người dẫn xuất hiện trực tiếp):** `36.98 giây` (**`54.9%`** — gồm cả cảnh người dẫn đi trong căn hộ mẫu). *(Nếu tính thuần các đoạn thu tiếng trực tiếp tại hiện trường so với đoạn lồng tiếng Voice-over phủ B-Roll thì tỷ lệ xấp xỉ **45% A-Roll nói trực tiếp / 55% B-Roll & dẫn cảnh**).*
  - **B-Roll minh họa thuần (không có người dẫn):** `30.42 giây` (**`45.1%`**) + `3.23 giây` Outro đen.
- **Tỷ lệ bố cục khung hình B-Roll:**
  1. **B-Roll tràn viền `Full 9:16`:** Chiếm **`79.5%`** thời lượng B-Roll (`24.18s / 30.42s`) — Flycam đại cảnh, trục cây xanh, mặt đứng tòa nhà, hầm đỗ xe, phối cảnh hồ & tòa tháp đêm.
  2. **Chia đôi màn hình ngang `50/50 Split-Screen` (`t=23.17s – 28.20s`, dài `5.03s` ~ `16.5%` B-Roll):** Ghép 2 góc nội thất ngang (Phòng khách ở nửa trên `y=0..1920`, Phòng sinh hoạt/Phòng ngủ ở nửa dưới `y=1920..3840`), đặt hộp viên nang thông số đè chính giữa đường ranh giới `y=50%`.
  3. **Chia ba màn hình ngang `1/3 – 1/3 – 1/3 Split-Screen` (`t=13.10s – 14.30s`, dài `1.20s` ~ `4.0%` B-Roll):** Ghép 3 dải video Flycam ngang chuyển động đồng thời tạo nhịp thị giác dồn dập khi liệt kê hệ sinh thái (*"cư dân, không gian xanh..."*).
- **Quy tắc khớp ý lời thoại (Semantic Visual Matching 100%):**
  - Nhắc *"nhà đẹp trên hình / sống lâu dài"* → Flycam thực tế khu đô thị cây xanh đã vận hành.
  - Nhắc *"căn 2PN + Study 107m2"* → Chia đôi `50/50` thấy cùng lúc không gian khách – bếp – phòng làm việc & phòng ngủ.
  - Nhắc *"ô tô để ở đâu / 1140 chỗ đỗ xe"* → Cận cảnh xe sang chạy trong bãi đỗ xe hiện đại.

---

### 5. Chuyển cảnh & Hiệu ứng thị giác (Transitions & VFX)

Video mẫu sử dụng **4 loại chuyển cảnh phân cấp rõ rệt theo cấu trúc nội dung**:
1. **Radial Zoom-Blur Burst (`6 frames = 0.20s`):** Mở màn (`0.00–0.20s`), thoát khỏi Hook sang B-Roll (`4.50–4.70s`), và chuyển từ hành lang ra cảnh kết ngoài trời (`54.90–55.10s`).
2. **Double Film-Burn / Warm Light-Leak Flash (`8–10 frames = 0.27–0.33s`):** Dùng **đúng tại các điểm chuyển Chương lớn** (`7.93s` vào Thứ nhất, `16.07s` vào Thứ hai, `38.67s` vào Tổng kết dự án, `44.77s` sang Phối cảnh đêm, `63.33s` vào CTA, `67.40s` vào Outro). Ánh sáng cam–vàng–trắng lóe kép (`double flicker`) hòa trộn kiểu `Screen/Add` sang trọng, không phải chớp trắng phẳng đơn điệu.
3. **Directional Whip Blur (`6 frames = 0.20s`):**
   - *Vertical Whip Streak* (`12.93–13.13s`): Vuốt dọc tốc độ cao từ A-Roll sang cảnh Split 3 tầng.
   - *Horizontal Whip Pan* (`35.77s`): Lia ngang theo thân xe ô tô qua cột bãi đỗ xe mở ra con số `1140`.
4. **Clean Hard Cut (`0 frames`):** Dùng giữa các cú máy B-Roll cùng một chuỗi ý (`4.7->6.4s`, `14.3->15.2->16.1s`, `23.2->25.8s`, `40.8->42.9s`) để giữ nhịp gọn, sạch, không lạm dụng hiệu ứng gây rối mắt.

---

### 6. Âm thanh, Nhạc nền (BGM) & Hiệu ứng âm thanh (SFX)

- **Chuẩn độ lớn & Cân bằng Mix (`ebur128` & `Mid/Side` đo thực tế):**
  - Độ lớn tổng thể bản mẫu: **`-16.9 LUFS`**, dải động **`LRA = 4.9 LU`** (rất đều, chắc tiếng), Peak `-0.0 dBFS`. *(Khi xuất Master thực chiến, chuẩn hóa giọng về `-14.5 ~ -15.5 LUFS` và giới hạn True Peak `<= -1.0 dBTP` để đạt độ to rõ tối ưu trên TikTok/Reels mà không vỡ tiếng).*
  - **Nhạc nền (BGM):** Tông **Modern Luxury Ambient / Cinematic Corporate Pulse** (ấm áp, sang trọng, nhịp vừa phải ~100–115 BPM, có nền pad piano/synth hiện đại). Mức âm lượng nhạc nền giữ ổn định thấp hơn giọng nói **`-14 dB đến -16 dB`** (không dùng ducking bơm nhấp nhô gắt; đến màn Outro đen `67.4s–70.0s` nhạc fade-out mượt từ `-32.4 dBFS` xuống `-43.9 dBFS` rồi ngắt sạch).
- **Danh mục & Mật độ Hiệu ứng Âm thanh (SFX) đo từ phổ tần số:**
  - Tổng cộng ~**32 cụm sự kiện SFX chủ đạo** trong `67s` (~`1 SFX mỗi 2.1 giây`, đặt đúng điểm nhấn chứ không nhồi rác):
    1. **Deep Bass Impact + Whoosh (`25–130 Hz` + `180–900 Hz`):** Nổ đúng điểm mở màn (`0.26s`), điểm bung con số `11 TỶ` (`1.26s`, `+19.2 dB sub`), con số `3 ĐIỀU NÀY` (`3.38s`), và điểm cắt hết Hook (`4.42s`).
    2. **Warm Film-Burn Shutter / Shimmer Swoosh (`2.5–15 kHz`, prominence `+27 đến +35.9 dB`):** Đi cặp chính xác từng frame với chuyển cảnh Light-Leak tại `7.97s`, `16.10s`, `38.70s`, `44.80s`, `63.40s`.
    3. **UI Glass Slide / Digital Glitch Pop:** Khi hộp kính `THỨ NHẤT / THỨ HAI / THỨ BA` trượt mở (`9.02s`, `17.0s`, `28.9s`) và tiêu đề vàng hiện ra (`10.2s`).
    4. **Soft Mechanical Tick / Typewriter Subtle Click:** Đệm rất khẽ dưới dòng chữ chạy từng ký tự hoặc con số đếm `1140` (`11.0–12.2s`, `36.0–37.2s`).
    5. **Fast Air Whip Whoosh:** Tại các cú vuốt dọc/ngang `13.0s`, `35.8s`, `55.0s`.

---

### 7. Màu sắc & Ánh sáng (Color Grading)

- **Tông màu chủ đạo (`High-Key Bright Warm Luxury` — Tươi sáng, sang trọng, sạch sẽ):**
  - Độ sáng trung bình (`Luminance Y`) trên toàn bộ các cảnh A-Roll và nội thất đạt **`144 – 180 / 255`** (rất tươi sáng, trong trẻo, áo sơ mi trắng lên đúng sắc trắng kem sạch sẽ không ám xám).
  - Độ ấm màu (`R - B Warmth`): **`+18 đến +44`** trên cảnh người nói và nội thất (tôn da hồng hào ấm áp, ánh nắng vàng dịu kiểu khu đô thị sinh thái cao cấp); riêng cảnh render đêm/bãi xe giữ tông xanh điện ảnh (`R - B = -14 đến -29`) để tương phản nổi bật chữ vàng Gold.
  - Độ bão hòa (`Saturation S` trong hệ HSV 0–255): **`44 – 90`** ở cảnh quay thật (xanh lá cây ParkCity tươi mát tự nhiên, không rực gắt nhân tạo).
- **Xử lý nền tối dưới chữ (`Scrim / Contrast Control`):**
  - **Trên cảnh A-Roll sáng:** Tuyệt đối **không dìm tối lem nhem cả khung hình**; thay vào đó dùng **Hộp kính xám đen bán trong suốt (`alpha 58%`)** hoặc **Viền Sticker trắng dày (`9–10 px` ở 1080p)** để chữ nổi bật 100% mà cảnh quay vẫn tươi sáng rạng rỡ!
  - **Trên cảnh B-Roll có phụ đề trắng đơn:** Phủ một lớp **Soft Bottom Vignette / Scrim rất nhẹ (`18% – 24%` đen mờ dần từ `y=70%` xuống `y=100%`)** khi nền dưới quá sáng (như mặt đường bê tông nắng gắt) để chữ trắng Italic đọc rõ tức thì.

---

## PHẦN II — BỘ QUY TẮC GỐC NHÁP (`DRAFT RULES R1 -> R22`)

| Mã | Nhóm | Quy tắc định lượng bắt buộc cho `concept-4-hung-anti` |
|---|---|---|
| **R1** | Khung hình | Xuất chuẩn dọc **`9:16` (`1080×1920` hoặc `2160×3840`) @ `30.00 fps`**, progressive, `bt709`, H.264 chất lượng cao. |
| **R2** | Cấu trúc 3 phần | Tuân thủ mạch **Hook (`10–12%`) → Body phân chương rõ ràng (`76–80%`) → CTA + Brand Outro đen (`10–12%`)**. |
| **R3** | Nhịp cắt cảnh | Tần suất đổi cảnh trung bình **`2.8 – 3.8 giây/cảnh`**; B-Roll giữ `1.5 – 4.5s/cú`, không để 1 khung tĩnh kéo lê quá `6.5s` mà không có chuyển động hoặc đổi bố cục. |
| **R4** | Cắt khoảng lặng | Cắt sạch hơi thở thừa đầu/cuối take dựa trên năng lượng sóng âm thực tế (`< -46 dBFS` + đệm đuôi `100–140 ms` bảo vệ âm cuối); khoảng nghỉ giữa các vế câu **`150–350 ms`**, giữa các chương lớn **`450–750 ms`**. |
| **R5** | Đa dạng 4 kiểu chữ | Bắt buộc phối hợp đúng vai trò **4 kiểu Typography**: (1) *Editorial Kinetic Cluster* cho Hook/Nhấn ý A-Roll, (2) *Glassmorphic Carbon Pill* cho tiêu đề chương/thẻ thông tin, (3) *Minimal White Italic Caption* 1 dòng cho B-Roll dẫn chuyện, (4) *CTA Bold Sticker* cho lời kêu gọi cuối. |
| **R6** | Hệ 3 Font chuẩn | Kết hợp hài hòa 3 họ chữ có đầy đủ tiếng Việt: **Condensed ExtraBold** (tiêu đề/số lớn) + **Serif Bold Italic** (dẫn ý & phụ đề B-Roll) + **Calligraphy Script** (từ nhấn mềm màu xanh băng có glow). |
| **R7** | Hộp kính Chương | Hộp viên nang bo tròn bán nguyệt rộng **`82% W`**, cao **`10.4% H`**, đặt tại `y = 77%..87.4% H`, nền đen mờ `alpha 58%` có **vân sọc chéo 45°**, viền **Ice-Cyan `#88F2E8`** dày `5–6 px` (1080p), nhãn chương đặt sát mép trên trái hộp. |
| **R8** | Cỡ chữ chuẩn | Số/Từ khóa Hero: **`7.5% – 9.5% H`**; Tiêu đề chính trong hộp kính: **`3.1% H`**; Dòng phụ trong hộp kính: **`2.3% H`**; Phụ đề đơn B-Roll: **`2.15% H`**; Số Hotline CTA: **`7.0% – 7.6% H`**. |
| **R9** | Vùng an toàn & Né mặt | Biên an toàn trái/phải `>= 8% W` (trừ hộp viên nang `9% W`); chữ trên A-Roll trung cảnh đặt ở ngực/bụng (`y = 54%..87% H`, dưới cằm & micro cổ áo tối thiểu `4% H`), trên A-Roll toàn thân đặt lệch sang khoảng trống bên cạnh người dẫn — **0% đè lên khuôn mặt**. |
| **R10** | Animation chữ | Số/Từ khóa chính bật **Pop Overshoot (`0 -> 112% -> 100%` trong `10 frames`)** đúng mili-giây phát âm (`0..+60ms`); Hộp kính mở ngang `12 frames` + tiêu đề hiện Glitch nhẹ + dòng phụ chạy **Typewriter có con trỏ `|`**. |
| **R11** | Không lạm dụng chữ B-Roll | Khi đang chiếu B-Roll đẹp kèm lời bình dài, dùng **phụ đề 1 dòng trắng nghiêng tối giản** ở `y = 73% H` (chỉ bật cụm chữ lớn khi có con số đắt giá hoặc câu hỏi chuyển ý). |
| **R12** | Xử lý A-Roll & Zoom | Giữ mặt người nói cân đối ở `cy = 30%..39% H`; dùng **Slow Push-in mượt (`1.00× -> 1.08×`)** hoặc phóng nhẹ dứt khoát ở câu chốt (`1.12× – 1.18×`), tuyệt đối không Zoom-Out lùi và không rung giật. |
| **R13** | Tỷ lệ A-Roll / B-Roll | Cân bằng thời lượng **A-Roll (~40–55%)** và **B-Roll minh họa (~45–60%)** bám sát kịch bản; mọi cảnh B-Roll phải khớp 100% ngữ nghĩa lời thoại đang đọc. |
| **R14** | Đan xen Split-Screen | Trong phần B-Roll, kết hợp **`~75–80%` Full `9:16`** với **`~20–25%` Chia khung (`50/50` hai tầng kèm hộp viên nang giữa tâm & `1/3-1/3-1/3` ba tầng)** để tận dụng tối đa footage ngang sắc nét mà không bị vỡ hạt do crop dọc quá đà. |
| **R15** | Chất lượng Source B-Roll | Lọc bỏ 100% đoạn đầu/cuối rung máy, đoạn out-net, đoạn dính giọng hậu trường (*"Ok tạm xong nhé"*) hoặc dính chữ/watermark kênh khác. |
| **R16** | Chuyển cảnh mở màn & Hook | Mở đầu Frame 0 bằng **Radial Zoom-Blur (`6 frames`)** và thoát khỏi cảnh Hook sang B-Roll bằng **Radial Zoom-Blur hoặc Whip Blur (`6 frames`)**. |
| **R17** | Chuyển cảnh sang chương | Dùng **Warm Film-Burn / Double Light-Leak Flash (`8–10 frames`, cam–vàng–trắng hòa trộn `Screen`)** tại các ranh giới chuyển chương lớn; dùng **Hard Cut sạch** giữa các cú B-Roll con trong cùng một ý. |
| **R18** | Outro Thương hiệu | Kết thúc bằng **`2.5 – 3.2 giây` màn hình đen `#000000`** hiện logo dự án (`LE Parc Place - PARKCITY HANOI`) sang trọng kèm nhạc nền fade-out êm ái, không để hình người dẫn đứng đơ chờ tắt máy. |
| **R19** | Âm lượng & BGM | Chuẩn hóa tổng thể Master đạt **`-14.5 đến -16.0 LUFS`**, True Peak **`<= -1.0 dBTP`**; nhạc nền thuộc dòng **Luxury Ambient / Modern Corporate** đặt thấp hơn giọng nói **`-14 dB đến -16 dB`** xuyên suốt. |
| **R20** | Thiết kế SFX đa lớp | Đánh SFX đúng sự kiện hình ảnh (~1 sự kiện / `2.0–2.5s`), dùng tối thiểu **15–20 mẫu âm thanh khác nhau không lặp nhàm**: *Bass Impact + Whoosh* cho Hook/Số lớn, *Film-Burn Shimmer* cho Light-Leak, *Glass Slide* cho hộp viên nang, *Subtle Type Tick* cho chữ chạy, *Whip Swoosh* cho chuyển cảnh lướt. |
| **R21** | Chỉnh màu Tươi sáng | Áp dụng color grading **High-Key Tươi Sáng & Ấm Áp (`Y_median ~ 145–170`, tăng sáng midtones/shadows sạch sẽ, da người hồng ấm tự nhiên `R > B`, xanh lá cây tươi trong)** đúng yêu cầu ghi chú riêng của Sếp (`chỉnh màu tươi sáng`). |
| **R22** | Tương phản dưới chữ | Áp lớp phủ tối mềm phía dưới (`Soft Bottom Scrim 18–22%` từ `y=72%..100%`) riêng cho các cảnh B-Roll sáng có phụ đề trắng đơn; trên A-Roll dùng hộp viên nang mờ hoặc viền trắng dày để giữ nguyên độ tươi sáng của khuôn mặt và trang phục. |
