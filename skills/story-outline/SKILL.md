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

## 🔀 2. GỢI Ý 3 NHÁNH RẼ KHI BÍ Ý TƯỞNG (PLOT BRANCHING)

Khi tác giả yêu cầu gợi ý tình tiết tiếp theo, AI mở tài liệu [../../references/plot-branching.md](../../references/plot-branching.md) và đề xuất chính xác **3 nhánh rẽ**:

1. **Nhánh A (Action & Escalation):** Đẩy cao xung đột ngay lập tức, nguy cơ ập đến bất ngờ, đối đầu trực diện.
2. **Nhánh B (Emotion & Depth):** Giãn nhịp (Slow-burn), đào sâu nội tâm, đối thoại riêng tư, phát triển quan hệ nhân vật.
3. **Nhánh C (Twist & Revelation):** Kích hoạt phục bút cũ, lật mở bí mật hoặc danh tính giả, tạo bước ngoặt bất ngờ.

*AI chỉ chấp bút sau khi tác giả chọn hoặc kết hợp các nhánh.*

---

## 🔍 3. SỔ THEO DÕI PHỤC BÚT & MANH MỐI (FORESHADOWING)

Lưu tại `stories/<active_story_id>/summaries/foreshadow.json`.

- **Xem danh sách phục bút:**
  ```powershell
  python manage_story.py foreshadow
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
*Mọi phục bút chưa giải sẽ được lệnh `context` tự động liệt kê nhắc nhở trước mỗi chương.*
