---
name: story-write
description: "Quy trình sáng tác tương tác từng bước (Author-Led Writing) gồm 7 bước khép kín. Hỗ trợ viết chương mới, mở rộng phân cảnh, viết khám phá không đề cương (pantser), chỉnh sửa cục bộ không ghi đè, và bám sát Style Profile cùng Narrative Memory. Kích hoạt: /story-write, 'viết chương', 'tiếp tục viết', 'mở rộng nháp', 'chấp bút', 'sửa đoạn này'."
---

# /story-write: Quy Trình Sáng Tác Tương Tác 7 Bước (Author-Led)

Quy trình sáng tác tương tác đồng hành giữa tác giả và AI Agent, tối ưu hóa sự cân bằng giữa cảm hứng sáng tạo và tính nhất quán logic chặt chẽ của tiểu thuyết.

---

## 🎯 CÁC TÌNH HUỐNG SÁNG TÁC ĐƯỢC HỖ TRỢ

Hệ thống linh hoạt đáp ứng mọi phương thức tác nghiệp:
1. **Viết theo đề cương chuẩn (Plotter Mode):** Có sẵn mục tiêu chương trong `outline.md` và Style Profile; AI nạp ngữ cảnh và bám sát tiến độ.
2. **Viết khám phá không đề cương (Pantser Mode):** Tác giả chỉ có một ý tưởng khởi đầu hoặc muốn để diễn biến tự nhiên hình thành. AI giúp định hình xung đột tại chỗ và cập nhật ngược lại đề cương/bộ nhớ sau khi viết xong.
3. **Mở rộng / Chấp bút từ ý tưởng thô:** Tác giả đưa vài dòng tóm tắt; AI phát triển thành văn xuôi giàu cảm giác và nhịp điệu.
4. **Chỉnh sửa / Viết lại cục bộ một phân cảnh:** Viết lại một đoạn cao trào hoặc đối thoại mà không làm xáo trộn toàn bộ chương hoặc các chương khác.
5. **Tiếp nhận phản hồi & Bảo toàn Canon:** Khi tác giả yêu cầu sửa đổi, AI tiếp thu tinh tế mà không làm sụp đổ các dữ kiện đã xác lập (quy tắc thế giới, chấn thương đang mang, bí mật chưa lộ).

---

## 🔄 VÒNG LẶP SÁNG TÁC 7 BƯỚC (7-STEP WRITING PIPELINE)

### Bước 1: Hiểu Mục Tiêu Cảnh / Chương (Goal & Intent Understanding)
- **Nếu đã có đề cương (`outline.md`):** Đọc mục tiêu cụ thể của chương tiếp theo và vị trí trong mạch truyện (Arc).
- **Nếu viết khám phá (Pantser):** Xác định ngay trọng tâm của phân cảnh sắp viết:
  * Ai đang chủ động?
  * Biến cố kích hoạt cảnh này là gì?
  * Đích đến cảm xúc của phân đoạn này là gì?
- **Xác định các bất biến (Invariants) bắt buộc bảo toàn:**
  * Quy tắc thế giới trong `summaries/canon.md` (hoặc `canon.json`).
  * Trạng thái thể chất/chấn thương trong `summaries/characters.md` (hoặc `characters_state.json`).
  * Bí mật chưa đến lúc lộ trong Ma trận bí mật (`knowledge.json`).

---

### Bước 2: Hoạch Định Kế Hoạch Cảnh (Scene Planning)
Trước khi viết câu chữ đầu tiên, thiết lập 5 yếu tố khung:
1. **POV & Nhân vật hiện diện:** Ai là người quan sát và cảm nhận? Ai cùng có mặt tại hiện trường?
2. **Điểm bắt đầu & Điểm kết thúc:** Nhân vật thay đổi gì về thể trạng, cảm xúc, vật phẩm hoặc nhận thức giữa đầu và cuối cảnh?
3. **Mâu thuẫn & Trở lực:** Xung đột chính là đối kháng trực diện, nghi ngờ ngầm, hay áp lực thời gian?
4. **Kiểm soát thông tin & Bí mật:** Chi tiết nào được phép bật mí? Chi tiết nào tuyệt đối phải giấu kín với người nghe?
5. **Nhịp điệu chủ đạo:** Cảnh giao tranh (câu ngắn, dồn dập, động từ mạnh) hay cảnh lắng đọng (câu dài, giàu giác quan, đối thoại nhiều subtext)?

---

### Bước 3: Truy Xuất Ngữ Cảnh 5 Lớp (Narrative Memory Retrieval)
- **Phương thức 1 (Native Markdown - Khuyến nghị cho Agent IDE):**
  Agent đọc trực tiếp các file bản chiếu:
  - `summaries/outline.md`: Mục tiêu chương tiếp theo.
  - `summaries/characters.md`: Tiến trình tâm lý, chấn thương hiện tại, túi đồ vật phẩm.
  - `summaries/timeline.md`: Trục thời gian nhân quả và di chứng gần nhất.
  - `summaries/canon.md`: Chân lý thế giới và danh sách tranh chấp mở.
- **Phương thức 2 (CLI Execution):**
  ```powershell
  python manage_story.py context
  ```
- **Tiêu chuẩn hoàn tất (5 Layers):**
  - **Lớp A (Core Context):** Nắm vững mục tiêu chương và chân lý thế giới.
  - **Lớp B (Story Memory):** Nắm vững các vết thương thể xác chưa lành, vật phẩm đang giữ, và ai biết bí mật gì.
  - **Lớp C (Disputes):** Nắm các mâu thuẫn mở chưa được giải quyết.
  - **Lớp D (Style Context):** Nắm các quy tắc Style Profile đang kích hoạt (độ dài câu, giác quan ưu tiên, khẩu khí).
  - **Lớp E (Recent Beat):** Đọc kỹ 3-5 đoạn văn cuối của chương liền trước để bắt nhịp cảm xúc mượt mà.

---

### Bước 4: Chấp Bút Văn Xuôi (Prose Drafting & Voice Execution)

#### Chế độ A: Native Markdown Direct (Agent IDE)
- Tạo hoặc chỉnh sửa trực tiếp file `chapters/chapter_XXXX.md` (ví dụ: `chapters/chapter_0005.md`).
- Cấu trúc chuẩn của một chương:
  ```markdown
  # Chương X: [Tên Chương]
  <!-- brief: Tóm tắt 1-2 câu diễn biến then chốt phục vụ nạp ngữ cảnh sau này -->

  (Văn xuôi triển khai từ Kế hoạch cảnh...)
  ```

#### Chế độ B: CLI Staging (Dành cho tác giả dùng Terminal)
- Soạn thảo vào file `chapters/draft.md`:
  ```markdown
  /story-title [Tên Chương]
  /story-brief [Tóm tắt 1-2 câu diễn biến then chốt]
  (Văn xuôi triển khai từ Kế hoạch cảnh...)
  ```

#### Kỹ thuật văn phong bắt buộc trong từng đoạn văn:
- **Tôn trọng vết thương cũ:** Nhân vật bị gãy tay hoặc nội thương không được vung kiếm bằng tay đau mà không có biểu hiện đau đớn dữ dội.
- **Bảo toàn Dramatic Irony (Hiểu lầm kịch tính):** Nhân vật có quyền tin sai sự thật; hành động của họ phải phản ánh niềm tin của họ, không phải sự thật toàn tri của tác giả.
- **Áp dụng Show, Don't Tell:** Hữu hình hóa cảm xúc qua phản ứng cơ thể (quai hàm nghiến chặt, lồng ngực đập thình thịch); kích hoạt ít nhất 3/5 giác quan; đan cài các nhịp dừng (beat) trong đối thoại.

---

### Bước 5: Audit Độc Lập 4 Cấp Độ (Independent Continuity & Slop Audit)
Chạy kiểm tra cơ học định lượng và kiểm định logic bộ nhớ:
- **Nếu viết trực tiếp (Native Markdown):**
  ```powershell
  python manage_story.py check --file chapters/chapter_XXXX.md
  python manage_story.py memory --audit --file chapters/chapter_XXXX.md
  ```
- **Nếu viết qua staging (`draft.md`):**
  ```powershell
  python manage_story.py check
  python manage_story.py memory --audit
  ```
- **Tiêu chuẩn phân loại phát hiện (4 Tiers):**
  - 🔴 **Lỗi nghiêm trọng (Critical):** Phá vỡ canon, chấn thương biến mất kỳ lạ, vật phẩm tự dịch chuyển, bí mật lộ sai người. **Bắt buộc sửa.**
  - 🟡 **Lệch đáng kể (Significant):** Động cơ nhân vật yếu đi, nhịp điệu quá vội vàng, thiếu tương tác giác quan. **Khuyến nghị sửa.**
  - 🟢 **Lệch mềm (Soft):** Biến thiên độ dài câu hoặc tỷ lệ thoại. Cân nhắc tùy hoàn cảnh.
  - 🎨 **Lựa chọn nghệ thuật (Artistic Choice):** Phép ẩn dụ, dòng ý thức, giọng văn đặc trưng có chủ đích. **Tuyệt đối bảo toàn, không sửa máy móc.**

---

### Bước 6: Sửa Chữa Có Kiểm Soát (Controlled Repair)
- Sửa trực tiếp các lỗi Critical và Significant đã xác nhận vào file chương hoặc bản nháp.
- Chạy lại lệnh audit để xác nhận không còn lỗi kỹ thuật và không làm phát sinh lỗi mới.
- Dừng lại ngay khi các lỗi nghiêm trọng đã được giải quyết để giữ lại nét văn phong tự nhiên.

---

### Bước 7: Lưu Trữ An Toàn & Đồng Bộ Narrative Memory
- **Nếu dùng Native Markdown:**
  - File chương đã nằm sẵn tại `chapters/chapter_XXXX.md`.
  - Cập nhật sự kiện chương vào Causal Timeline:
    ```powershell
    python manage_story.py memory --add-event --chapter X --title "[Tên sự kiện]" --summary "[Tóm tắt biến cố chính]"
    ```
  - Cập nhật trạng thái nhân vật / vật phẩm nếu có chuyển giao:
    ```powershell
    # Ví dụ: nếu có vật phẩm chuyển giao trong chương
    python manage_story.py memory --add-fact --subject "[Nhân vật]" --predicate "trạng_thái" --object "[Bị thương/Lên cấp]" --chapter X
    ```
  - Lệnh trên tự động đồng bộ lại các bản chiếu `summaries/characters.md`, `summaries/timeline.md`, và `summaries/canon.md`.
- **Nếu dùng CLI Staging:**
  - Chạy lệnh lưu:
    ```powershell
    python manage_story.py save
    ```
  - Hệ thống tự động sao lưu bản nháp vào `chapters/.draft_backups/`, ghi nguyên tử vào `chapters/chapter_XXXX.md`, đồng bộ Narrative Memory và reset `draft.md` an toàn.
- **Nguyên tắc bảo vệ dữ liệu:** Không bao giờ xóa bản nháp hoặc ghi đè chương cũ nếu thao tác lưu gặp lỗi.
