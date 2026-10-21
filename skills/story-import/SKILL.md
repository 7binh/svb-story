---
name: story-import
description: "Nghịch đảo nhập bản thảo truyện có sẵn (file thô nhiều chương) vào hệ sinh thái StoryFlow. Tự động bóc tách từng chương, tái dựng Narrative Memory, phân định sự thật vs suy luận, và xác định điểm tiếp tục sáng tác mà không làm biến dạng bản gốc. Kích hoạt: /story-import, 'nhập truyện', 'import truyện', 'phân tích truyện cũ', 'nạp bản thảo'."
---

# /story-import: Nghịch Đảo & Tái Dựng Ngữ Cảnh Bản Thảo Có Sẵn

Chuyên trách việc tiếp nhận các tác phẩm đã viết sẵn (file `.txt`, `.md` chứa hàng chục đến hàng trăm chương) và chuyển hóa nguyên vẹn vào cấu trúc dữ liệu đa tác phẩm của StoryFlow, thiết lập đầy đủ Narrative Memory để có thể viết tiếp mượt mà ngay lập tức.

---

## 🛡️ NGUYÊN TẮC BẢO VỆ BẢN THẢO GỐC (INGESTION SAFETY)

1. **Bảo tồn nguyên vẹn 100% bản gốc:** Quá trình phân rã không làm thay đổi, cắt xén hay xóa bỏ file tài liệu nguồn của tác giả.
2. **Phân định rõ ràng các tầng dữ kiện (Truth vs Inference):**
   - **Sự kiện đã xác lập (Confirmed Canon & Events):** Những tình tiết, hành động đã diễn ra trực tiếp trong các chương truyện.
   - **Kế hoạch / Dự định (Outline):** Các ghi chú về tương lai nếu có trong file nguồn; lưu vào `outline.md`, tuyệt đối không đưa vào sự kiện lịch sử đã qua.
   - **Suy luận chưa kiểm chứng (Inferred Facts):** Những giả thuyết về quan hệ nhân vật, âm mưu ngầm được AI suy đoán từ câu chữ; bắt buộc đánh dấu `state="inferred"`.
   - **Nút thắt chưa lời giải (Unresolved Mysteries):** Những câu hỏi mở, bí mật còn bỏ ngỏ; đưa vào `knowledge.json` với `state="unresolved"`.
   - **Trạng thái nhân vật ở chương cuối (End-State):** Xác định chính xác nhân vật đang ở đâu, mang vết thương gì, cầm vật phẩm nào tại điểm dừng của chương cuối cùng.
3. **Chỉ sáng tác sau khi hoàn tất tiếp nhận:** Không vội vàng viết chương mới khi cấu trúc dữ liệu và điểm tiếp tục chưa được xác nhận.

---

## 📥 QUY TRÌNH NGHỊCH ĐẢO 4 BƯỚC (REVERSE-ENGINEERING PIPELINE)

### Bước 1: Khởi Tạo Không Gian Tác Phẩm
Khi tác giả cung cấp file bản thảo hoặc đường dẫn:
```powershell
python manage_story.py init --title "<Tên Truyện>" --author "<Tác Giả>" --genre "<Thể Loại>" --id "<slug>"
```
Hệ thống tự động thiết lập cây thư mục chuẩn: `stories/<slug>/chapters/` và `stories/<slug>/summaries/`.

---

### Bước 2: Bóc Tách & Đánh Số Chương Tự Động
- Sử dụng thuật toán nhận diện ranh giới chương thông minh:
  * Tiếng Việt: `Chương \d+`, `Hồi \d+`, `Tiết \d+`, `Quyển \d+`.
  * Tiếng Anh / Đa ngữ: `Chapter \d+`, `# \d+`.
- Tách từng chương thành file độc lập: `stories/<slug>/chapters/chapter_XXXX.md` (định dạng 4 chữ số: `chapter_0001.md`, `chapter_0002.md`...).
- Gắn thẻ tóm tắt nhanh ở đầu mỗi file chương:
  ```markdown
  # Chương X: [Tiêu Đề Chương]
  <!-- brief: [Tóm tắt 1-2 câu diễn biến then chốt] -->

  (Toàn văn chương gốc giữ nguyên trạng...)
  ```
- Cập nhật số chương hiện có vào `story.json`.

---

### Bước 3: Tái Dựng Hồ Sơ & Narrative Memory
AI Agent quét bản thảo đã phân tách để trích xuất các tầng dữ liệu:
1. **Hồ sơ nhân vật & Trạng thái cuối:**
   - Trích xuất nhân vật chính, đối thủ, đồng minh vào `character_bible.json` và `summaries/characters.md`.
   - Ghi nhận trạng thái chấn thương, cảnh giới, vật phẩm tại chương cuối cùng vào `characters_state.json`.
2. **Quy tắc thế giới & Địa danh (Lorebook):**
   - Ghi nhận các môn phái, địa danh, quy tắc tu luyện vào `lorebook.json` và `summaries/canon.md`.
3. **Causal Timeline & Tóm tắt cuốn chiếu:**
   - Tạo các mốc sự kiện chính đưa vào `events.json`.
   - Tổng hợp tóm tắt các chặng đưa vào `summaries/rolling_summary.txt`.
4. **Phục bút chưa giải:**
   - Ghi nhận các manh mối còn dang dở vào `summaries/foreshadow.json`.

---

### Bước 4: Xác Định Điểm Tiếp Tục Sáng Tác
Sau khi quá trình nghịch đảo hoàn tất, Agent lập báo cáo tiếp nhận:
- **Tổng số chương đã nạp:** [Ví dụ: 25 chương, 65.000 từ].
- **Chương cuối cùng:** Chương 25: [Tên chương].
- **Trạng thái nhân vật chính tại điểm kết:** [Đang ở đâu, mang thương thế gì, nắm giữ vật phẩm nào].
- **Các bí mật / phục bút chưa giải quyết:** [Danh sách 2-3 nút thắt then chốt].
- **Điểm bắt đầu viết tiếp:** Chương 26!

👉 *Tác giả có thể kiểm tra trạng thái bằng `python manage_story.py status` và bắt đầu viết chương kế tiếp qua `/story-write` hoặc `/story-flow` hoàn toàn tự nhiên!*
