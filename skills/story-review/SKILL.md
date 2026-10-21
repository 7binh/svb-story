---
name: story-review
description: "Thẩm định phản biện đối kháng đa vai sau khi viết chương hoặc hoàn thành một Arc (soát lỗi logic bối cảnh, nhịp điệu trần thuật và tính cách nhân vật). Kích hoạt: /story-review, 'thẩm định', 'soát lỗi', 'review chương', 'đánh giá chương'."
---

# /story-review: Thẩm Định Đối Kháng Đa Góc Nhìn

Đóng vai 3 độc giả khó tính để rà soát toàn diện bản thảo trước khi hoàn thiện chương hoặc chuyển sang Arc mới.

---

## 🎭 3 VAI THẨM ĐỊNH ĐỐI KHÁNG

Khi nhận lệnh `/story-review`, AI tiến hành thẩm định lần lượt theo 3 trục độc lập:

### 1. Vai 1: Chuyên Gia Logic & Tính Nhất Quán (Logic & Lore Reviewer)
- **Nhiệm vụ:** Đối chiếu nội dung chương với `character_bible.json` và `lorebook.json`.
- **Câu hỏi kiểm tra:**
  - Cảnh giới, năng lực hoặc bảo vật của nhân vật có bị "buff" vô lý hay mâu thuẫn với quy tắc đã đặt ra trước đó không?
  - Dòng thời gian, địa điểm di chuyển có hợp lý không?
  - Có chi tiết nào vi phạm các phục bút đang chờ trong `foreshadow.json` không?

---

### 2. Vai 2: Độc Giả Đại Chúng & Tiết Tấu (Pacing & Engagement Reviewer)
- **Nhiệm vụ:** Đánh giá nhịp điệu của câu chuyện và mức độ giữ chân độc giả.
- **Câu hỏi kiểm tra:**
  - Chương này có bị quá lê thê hoặc quá vội vàng không?
  - Điểm xung đột chính có đủ căng thẳng không?
  - Cuối chương có để lại điểm treo móc (cliffhanger/hook) khiến người đọc muốn bấm đọc tiếp chương sau không?

---

### 3. Vai 3: Nhà Phê Bình Nhân Vật & Cảm Xúc (Character Voice & OOC Reviewer)
- **Nhiệm vụ:** Rà soát xem nhân vật có bị lệch tính cách (*Out Of Character - OOC*) không.
- **Câu hỏi kiểm tra:**
  - Lời thoại của nhân vật có đúng khẩu khí và vị thế của họ không?
  - Phản ứng tâm lý trước biến cố có chân thật và tương xứng với quá khứ của nhân vật không?

---

## 📋 MẪU BÁO CÁO THẨM ĐỊNH (OUTPUT FORMAT)
AI xuất báo cáo ngắn gọn theo cấu trúc:
- **Điểm sáng:** 1-2 điểm làm tốt nhất (cảm xúc, nhịp văn, đối thoại).
- **Lỗ hổng cần sửa (Crucial Fixes):** Chỉ ra chính xác đoạn văn có vấn đề và đề xuất cách sửa cụ thể.
- **Điểm đánh giá chung:** Đạt / Cần chỉnh sửa trước khi lưu.
