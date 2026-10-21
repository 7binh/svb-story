---
name: story-review
description: "Thẩm định phản biện đối kháng đa vai sau khi viết chương hoặc hoàn thành một Arc (soát lỗi logic bối cảnh, nhịp điệu trần thuật và tính cách nhân vật). Kích hoạt: /story-review, 'thẩm định', 'soát lỗi', 'review chương', 'đánh giá chương'."
---

# /story-review: Thẩm Định Đối Kháng Đa Góc Nhìn

Đóng vai 3 độc giả khó tính để rà soát toàn diện bản thảo trước khi hoàn thiện chương hoặc chuyển sang Arc mới.

---

## 🎭 3 VAI THẨM ĐỊNH ĐỐI KHÁNG

Khi nhận lệnh `/story-review`, AI tiến hành thẩm định độc lập qua 3 lăng kính chuyên môn kết hợp chạy lệnh kiểm định tự động:
```powershell
python manage_story.py memory --audit
```

### 1. Vai 1: Chuyên Gia Logic, Canon & Continuity (Logic & Lore Reviewer)
- **Nhiệm vụ:** Đối chiếu nội dung chương với Story Canon, Timeline (`events.json`), và chấn thương/vật phẩm (`characters_state.json`).
- **Câu hỏi kiểm tra:**
  - Quy tắc thế giới và cảnh giới có bị phá vỡ không?
  - Dòng thời gian và quan hệ nhân quả có bị đảo lộn không?
  - Nhân vật có đang tự nhiên lành lặn vết thương cũ hoặc dùng lại vật phẩm đã mất không?
  - Có nhân vật nào hành xử/nói năng dựa trên bí mật mà họ chưa từng được biết không?

---

### 2. Vai 2: Độc Giả Đại Chúng & Tiết Tấu (Pacing & Engagement Reviewer)
- **Nhiệm vụ:** Đánh giá nhịp điệu của câu chuyện và mức độ giữ chân độc giả.
- **Câu hỏi kiểm tra:**
  - Chương này có bị quá lê thê hoặc quá vội vàng không?
  - Điểm xung đột chính có đủ căng thẳng và có nguyên nhân rõ ràng không?
  - Cuối chương có để lại điểm treo móc (cliffhanger/hook) kích thích tò mò không?

---

### 3. Vai 3: Nhà Phê Bình Nhân Vật & Cảm Xúc (Character Voice & Psychology Reviewer)
- **Nhiệm vụ:** Rà soát chiều sâu tâm lý, giọng điệu nhân vật và nguy cơ OOC (*Out Of Character*).
- **Câu hỏi kiểm tra:**
  - Khẩu khí của nhân vật có nhất quán với địa vị và bối cảnh của họ không?
  - Động cơ và phản ứng cảm xúc có bắt nguồn từ các biến cố trước đó hay bị khiên cưỡng?
  - Niềm tin của nhân vật (dù đúng hay sai) có được tôn trọng trong hành vi không?

---

## 📋 HỆ THỐNG PHÂN LOẠI 4 CẤP ĐỘ PHÁT HIỆN (4-TIER AUDIT RUBRIC)

Báo cáo thẩm định bắt buộc phân loại mọi phát hiện thành 4 cấp độ rõ ràng:

1. 🔴 **Lỗi nghiêm trọng (Critical):**
   - Phá vỡ canon, timeline, quan hệ nhân quả, rò rỉ bí mật sai nhân vật, mâu thuẫn trạng thái chấn thương/vật phẩm.
   - *Yêu cầu:* Bắt buộc chỉ ra bằng chứng (Chương X dòng Y) và sửa trước khi lưu chương.
2. 🟡 **Lệch đáng kể (Significant):**
   - Động cơ nhân vật bị suy yếu, nhịp điệu chuyển cảnh quá gắt, thiếu tương tác giác quan.
   - *Yêu cầu:* Khuyến nghị sửa đổi cụ thể.
3. 🟢 **Lệch mềm (Soft):**
   - Biến thiên tỷ lệ đối thoại / miêu tả, độ dài câu trung bình hơi lệch so với profile mẫu nhưng phù hợp cảnh.
   - *Yêu cầu:* Tùy chọn cân nhắc, không ép buộc.
4. 🎨 **Lựa chọn nghệ thuật hợp lệ (Artistic Choice):**
   - Các phép ẩn dụ, dòng ý thức, đảo trật tự kể chuyện có chủ đích nghệ thuật.
   - *Yêu cầu:* Tôn trọng và bảo toàn nguyên vẹn, không được sửa máy móc.

---

## 📋 MẪU BÁO CÁO THẨM ĐỊNH (OUTPUT FORMAT)
- **Điểm sáng:** 1-2 điểm làm tốt nhất (cảm xúc, đối thoại, nhịp văn).
- **Danh sách phát hiện:** Bảng phân loại [Critical / Significant / Soft / Artistic Choice] kèm trích dẫn văn bản và phương án đề xuất.
- **Kết luận:** Sẵn sàng lưu (Ready to save) / Cần chỉnh sửa (Needs repair).
