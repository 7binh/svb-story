---
name: story-cover
description: "Thiết kế ý tưởng nghệ thuật và tạo bộ prompt ảnh bìa tiểu thuyết AI chuyên nghiệp dựa trên metadata, nhân vật tiêu điểm và không khí tác phẩm. Kích hoạt: /story-cover, 'tạo bìa', 'làm bìa truyện', 'thiết kế bìa', 'vẽ bìa tiểu thuyết'."
---

# /story-cover: Thiết Kế Bìa Tiểu Thuyết AI Chuyên Nghiệp

Chuyên trách việc trích xuất linh hồn của tác phẩm (thể loại, nhân vật tiêu điểm, bối cảnh đặc trưng, tông màu và cảm xúc) để xây dựng bộ prompt sinh ảnh bìa tiểu thuyết chuẩn xác, sẵn sàng sử dụng cho Midjourney, Stable Diffusion XL, DALL-E 3 hoặc Imagen.

---

## 🎨 NGUYÊN TẮC THIẾT KẾ BÌA TIỂU THUYẾT (COVER DESIGN PRINCIPLES)

1. **Một điểm nhấn thị giác duy nhất (Focal Point):** Không nhồi nhét quá nhiều nhân vật hoặc chi tiết rườm rà. Chọn đúng 1 nhân vật chính (kèm vũ khí/linh thú đặc trưng) hoặc 1 biểu tượng bối cảnh quyền lực.
2. **Không gian bố cục cho Typography:** Luôn để lại khoảng trống an toàn (Negative Space) ở 1/3 phía trên (dành cho Tên truyện) và 1/4 phía dưới (dành cho Tên tác giả và Thể loại).
3. **Tỷ lệ khung hình tiểu thuyết chuẩn:** Mặc định sử dụng tỷ lệ `--ar 2:3` (chuẩn bìa sách xuất bản và bìa web novel quốc tế).
4. **Tương phản ánh sáng & Không khí:** Sử dụng ánh sáng điện ảnh (Cinematic Lighting) làm nổi bật nhân vật trên phông nền mờ ảo hoặc hoành tráng.

---

## 🛠️ QUY TRÌNH THỰC HIỆN 2 BƯỚC

### Bước 1: Trích Xuất Dữ Liệu Tác Phẩm
AI tự động đọc dữ liệu từ dự án:
- `stories/<slug>/story_config.json` hoặc `story.json`: Tên truyện, tên tác giả, thể loại.
- `summaries/characters.md` hoặc `character_bible.json`: Ngoại hình, trang phục, khí chất, vũ khí của nhân vật chính.
- `summaries/canon.md` hoặc `outline.md`: Bối cảnh chủ đạo (Tiên hiệp cổ trang, Cyberpunk hiện đại, Kỳ ảo u tối, Trinh thám hình sự).

*(Nếu người dùng chưa khởi tạo truyện hoặc muốn làm bìa theo ý tưởng tự do, AI sẽ hỏi nhanh 3 thông tin: Thể loại, Nhân vật/Vật phẩm trung tâm, và Tông màu mong muốn).*

---

### Bước 2: Xuất Bộ Prompt Chuẩn Quốc Tế & Bố Cục Thiết Kế

Khi hoàn tất, Agent cung cấp cho tác giả bản thiết kế hoàn chỉnh gồm:

#### 1. Bảng Thông Tin Thị Giác
- **Tiêu đề tác phẩm:** [Tên truyện tiếng Việt & Tên tiếng Anh/Pinyin nếu có]
- **Tác giả:** [Bút danh tác giả]
- **Thể loại:** [Tiên hiệp / Đô thị / Huyền ảo / Trinh thám...]
- **Tông màu chủ đạo:** [Ví dụ: Xanh đen huyền bí kết hợp ánh sáng kim sắc le lói]
- **Tâm trạng thị giác:** [Cô độc, hào hùng, bi tráng, hay ma mị]

#### 2. Bộ Prompt Tiếng Anh Tối Ưu (Prompt Generation)
- **Midjourney v6 Prompt:**
  ```text
  A cinematic book cover for a dark fantasy xianxia novel, featuring a solitary male swordsman standing atop a mist-covered cliff edge, dressed in flowing tattered dark robes, holding a faintly glowing ancient dao sword. Dramatic rim lighting, swirling spiritual aura, moonlit stormy clouds, photorealistic 8k, highly detailed digital painting, empty top space for title typography, empty bottom space for author name --ar 2:3 --v 6.0 --style raw
  ```
- **DALL-E 3 / Bing Image Creator Prompt:**
  ```text
  Book cover illustration for a fantasy novel. A lone male warrior with a determined expression standing on a rocky precipice surrounded by swirling fog. Dark blue and gold color palette, cinematic lighting, negative space at the top and bottom suitable for book cover text layout, vertical 2:3 ratio, epic atmosphere.
  ```
- **Stable Diffusion XL Prompt:**
  ```text
  masterpiece, best quality, highly detailed, novel book cover, solitary warrior, ancient sword, dramatic atmosphere, cinematic rim lighting, volumetric fog, dark palette, gold accents, rule of thirds, clean composition with negative space for typography, 8k resolution, trending on Artstation
  Negative prompt: text, watermark, signature, ugly, blurry, deformed anatomy, crowded background, lowres
  ```

#### 3. Hướng Dẫn Bố Cục Chữ (Typography Placement Guide)
- **Khu vực Tiêu đề (Header/Upper 30%):** Đặt tựa đề truyện bằng font chữ đậm, sắc sảo (với truyện tiên hiệp/hành động) hoặc mềm mại, uyển chuyển (với truyện tình cảm).
- **Điểm nhấn trung tâm (Middle 50%):** Nhân vật hoặc bảo vật tiêu điểm.
- **Khu vực Tác giả & Tagline (Lower 20%):** Bút danh tác giả viết gọn gàng, nhỏ hơn tiêu đề 3-4 lần, đặt cân đối ở góc dưới hoặc chính giữa mép dưới.
