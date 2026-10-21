---
name: story-deslop
description: "Chuyên trách khử văn mẫu AI (AI-slop), chuẩn hóa dấu câu an toàn và nâng cao chất lượng văn phong theo nguyên tắc Show, Don't Tell. Kích hoạt: /story-deslop, 'khử văn mẫu', 'khử AI', 'tút lại văn', 'chỉnh văn phong'."
---

# /story-deslop: Bộ Lọc Khử Văn Mẫu AI & Trau Chuốt Văn Phong

Loại bỏ cảm giác máy móc, văn dịch thô và sáo rỗng trong các văn bản do AI sinh ra, trả lại sự tự nhiên và chiều sâu cảm xúc cho tiếng Việt.

> **Nguyên tắc an toàn (Guardrail):**
> - Quá trình khử slop chỉ nhắm vào lỗi kỹ thuật, từ ngữ sáo rỗng và nhịp câu máy móc.
> - Tuyệt đối không thay đổi sự kiện, POV, sự thật thế giới, niềm tin nhân vật, mối quan hệ hay quy tắc bối cảnh đã ghi nhận trong Story Canon.
> - Không áp đặt kiểm duyệt nội dung ngoài phạm vi kỹ thuật sáng tác.

---

## 🧹 QUY TRÌNH 3 BƯỚC KHỬ SLOP

### Bước 1: Quét Kỹ Thuật Tự Động (Native Quality Gate)
Chạy lệnh phân tích bản nháp `draft.md`:
```powershell
python manage_story.py check
```
- Module Python `scripts/vn_checker.py` tự động phát hiện khoảng trắng lỗi quanh dấu câu, ngoặc kép thoại chưa đóng, và đối chiếu danh mục cụm từ sáo rỗng AI.
- Nếu có script mở rộng, hệ thống kiểm tra chặt chẽ mã thoát và báo cáo trung thực nếu xảy ra lỗi.

---

### Bước 2: Thanh Lọc "Danh Sách Đen" Cụm Từ Sáo Rỗng
Đối chiếu trực tiếp với tài liệu [../../references/anti-slop.md](../../references/anti-slop.md):
- **Loại bỏ triệt để:** *"Không thể phủ nhận rằng...", "Bầu không khí bỗng ngưng đọng...", "Dường như có một tia phức tạp trong mắt..."*.
- **Cắt bỏ đoạn thuyết minh giả tạo ở cuối chương:** Thay thế các câu đúc kết triết lý vụng về bằng hành động thực tế hoặc câu hỏi mở.
- **Quy tắc cắt gọt 20%:** Nếu có 3 câu giải thích cảm xúc trừu tượng liên tiếp, xóa bớt 2 câu và giữ lại 1 câu hành động vật lý cụ thể.

---

### Bước 3: Nâng Cấp Theo Nguyên Tắc Show, Don't Tell
Đối chiếu tài liệu [../../references/show-dont-tell.md](../../references/show-dont-tell.md):
1. **Hữu hình hóa cảm xúc:** Thay vì viết "hắn rất tức giận", chuyển thành: quai hàm nghiến chặt, gân xanh nổi cộm trên mu bàn tay, hơi thở dồn dập.
2. **Kích hoạt ít nhất 3/5 giác quan:** Bổ sung mùi vị, nhiệt độ không gian, âm thanh nền (tiếng mưa rơi trên mái ngói, mùi tanh của bùn, ngọn gió rít qua kẽ cửa).
3. **Đối thoại đa tầng:** Thêm các nhịp dừng (beats), cái nhấp ngụm trà, ánh mắt lướt nhanh để câu thoại mang hàm ý ngầm.
