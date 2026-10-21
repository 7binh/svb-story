---
name: story-write
description: "Quy trình viết và mở rộng chương truyện tối ưu token theo định hướng tác giả (Author-Led). Hỗ trợ cả Native Markdown trực tiếp và CLI Staging. Kích hoạt: /story-write, 'viết chương', 'tiếp tục viết', 'mở rộng nháp', 'chấp bút'."
---

# /story-write: Quy Trình Viết & Mở Rộng Chương Truyện Từng Bước

Quy trình sáng tác tương tác khép kín kết hợp giữa tác giả, AI Agent và các công cụ thực thi xác định (`manage_story.py`), thực thi Style Enforcement Pipeline và Narrative Memory trong từng phân cảnh.

Hệ thống hỗ trợ 2 chế độ tác nghiệp:
- **Chế độ 1: Native Markdown Direct (Mặc định cho AI Agent IDE như Antigravity / Claude Code)**: Đọc đề cương và bản chiếu Markdown trong `summaries/`, viết trực tiếp ra `chapters/chapter_XXXX.md`, kiểm tra bằng CLI tool xác định và đồng bộ sự kiện vào Memory.
- **Chế độ 2: CLI Staging (Dành cho Author-CLI)**: Soạn nháp trung gian qua `chapters/draft.md`, gắn thẻ `/story-title`, `/story-brief` và lưu tự động bằng lệnh `save`.

---

## 🔄 VÒNG LẶP SÁNG TÁC 7 BƯỚC (7-STEP WRITING PIPELINE)

### Bước 1: Hiểu Mục Tiêu Chương (Goal Understanding)
- Xác định rõ mục tiêu cốt truyện chương tiếp theo từ `outline.md` và vị trí trong Arc truyện hiện tại.
- Xác định những bất biến không được phép thay đổi ngoài ý muốn (quy tắc thế giới trong `summaries/canon.md`, chấn thương đang mang trong `summaries/characters.md`, bí mật chưa được lộ trong Secrets Matrix).

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
- **Cách 1 (Native Markdown):** Agent đọc trực tiếp các bản chiếu trong thư mục truyện:
  - `outline.md`: Đề cương phân chương.
  - `summaries/characters.md`: Tiến trình tâm lý, mục tiêu, chấn thương và vật phẩm nhân vật.
  - `summaries/timeline.md`: Trục thời gian nhân quả và di chứng từ các chương trước.
  - `summaries/canon.md`: Chân lý thế giới, Ma trận bí mật và các mâu thuẫn tranh chấp đang mở.
- **Cách 2 (CLI Token-Optimized):** Chạy lệnh:
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

#### Lựa chọn A — Viết Trực Tiếp Native Markdown (Khuyến nghị cho Agent IDE):
- Dùng công cụ `write_file` tạo trực tiếp file `chapters/chapter_XXXX.md` (ví dụ: `chapters/chapter_0005.md`).
- Cấu trúc đầu file chuẩn:
  ```markdown
  # Chương X: [Tên Chương]
  <!-- brief: Tóm tắt 1-2 câu diễn biến then chốt phục vụ nạp ngữ cảnh sau này -->

  (Nội dung văn xuôi triển khai từ kế hoạch cảnh...)
  ```

#### Lựa chọn B — Viết Qua Staging (Dành cho Author-CLI):
- Soạn thảo trực tiếp vào file `chapters/draft.md`:
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
- **Hành động:** Chạy lệnh kiểm tra văn phong định lượng và kiểm định continuity:
  - Nếu viết trực tiếp (Mode 1):
    ```powershell
    python manage_story.py check --file chapters/chapter_XXXX.md
    python manage_story.py memory --audit --file chapters/chapter_XXXX.md
    ```
  - Nếu viết qua staging (Mode 2):
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
- Sửa trực tiếp các lỗi Critical và Significant đã xác minh vào file chương / bản nháp.
- Chạy lại lệnh audit để xác nhận lỗi đã giải quyết và không phát sinh lỗi mới.
- Tuyệt đối không chỉnh sửa lặp vô hạn làm mất đi tính tự nhiên của văn chương.

---

### Bước 7: Lưu Trữ An Toàn & Đồng Bộ Narrative Memory
- **Nếu dùng Mode 1 (Native Markdown):**
  - File chương đã được lưu tại `chapters/chapter_XXXX.md`.
  - Cập nhật sự kiện chương vào Narrative Memory Timeline:
    ```powershell
    python manage_story.py memory --add-event --chapter X --title "[Tên sự kiện]" --summary "[Tóm lược biến cố]"
    ```
  - Lệnh trên sẽ tự động tái xuất bản chiếu Markdown sang `summaries/characters.md`, `summaries/timeline.md`, và `summaries/canon.md`!
  - Cập nhật số chương hiện tại trong cấu hình nếu cần:
    ```powershell
    python manage_story.py status
    ```
- **Nếu dùng Mode 2 (CLI Staging):**
  - Chạy lệnh lưu:
    ```powershell
    python manage_story.py save
    ```
  - Console thông báo `[SUCCESS]`, file chương được ghi nguyên tử vào `chapters/chapter_XXXX.md`.
  - Bản nháp cũ được lưu trữ tự động vào `chapters/.draft_backups/`.
  - Sự kiện chương mới tự động cập nhật vào `events.json` và đồng bộ Markdown projections.
  - *Nguyên tắc bảo vệ dữ liệu:* Nếu lệnh `save` thất bại, `draft.md` được giữ nguyên 100%, không cập nhật Canon bằng nội dung chương chưa lưu.
