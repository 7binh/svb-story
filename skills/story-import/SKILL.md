---
name: story-import
description: "Nghịch đảo nhập truyện cũ (file văn bản thô nhiều chương) thành cấu trúc dữ liệu đa tác phẩm chuẩn của hệ thống StoryFlow. Kích hoạt: /story-import, 'nhập truyện', 'import truyện', 'phân tích truyện cũ'."
---

# /story-import: Nghịch Đảo Bản Thảo Truyện Cũ

Giúp bạn nạp một tác phẩm đã viết sẵn (dưới dạng file `.txt`, `.md` chứa hàng chục hoặc hàng trăm chương) vào hệ sinh thái StoryFlow mà không cần làm thủ công.

---

## 📥 QUY TRÌNH NGHỊCH ĐẢO DỮ LIỆU

Khi bạn cung cấp đường dẫn đến file truyện cũ hoặc paste nội dung:

### Bước 1: Khởi Tạo Dự Án Mới
AI chạy lệnh tạo truyện mới:
```powershell
python manage_story.py init --title "<Tên Truyện>" --author "<Tác Giả>" --id "<slug>"
```

### Bước 2: Bóc Tách & Tự Động Đánh Số Chương
- Tự động nhận diện ranh giới các chương dựa trên biểu thức chính quy (Regex): `Chương \d+`, `Hồi \d+`, `Chapter \d+`.
- Tách từng chương và lưu vào `stories/<slug>/chapters/chapter_XXXX.md`.
- Ghi nhận index chương vào file `stories/<slug>/story.json`.

### Bước 3: Trích Xuất Hồ Sơ & Tóm Tắt Khởi Đầu
- Tự động quét 5-10 chương đầu để nhận diện tên nhân vật chính, cập nhật sơ bộ vào `character_bible.json`.
- Ghi nhận các địa danh, thế lực xuất hiện vào `lorebook.json`.
- Tạo bản tóm tắt tích lũy ban đầu đưa vào `rolling_summary.txt`.

👉 Sau khi hoàn tất bước này, bạn có thể tiếp tục viết chương kế tiếp bằng lệnh `/story-write` hoàn toàn bình thường!
