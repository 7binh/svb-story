---
name: story-flow
description: "Orchestrator điều phối toàn trình chu trình sáng tác StoryFlow (context → draft → quality check → save) dành cho AI Agent. Kích hoạt: /story-flow, 'viết toàn trình', 'quy trình toàn trình', 'tự hành viết truyện'."
---

# /story-flow: Điều Phối Toàn Trình Sáng Tác Tự Hành (Orchestrator)

Đóng vai trò là **Orchestrator toàn trình** liên kết các khâu sáng tác thành một chu trình liên tục khép kín, tối ưu hóa ngữ cảnh và đảm bảo an toàn dữ liệu tuyệt đối (không âm thầm ghi đè hay xóa bản nháp khi có lỗi).

> **Phân định phạm vi:**
> - Dùng `/story-write` khi tác giả muốn tương tác, duyệt và tinh chỉnh từng bước một.
> - Dùng `/story-flow` khi muốn AI điều phối toàn bộ chu trình 5 bước theo mục tiêu chương đã định.

---

## 🎯 NGUYÊN TẮC CỐT LÕI (Leading Words)

1. **Tight-Context**: Chỉ nạp tóm tắt cuốn chiếu, brief các chương trung gian, và duy nhất chương $N$ liền trước.
2. **Safe-Drafting**: Luôn tạo bản sao lưu trong `chapters/.draft_backups/` trước khi reset file nháp `draft.md`.
3. **Style-Enforced**: Tự động áp dụng Style Profile đang active (ngắn/dài, giác quan, khẩu khí) và đối chiếu với [../../references/show-dont-tell.md](../../references/show-dont-tell.md).
4. **Honest Quality Gate**: Phân biệt rõ kết quả kiểm tra tự động (`manage_story.py check`) với đánh giá định tính của AI; không bao giờ báo pass giả.

---

## 🔄 CHU TRÌNH ĐIỀU PHỐI 5 BƯỚC (END-TO-END PIPELINE)

```mermaid
flowchart TD
    A["Bước 1: Nạp Ngữ Cảnh (python manage_story.py context)"] --> B["Bước 2: Chuẩn Bị Đề Cương & Nhánh Rẽ"]
    B --> C["Bước 3: Soạn Thảo Bản Nháp Đa Năng (draft.md)"]
    C --> D["Bước 4: Kiểm Soát Chất Lượng (python manage_story.py check)"]
    D -- "Có lỗi hoặc Slop" --> E["Sửa Chữa Trực Tiếp Bản Nháp"]
    E --> D
    D -- "Đạt Chuẩn" --> F["Bước 5: Lưu Trữ & Index (python manage_story.py save)"]
    F --> G["Cập Nhật Nhân Vật / Bối Cảnh / Tóm Tắt Mốc"]
```

### Bước 1: Nạp Ngữ Cảnh 5 Lớp & Kiểm Tra Trạng Thái
- **Thực thi:**
  ```powershell
  python manage_story.py context
  ```
- **Side effects:** Chỉ đọc dữ liệu, không làm thay đổi trạng thái file.
- **Tiêu chuẩn hoàn tất:**
  1. Nắm Lớp A (Mục tiêu chương $N+1$, quy tắc thế giới) & Lớp B (Sự kiện nhân quả, chấn thương, vật phẩm, bí mật).
  2. Nắm Lớp C (Mâu thuẫn tranh chấp đang mở) & Lớp D (Style Profile rules & giới hạn suy luận).
  3. Nắm Lớp E (Đoạn kết chương liền trước $N$ để bắt đúng mạch cảm xúc).

---

### Bước 2: Hoạch Định Mạch Truyện & Đề Cương
- Đối chiếu mục tiêu chương trong `outline.md`.
- Nếu cần gợi ý hướng phát triển, tham khảo [../../references/plot-branching.md](../../references/plot-branching.md) theo 3 nhánh chuẩn: Action (Leo thang) / Emotion (Nội tâm) / Twist (Khúc quanh).

---

### Bước 3: Soạn Thảo Bản Nháp Đa Năng (draft.md)
- Soạn thảo trực tiếp vào `stories/<id>/chapters/draft.md`.
- **Cú pháp bắt buộc dòng 1 và 2:**
  ```markdown
  /story-title [Tên Chương Mới]
  /story-brief [Tóm tắt 1-2 câu sự kiện then chốt phục vụ load ngữ cảnh sau này]
  (Nội dung chương triển khai tại đây...)
  ```
- *Lưu ý an toàn:* Hệ thống hỗ trợ xử lý linh hoạt dòng trắng đầu file và hỗ trợ tham số `/Force` khi cần bỏ qua kiểm tra tính liên tục chương.
- *Ràng buộc logic:* Giữ kín bí mật đối với các nhân vật chưa biết; duy trì chấn thương thể chất đã ghi nhận.

---

### Bước 4: Chốt Chặn Kiểm Tra Kép (Quality Gate & Continuity Audit)
- **Thực thi:**
  ```powershell
  python manage_story.py check
  python manage_story.py memory --audit
  ```
- **Kiểm tra tự động:**
  - `check`: Quét lỗi dấu câu và cụm từ văn mẫu AI cấm kỵ qua module `vn_checker`.
  - `memory --audit`: Kiểm tra lỗi rò rỉ bí mật, chấn thương bị bỏ quên, hoặc vật phẩm dịch chuyển bất hợp lý.
- **Tự thẩm định văn phong:** Rà soát bản thảo theo 5 trục của Style Profile đang active. Phân biệt rõ lỗi Critical (bắt buộc sửa) với Artistic Choice (bảo toàn nguyên vẹn).

---

### Bước 5: Lưu Trữ Nguyên Tử & Cập Nhật Narrative Memory
- **Thực thi:**
  ```powershell
  python manage_story.py save
  ```
- **Side effects:**
  - Bản nháp cũ được tự động sao lưu tại `stories/<id>/chapters/.draft_backups/draft_YYYYMMDD_HHMMSS.md`.
  - Chương mới được ghi nguyên tử vào `stories/<id>/chapters/chapter_XXXX.md`.
  - File index `story.json` và cấu hình `story_config.json` được cập nhật.
  - Sự kiện chương mới được tự động ghi nhận vào Narrative Memory Timeline (`events.json`).
  - File `draft.md` được reset về trắng.
- **Xử lý sự cố:** Nếu quá trình ghi gặp lỗi, bản nháp `draft.md` được giữ nguyên vẹn 100%, không bị mất dữ liệu và Canon không bị sửa đổi.

---

## 🛠️ BẢNG THAM CHIẾU LỆNH ĐIỀU PHỐI (CLI COMMANDS)

| Lệnh CLI | Chức năng trong chu trình |
|---|---|
| `python manage_story.py context` | In toàn bộ ngữ cảnh tối ưu token cho chương tiếp theo |
| `python manage_story.py check` | Chạy chốt chặn kiểm soát văn phong và lọc slop AI |
| `python manage_story.py save` | Bóc tách nháp `draft.md`, sao lưu và lưu vào kho dữ liệu |
| `python manage_story.py append-summary --from X --to Y --text "..."` | Nối tóm tắt mốc vào `rolling_summary.txt` |
| `python manage_story.py style --list` | Tra cứu các profile văn phong (story & global) |
| `python manage_story.py outline` | Hiển thị đề cương hiện tại |
| `python manage_story.py foreshadow` | Liệt kê các manh mối và phục bút đang mở |
