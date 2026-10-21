---
name: story
description: "Trạm điều phối trung tâm cho hệ sinh thái viết truyện StoryFlow. Điều hướng giữa các skill viết, đề cương, khử văn mẫu, thẩm định, tạo bìa, import và khởi chạy Web Dashboard. Kích hoạt: /story, $story, /truyện, 'viết truyện', 'quản lý truyện', 'mở dashboard'."
---

# /story: Trạm Điều Phối Sáng Tác & Quản Trị Truyện

Đóng vai trò là **Router Skill** dẫn đường theo chuẩn `matt-writing-for-agents`: giúp tác giả và AI nhanh chóng định vị đúng công cụ cần dùng mà không gây tràn ngữ cảnh.

---

## 🧭 BẢNG ĐIỀU HƯỚNG TỔNG QUAN

| Nhu cầu của bạn | Lệnh kích hoạt trực tiếp | Chức năng chính |
|---|---|---|
| **Viết chương mới / Mở rộng nháp** | `/story-write` (hoặc `/story-flow`) | Vòng lặp 5 bước: context -> viết nháp -> check -> save. |
| **Học & Giải mã văn phong truyện mẫu** | `/story-study` | Phân tích 5 trục từ file, thư mục hoặc dán nháp; tạo Style Fingerprint & Rules. |
| **Lập đề cương / Gợi ý rẽ nhánh / Phục bút** | `/story-outline` | Quản lý mục tiêu từng Arc, gợi ý 3 nhánh rẽ, theo dõi manh mối. |
| **Khử văn mẫu AI / Chuẩn hóa câu từ** | `/story-deslop` | Lọc bỏ từ ngữ sáo rỗng, áp dụng Show-Don't-Tell và chiều sâu giác quan. |
| **Thẩm định phản biện đa góc nhìn** | `/story-review` | Soát lỗi logic bối cảnh, nhịp điệu (pacing) và tính cách nhân vật (OOC). |
| **Thiết kế ảnh bìa tiểu thuyết AI** | `/story-cover` | Tự động tạo prompt sinh ảnh bìa chuyên nghiệp từ metadata truyện. |
| **Nhập bản thảo cũ vào hệ thống** | `/story-import` | Phân rã file truyện cũ nhiều chương vào cấu trúc đa tác phẩm. |
| **Mở giao diện Web quản lý trực quan** | `python manage_story.py dashboard` | Khởi chạy máy chủ Web UI xem truyện trên trình duyệt. |

---

## 🛠️ THAO TÁC NHANH VỚI TÁC PHẨM (CLI QUICK ACTIONS)

- **Xem danh sách các bộ truyện:** `python manage_story.py stories`
- **Chọn bộ truyện làm việc:** `python manage_story.py select --id <slug>`
- **Khởi tạo truyện mới:** `python manage_story.py init --title "Tên Truyện" --author "Tác Giả" --genre "Thể Loại"`
- **Kiểm tra tiến độ & tình trạng:** `python manage_story.py status`
