---
name: story-outline
description: "Hoạch định đề cương thích ứng (Adaptive Outline), đề xuất 3 nhánh rẽ cốt truyện khi bí ý tưởng và quản lý sổ tay phục bút, manh mối, bí mật. Kích hoạt: /story-outline, 'đề cương', 'lên dàn ý', 'gợi ý rẽ nhánh', 'phục bút', 'manh mối', 'bí mật'."
---

# /story-outline: Hoạch Định Đề Cương & Quản Lý Phục Bút

Chuyên trách việc thiết kế cấu trúc truyện dài tập, phân bổ mục tiêu từng Arc/Chương, gợi ý các hướng rẽ tình tiết khi bí ý tưởng và theo dõi chặt chẽ mọi nút thắt, phục bút trong tác phẩm.

---

## ⚠️ NGUYÊN TẮC CỐT TỬ: PHÂN BIỆT ĐỀ CƯƠNG VS SỰ KIỆN LỊCH SỬ

1. **Đề cương (`outline.md`) là KẾ HOẠCH TƯƠNG LAI, không phải SỰ THẬT ĐÃ XẢY RA:**
   - Các diễn biến nằm trong đề cương chỉ là dự định của tác giả.
   - **Tuyệt đối không** ghi các sự kiện từ đề cương vào dòng sự kiện Narrative Memory (`events.json`) hay Canon thế giới (`canon.json`) trước khi chương đó thực sự được viết và lưu trữ!
   - Chỉ khi chương đã được viết thành văn xuôi hoàn chỉnh và lưu trữ qua lệnh `save` hoặc `memory --add-event`, biến cố đó mới trở thành lịch sử xác lập.
2. **Điều chỉnh đề cương không được viết lại lịch sử truyện:**
   - Khi thay đổi kế hoạch các chương tương lai, giữ nguyên toàn bộ các chương và sự kiện đã diễn ra trong quá khứ.
   - Nếu kế hoạch mới mâu thuẫn với một sự kiện đã xảy ra, phải ghi nhận thành một điểm tranh chấp hoặc tìm giải pháp nhân quả hợp lý thay vì âm thầm sửa đổi quá khứ.

---

## 🗺️ 1. THIẾT KẾ & QUẢN LÝ ĐỀ CƯƠNG THÍCH ỨNG (ADAPTIVE OUTLINE)

Đề cương được lưu trữ trực tiếp dưới dạng Markdown tại `stories/<slug>/summaries/outline.md`.

- **Xem đề cương hiện hành:**
  ```powershell
  python manage_story.py outline
  ```
- **Cấu trúc chuẩn của một Đề cương Đa Tầng:**
  ```markdown
  # ĐỀ CƯƠNG TỔNG THỂ: [Tên Truyện]

  ## 1. THẾ GIỚI QUAN & QUY TẮC CỐT LÕI
  - Bối cảnh thời đại, hệ thống sức mạnh, các thế lực lớn.

  ## 2. ARC 1: [Tên Arc 1] (Chương 1 - 15)
  - **Mục tiêu tối thượng của Arc:** Nhân vật chính tìm được cổ vật và rời khỏi gia tộc.
  - **Xung đột chủ đạo:** Sự chèn ép của trưởng lão và bí mật thân thế.
  - **Kế hoạch phân chương:**
    - Chương 1: [Tên Chương] — Giới thiệu nhân vật, hoàn cảnh ngặt nghèo, biến cố khởi đầu.
    - Chương 2: [Tên Chương] — Chạm trán đối thủ, phát hiện manh mối đầu tiên.
    - ...
  ```
- **Cập nhật đề cương qua công cụ Native Markdown hoặc CLI:**
  - *Native Markdown:* Chỉnh sửa trực tiếp file `summaries/outline.md` bằng trình soạn thảo.
  - *CLI Staging:* Viết vào `chapters/draft.md` với dòng đầu `/story-outline` rồi chạy `python manage_story.py save`.

---

## 🔀 2. GỢI Ý 3 NHÁNH RẼ KHI BÍ Ý TƯỞNG (PLOT BRANCHING)

Khi tác giả yêu cầu gợi ý hướng đi tiếp theo (`"bí ý tưởng"`, `"chưa biết viết gì tiếp"`, `"gợi ý plot twist"`), AI đối chiếu dữ kiện từ Narrative Memory và đề xuất chính xác **3 nhánh rẽ chuẩn** dựa trên [../../references/plot-branching.md](../../references/plot-branching.md):

1. **Nhánh A — Đẩy cao xung đột (Action & Escalation):**
   - Đưa nguy cơ đến sớm hơn dự kiến: kẻ thù ra tay trước, một cái bẫy sập xuống, hoặc thời hạn gấp rút buộc nhân vật phải hành động ngay lập tức dưới áp lực lớn.
2. **Nhánh B — Đào sâu nội tâm & Quan hệ (Emotional Depth & Slow-Burn):**
   - Giãn nhịp hành động: một cuộc đối thoại đêm khuya giữa hai nhân vật, bộc lộ vết thương quá khứ, rạn nứt niềm tin hoặc khai thác mâu thuẫn niềm tin (Dramatic Irony).
3. **Nhánh C — Kích hoạt phục bút / Khúc quanh (Twist & Revelation):**
   - Lật mở một chi tiết đã gieo từ trước trong sổ tay phục bút (`foreshadow.json`) hoặc hé lộ một bí mật trong ma trận thông tin (`knowledge.json`).

*Nguyên tắc tương tác:* AI chỉ phác thảo ngắn gọn 1 đoạn cho mỗi nhánh kèm ưu/nhược điểm. Tác giả là người quyết định chọn nhánh A, B, C hoặc kết hợp trước khi tiến hành viết văn xuôi.

---

## 🔍 3. QUẢN LÝ SỔ PHỤC BÚT & MA TRẬN BÍ MẬT (FORESHADOW & SECRETS)

Lưu tại `stories/<slug>/summaries/foreshadow.json` và `summaries/memory/knowledge.json`.

- **Xem danh mục phục bút & ma trận bí mật:**
  ```powershell
  python manage_story.py foreshadow
  python manage_story.py memory --secrets
  ```
- **Ghi nhận manh mối mới (Dòng 1 `draft.md`):**
  ```markdown
  /story-foreshadow --clue "Bức thư màu đen" --chapter 5
  Tìm thấy trong di vật của sư phụ, có dấu niêm phong màu đỏ chưa mở.
  ```
- **Đánh dấu phục bút đã giải quyết:**
  ```markdown
  /story-foreshadow --clue "Bức thư màu đen" --resolve --chapter 15
  Lâm Phong đã mở thư và biết sự thật về huyết mạch gia tộc.
  ```
- **Kiểm soát bí mật (Dramatic Irony):**
  Thêm bí mật vào ma trận thông tin qua CLI:
  ```powershell
  python manage_story.py memory --add-fact --subject "Dạ Lão" --predicate "thực_chất_là" --object "Cừu nhân giết cha Lâm Phong" --type character_belief --state confirmed --chapter 8
  ```
  *Mọi manh mối chưa giải và bí mật chưa lộ sẽ được lệnh `python manage_story.py context` tự động tổng hợp nhắc nhở trước mỗi chương để tránh tình trạng "bỏ quên nút thắt".*
