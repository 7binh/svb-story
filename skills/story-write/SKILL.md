---
name: story-write
description: "Quy trình viết và mở rộng chương truyện tối ưu token theo định hướng tác giả. Kích hoạt: /story-write, /story-flow, 'viết chương', 'tiếp tục viết', 'mở rộng nháp'."
---

# /story-write: Quy Trình Viết & Mở Rộng Chương Truyện

Quy trình 5 bước khép kín phối hợp giữa tác giả, AI và công cụ CLI `manage_story.py`.

---

## 🔄 VÒNG LẶP SÁNG TÁC 5 BƯỚC

### Bước 1: Nạp Ngữ Cảnh Tối Ưu (Context Resolution)
- **Hành động:** Chạy lệnh:
  ```powershell
  python manage_story.py context
  ```
- **Tiêu chuẩn hoàn tất (Completion Criterion):**
  1. Đã đọc tóm tắt mốc trong `rolling_summary.txt`.
  2. Đã đọc brief tóm tắt ngắn trên console của các chương lẻ trung gian.
  3. Đã mở đọc toàn văn duy nhất chương liền trước (Chương N) để bắt nhịp hành văn.
  4. Đã nắm mục tiêu đề cương chương tiếp theo và phục bút đang chờ.
  5. Đã đọc mục [6] HỒ SƠ VĂN PHONG ĐANG ÁP DỤNG (profile_id, version, 3 dòng chỉ dẫn nhanh và đường dẫn file STYLE_PROFILE.md đầy đủ).

---

### Bước 2: Soạn Thảo Bản Nháp Đa Năng (Drafting & Style Enforcement)
- **Hành động:** Soạn thảo vào file `stories/<active_story_id>/chapters/draft.md`.
- **Cú pháp bắt buộc dòng 1 và 2:**
  ```markdown
  /story-title [Tên Chương Mới]
  /story-brief [Tóm tắt 1-2 câu diễn biến chính để phục vụ load context sau này]
  (Nội dung chương triển khai từ đoạn test/ý tưởng của tác giả...)
  ```
- **Quy tắc văn phong bắt buộc (Style Enforcement Pipeline):**
  - Tuân thủ bộ quy tắc trong file `STYLE_PROFILE.md` của profile đang active (nhịp câu, mật độ giác quan, tỷ lệ thoại vs tự sự).
  - Áp dụng triệt để [../../references/show-dont-tell.md](../../references/show-dont-tell.md) (hữu hình hóa cảm xúc qua phản ứng cơ thể, đối thoại đa tầng).

---

### Bước 3: Chốt Chặn Kiểm Tra Chất Lượng & Đối Chiếu 5 Trục (Quality Gate)
- **Hành động:** Chạy lệnh kiểm tra:
  ```powershell
  python manage_story.py check
  ```
- **Tiêu chuẩn hoàn tất (Completion Criterion):**
  1. Không còn lỗi dấu câu thô; không chứa các cụm từ sáo rỗng báo động bởi `scripts/check-ai-patterns.js`.
  2. Tự kiểm định bản nháp đã đáp ứng đủ 5 trục của Style Rules đang active (nhịp câu, giác quan, tỷ lệ thoại, khẩu khí, tu từ). Nếu phát hiện sai lệch, sửa trực tiếp vào nháp trước khi lưu.

---

### Bước 4: Lưu Trữ Tự Động (Save & Index)
- **Hành động:** Chạy lệnh lưu:
  ```powershell
  python manage_story.py save
  ```
- **Tiêu chuẩn hoàn tất (Completion Criterion):** Console in ra thông báo `[SUCCESS]`, file chương được lưu vào `chapters/chapter_XXXX.md`, `story.json` được cập nhật, và file `draft.md` được reset.

---

### Bước 5: Cập Nhật Dữ Liệu Sau Khi Viết (Post-Chapter Updates)
- Nếu có nhân vật mới/thay đổi trạng thái: Soạn `/story-character` vào `draft.md` rồi chạy `save`.
- Nếu có địa danh/bảo vật mới: Soạn `/story-lore` vào `draft.md` rồi chạy `save`.
- Nếu đạt mốc bội số của 10 chương: Soạn `/story-summary --from X --to Y` vào `draft.md` rồi chạy `save`.
