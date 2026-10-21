---
name: story-cover
description: "Thiết kế prompt và tạo bìa tiểu thuyết AI chuyên nghiệp dựa trên metadata và không khí của tác phẩm. Kích hoạt: /story-cover, 'tạo bìa', 'làm bìa truyện', 'thiết kế bìa', 'vẽ bìa'."
---

# /story-cover: Thiết Kế Bìa Tiểu Thuyết AI

Tự động trích xuất thể loại, nhân vật chính và phong cách nghệ thuật từ dự án truyện để tạo ra các prompt sinh ảnh bìa chuyên nghiệp (tương thích Midjourney, DALL-E, Stable Diffusion hoặc Imagen).

---

## 🎨 QUY TRÌNH THỰC HIỆN

### Bước 1: Trích Xuất Dữ Liệu Tác Phẩm
AI đọc `stories/<active_story_id>/story_config.json`, `character_bible.json` và `outline.md` để xác định:
- **Tên truyện:** Tiêu đề tác phẩm.
- **Thể loại:** Tiên hiệp, Đô thị, Huyền huyễn, Trinh thám, Kinh dị...
- **Nhân vật tiêu điểm:** Ngoại hình, thần thái, vũ khí hoặc linh thú đi kèm.
- **Tông màu chủ đạo:** U tối huyền bí, rực rỡ kim sắc, lạnh lẽo cô độc, hay ấm áp hoài niệm.

---

### Bước 2: Tạo Bộ Prompt Chuẩn Quốc Tế
AI sẽ cung cấp cho bạn:
1. **Prompt tiếng Anh chi tiết (Full Prompt):** Tối ưu cho AI Art Generator (Midjourney v6, Stable Diffusion XL...) bao gồm góc máy, ánh sáng điện ảnh, bố cục chữ tiêu đề (*typography placement*), tỷ lệ khung hình chuẩn tiểu thuyết (`--ar 2:3`).
2. **Bố cục gợi ý cho bìa sách:**
   - Vị trí đặt Tiêu đề (Header/Footer).
   - Vị trí đặt Tên tác giả.
   - Điểm nhấn thị giác chính (Focal point).
