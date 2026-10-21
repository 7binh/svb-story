---
name: story-write
description: "Quy trình viết và mở rộng chương truyện tối ưu token theo định hướng tác giả (Author-Led). Kích hoạt: /story-write, 'viết chương', 'tiếp tục viết', 'mở rộng nháp', 'chấp bút'."
---

# /story-write: Quy Trình Viết & Mở Rộng Chương Truyện Từng Bước

Quy trình 5 bước tương tác khép kín phối hợp giữa tác giả, AI và công cụ CLI `manage_story.py`, thực thi Style Enforcement Pipeline trong từng phân cảnh.

---

## 🔄 VÒNG LẶP SÁNG TÁC 7 BƯỚC (7-STEP WRITING PIPELINE)

### Bước 1: Hiểu Mục Tiêu Chương (Goal Understanding)
- Xác định rõ mục tiêu cốt truyện chương tiếp theo từ `outline.md` và vị trí trong Arc truyện hiện tại.
- Xác định những bất biến không được phép thay đổi ngoài ý muốn (quy tắc thế giới, chấn thương đang mang, bí mật chưa được lộ).

---

### Bước 2: Lập Kế Hoạch Cảnh (Scene Planning)
- Đối với phân cảnh phức tạp, xác định trước:
  1. **POV & Nhân vật xuất hiện**: Ai là nhân vật trung tâm, ai chứng kiến?
  2. **Trạng thái đầu & cuối cảnh**: Nhân vật thay đổi gì về thể chất, tâm lý, hoặc vật phẩm?
  3. **Mâu thuẫn & Trở lực**: Xung đột chính là gì (đối đầu, nghi kỵ nội tâm, áp lực thời gian)?
  4. **Kiểm soát bí mật**: Thông tin nào được phép tiết lộ, thông tin nào bắt buộc tiếp tục giữ kín?
  5. **Nhịp kể & Cảm xúc**: Cảnh hành động (dồn dập) hay cảnh tâm lý (lắng đọng, đào sâu đối thoại)?

---

### Bước 3: Truy Xuất Bộ Nhớ & Ngữ Cảnh 5 Lớp (Narrative Memory Retrieval)
- **Hành động:** Chạy lệnh:
  ```powershell
  python manage_story.py context
  ```
- **Tiêu chuẩn hoàn tất (Completion Criterion):**
  - **Lớp A (Core Context):** Nắm vững mục tiêu chương và quy tắc thế giới.
  - **Lớp B (Story Memory):** Nắm các sự kiện tiền đề gần nhất, chấn thương thể chất, vật phẩm đang giữ, và ma trận bí mật.
  - **Lớp C (Evidence & Disputes):** Đối soát các mâu thuẫn tranh chấp đang mở (nếu có).
  - **Lớp D (Style Context):** Nắm vững Profile văn phong đang active (nhịp câu, giác quan, khẩu khí) và giới hạn suy luận.
  - **Lớp E (Recent Context):** Đọc kỹ đoạn kết chương trước để bắt đúng nhịp mạch cảm xúc.

---

### Bước 4: Viết Văn Xuôi (Prose Drafting & Voice)
- Soạn thảo trực tiếp vào file `stories/<active_story_id>/chapters/draft.md`.
- **Cú pháp bắt buộc dòng 1 và 2:**
  ```markdown
  /story-title [Tên Chương Mới]
  /story-brief [Tóm tắt 1-2 câu diễn biến chính để phục vụ load context sau này]
  (Nội dung chương triển khai từ kế hoạch cảnh...)
  ```
- **Quy tắc văn phong & continuity bắt buộc:**
  - Tôn trọng chấn thương: Nhân vật bị thương không thực hiện động tác mạnh bằng chi bị thương mà không có lý do.
  - Giữ kín bí mật: Nhân vật chưa được chia sẻ bí mật không được nói bóng gió hay hành động như thể đã biết.
  - Áp dụng triệt để [../../references/show-dont-tell.md](../../references/show-dont-tell.md): Khắc họa phản ứng cơ thể, kích hoạt ít nhất 3/5 giác quan, đối thoại đa tầng có subtext.

---

### Bước 5: Audit Độc Lập 4 Cấp Độ (Independent Continuity Audit)
- **Hành động:** Chạy lệnh kiểm tra văn phong và kiểm định continuity:
  ```powershell
  python manage_story.py check
  python manage_story.py memory --audit
  ```
- **Tiêu chuẩn hoàn tất (Completion Criterion):**
  Phân loại và xử lý phát hiện theo 4 cấp độ:
  - 🔴 **Lỗi nghiêm trọng (Critical):** Phá vỡ canon, timeline, đảo lộn nhân quả, bí mật lộ sai người, hoặc vật phẩm dịch chuyển vô căn cứ. **Bắt buộc sửa.**
  - 🟡 **Lệch đáng kể (Significant):** Suy yếu động cơ nhân vật, lệch nhịp điệu quá mức. **Khuyến nghị sửa.**
  - 🟢 **Lệch mềm (Soft):** Biến thiên độ dài câu, tỷ lệ thoại. Cân nhắc điều chỉnh nếu cần.
  - 🎨 **Lựa chọn nghệ thuật (Artistic Choice):** Phép ẩn dụ, dòng ý thức, giọng điệu đặc trưng có chủ ý. **Bảo toàn nguyên vẹn.**

---

### Bước 6: Sửa Chữa Có Kiểm Soát (Controlled Repair)
- Sửa trực tiếp các lỗi Critical và Significant đã xác minh vào `draft.md`.
- Chạy lại `python manage_story.py memory --audit` để xác nhận lỗi đã giải quyết và không phát sinh lỗi mới.
- Tuyệt đối không chỉnh sửa lặp vô hạn làm mất đi tính tự nhiên của văn chương.

---

### Bước 7: Lưu Trữ An Toàn & Cập Nhật Bộ Nhớ (Save & Memory Update)
- **Hành động:** Chạy lệnh lưu:
  ```powershell
  python manage_story.py save
  ```
- **Tiêu chuẩn hoàn tất (Completion Criterion):**
  - Console thông báo `[SUCCESS]`, file chương được ghi nguyên tử vào `chapters/chapter_XXXX.md`.
  - Bản nháp cũ được lưu trữ tự động vào `chapters/.draft_backups/`.
  - Sự kiện chương mới được tự động ghi nhận vào Narrative Memory Timeline (`events.json`).
  - Cập nhật các thay đổi trạng thái nhân vật / chuyển giao vật phẩm bằng lệnh `manage_story.py memory` nếu có diễn biến lớn.
  - *Nguyên tắc bảo vệ dữ liệu:* Nếu lệnh `save` thất bại, `draft.md` được giữ nguyên 100%, không cập nhật Canon bằng nội dung chương chưa lưu.
  hoặc soạn `/story-summary --from <N> --to <M>` vào `draft.md` rồi chạy `save`.
