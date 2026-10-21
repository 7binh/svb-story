---
name: story-deslop
description: "Chuyên trách khử văn mẫu AI (AI-slop), chuẩn hóa dấu câu và nâng cao chất lượng văn phong theo nguyên tắc Show, Don't Tell. Kích hoạt: /story-deslop, 'khử văn mẫu', 'khử AI', 'tút lại văn', 'chỉnh văn phong'."
---

# /story-deslop: Bộ Lọc Khử Văn Mẫu AI & Trau Chuốt Văn Phong

Loại bỏ cảm giác máy móc, văn dịch thô và sáo rỗng trong các văn bản do AI sinh ra, trả lại sự tự nhiên và chiều sâu cảm xúc cho tiếng Việt.

---

## 🧹 QUY TRÌNH 3 BƯỚC KHỬ SLOP

### Bước 1: Quét Tự Động Bằng Bộ Lọc Kỹ Thuật
Chạy lệnh phân tích bản nháp `draft.md`:
```powershell
python manage_story.py check
```
- Tự động sửa dấu câu, khoảng cách, ngoặc kép thoại qua `scripts/normalize-punctuation.js`.
- Bắt quả tang các cụm từ lặp và cấu trúc sáo rỗng qua `scripts/check-ai-patterns.js`.

---

### Bước 2: Thanh Lọc "Danh Sách Đen" Cụm Từ Sáo Rỗng
Đối chiếu trực tiếp với tài liệu [../../references/anti-slop.md](../../references/anti-slop.md):
- **Xóa bỏ triệt để:** *"Không thể phủ nhận rằng...", "Bầu không khí bỗng ngưng đọng...", "Dường như có một tia phức tạp trong mắt..."*.
- **Cắt bỏ đoạn thuyết minh giả tạo ở cuối chương:** Thay thế các câu đúc kết triết lý vụng về bằng hành động thực tế hoặc câu hỏi mở.

---

### Bước 3: Nâng Cấp Theo Nguyên Tắc Show, Don't Tell
Đối chiếu tài liệu [../../references/show-dont-tell.md](../../references/show-dont-tell.md):
1. **Hữu hình hóa cảm xúc:** Thay vì viết "hắn rất tức giận", chuyển thành: quai hàm nghiến chặt, gân xanh nổi cộm trên mu bàn tay, hơi thở dồn dập.
2. **Kích hoạt ít nhất 3/5 giác quan:** Bổ sung mùi vị, nhiệt độ không gian, âm thanh nền (tiếng mưa rơi trên mái ngói, mùi tanh của bùn, ngọn gió rít qua kẽ cửa).
3. **Đối thoại đa tầng:** Thêm các nhịp dừng (beats), cái nhấp ngụm trà, ánh mắt lướt nhanh để câu thoại mang hàm ý ngầm.
