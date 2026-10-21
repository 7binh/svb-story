---
name: story-outline
description: "Quản lý đề cương thích ứng (Adaptive Outline), gợi ý 3 nhánh rẽ cốt truyện khi bí ý tưởng và theo dõi sổ tay phục bút (Foreshadowing). Kích hoạt: /story-outline, 'đề cương', 'lên dàn ý', 'gợi ý rẽ nhánh', 'phục bút', 'manh mối'."
---

# /story-outline: Đề Cương Thích Ứng & Theo Dõi Phục Bút

Chuyên trách việc hoạch định mạch truyện, đề xuất ý tưởng rẽ nhánh và không để sót bất kỳ nút thắt hay manh mối nào trong tác phẩm dài tập.

---

## 🗺️ 1. QUẢN LÝ ĐỀ CƯƠNG PHÂN ĐOẠN (ADAPTIVE OUTLINE)

Đề cương được lưu tại `stories/<active_story_id>/summaries/outline.md`.

- **Xem đề cương hiện tại:**
  ```powershell
  python manage_story.py outline
  ```
- **Cập nhật đề cương qua `draft.md`:** Soạn thảo vào file `draft.md` rồi chạy `python manage_story.py save`:
  ```markdown
  /story-outline
  ## MỤC TIÊU ARC HIỆN TẠI
  - Xung đột chủ đạo: Tranh đoạt bí cảnh cổ đại.
  ## KẾ HOẠCH CÁC CHƯƠNG TIẾP THEO
  - Chương 12: Tiến vào bí cảnh, chạm trán đệ tử Ma Tông.
  - Chương 13: Cạm bẫy trận pháp cổ và manh mối về Dạ Lão.
  ```

---

## 🔀 2. GỢI Ý 3 NHÁNH RẼ KHI BÍ Ý TƯỞNG (PLOT BRANCHING & MEMORY SYNC)

Khi tác giả yêu cầu gợi ý tình tiết tiếp theo, AI đối chiếu dữ kiện từ Narrative Memory (`events.json`, `knowledge.json`) và đề xuất chính xác **3 nhánh rẽ** dựa trên [../../references/plot-branching.md](../../references/plot-branching.md):

1. **Nhánh A (Action & Escalation):** Đẩy cao xung đột ngay lập tức, kích hoạt các mối thù trong Canon, đối đầu trực diện.
2. **Nhánh B (Emotion & Depth):** Giãn nhịp (Slow-burn), khai thác chấn thương thể chất/tâm lý, mâu thuẫn niềm tin (Belief vs Truth) của nhân vật.
3. **Nhánh C (Twist & Revelation):** Kích hoạt phục bút cũ hoặc lật mở một phần bí mật (`secrets`) đã đến điều kiện tiết lộ.

*AI chỉ chấp bút sau khi tác giả chọn hoặc kết hợp các nhánh.*

---

## 🔍 3. SỔ THEO DÕI PHỤC BÚT & BÍ MẬT (FORESHADOWING & SECRETS)

Lưu tại `stories/<active_story_id>/summaries/foreshadow.json` và `memory/knowledge.json`.

- **Xem danh sách phục bút & bí mật:**
  ```powershell
  python manage_story.py foreshadow
  python manage_story.py memory --secrets
  ```
- **Ghi nhận manh mối mới (Dòng 1 `draft.md`):**
  ```markdown
  /story-foreshadow --clue "Bức thư màu đen" --chapter 5
  Tìm thấy trong di vật của sư phụ, có dấu niêm phong màu đỏ.
  ```
- **Đánh dấu đã giải quyết (Dòng 1 `draft.md`):**
  ```markdown
  /story-foreshadow --clue "Bức thư màu đen" --resolve --chapter 15
  Lâm Phong đã mở bức thư và biết bí mật huyết mạch gia tộc.
  ```
*Mọi phục bút chưa giải và ma trận bí mật sẽ được lệnh `python manage_story.py context` tự động tổng hợp nhắc nhở trước mỗi chương.*
