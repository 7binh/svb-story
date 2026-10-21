---
name: story-flow
description: "Trợ lý sáng tác và quản lý tiểu thuyết theo định hướng tác giả (Author-Led). Kích hoạt bằng lệnh /story-flow hoặc /story-write. Vòng lặp viết truyện tối ưu token, đề cương thích ứng linh hoạt, gợi ý rẽ nhánh cốt truyện, theo dõi phục bút và tích hợp bộ công cụ kiểm duyệt chất lượng từ .agents."
---

# SKILL: StoryFlow — Hệ Thống Sáng Tác & Quản Trị Tiểu Thuyết

Lệnh kích hoạt: `/story-flow` (hoặc `/story-write`).

StoryFlow kết hợp triết lý **Tác giả nắm quyền đạo diễn** (từ `agent_story_writer`) với **kỷ luật đề cương, bộ lọc chất lượng và công cụ vệ tinh** (từ `.agents`), giúp AI viết truyện có hồn, đúng hướng và không bị sa lầy vào văn mẫu máy móc.

---

## 🎯 NGUYÊN TẮC CỐT LÕI (Leading Words)

1. **Author-Led (Tác giả làm chủ)**: AI mở rộng và trau chuốt dựa trên đoạn test, ý tưởng thô hoặc nháp trực tiếp của tác giả; không tự ý bẻ lái câu chuyện.
2. **Token-Tight Context (Tiết kiệm ngữ cảnh)**: Tuyệt đối không đọc tràn lan toàn bộ các chương cũ. Chỉ đọc tóm tắt lớn, tóm tắt ngắn (brief), và duy nhất 1 chương liền kề.
3. **Adaptive Outline (Đề cương thích ứng)**: Duy trì mục tiêu của từng quyển (Arc) và kế hoạch 3-5 chương tiếp theo. Nếu tác giả bí ý, AI đề xuất 3 nhánh rẽ thay vì tự biên tự diễn.
4. **Anti-Slop Quality Gate**: Áp dụng triệt để bộ lọc dấu câu và quét mẫu câu lặp AI từ `.agents` (`scripts/check-ai-patterns.js`).

---

## 📂 QUẢN LÝ DỰ ÁN & ĐA TÁC PHẨM

Mọi tác phẩm nằm tại `stories/<story_id>/`. File `active_story.json` lưu định danh truyện đang viết.

- **Xem danh sách truyện**: `python manage_story.py stories`
- **Chọn truyện làm việc**: `python manage_story.py select --id <story_id>`
- **Khởi tạo truyện mới**: `python manage_story.py init --title "..." --author "..." [--id "slug"]`

---

## 🔄 QUY TRÌNH SÁNG TÁC 5 BƯỚC

### Bước 1: Nạp Ngữ Cảnh & Mục Tiêu Đề Cương
Trước khi viết, thực thi lệnh:
```powershell
python manage_story.py context
```
- Nắm nội dung `rolling_summary.txt`, `character_bible.json`, `lorebook.json`.
- Đọc brief các chương trung gian trên console (không mở file chương lẻ).
- Đọc toàn văn duy nhất chương liền trước (Chương N) để bắt nhịp hành văn.
- Nắm mục tiêu đề cương chương tiếp theo và danh sách phục bút (foreshadow) chưa giải quyết.

---

### Bước 2: Nhận Đề Cương Hoặc Gợi Ý Rẽ Nhánh (Khi Cần)
- Nếu tác giả đã có ý tưởng: Tác giả ghi vào nháp hoặc yêu cầu AI triển khai.
- Nếu tác giả chưa rõ hướng đi: AI đọc [references/plot-branching.md](references/plot-branching.md) và đề xuất **3 nhánh rẽ rõ rệt**:
  - *Nhánh A (Action)*: Đẩy cao xung đột, nguy cơ ập đến.
  - *Nhánh B (Emotion)*: Giãn nhịp, đối thoại riêng tư, đào sâu nội tâm.
  - *Nhánh C (Twist)*: Lật mở phục bút hoặc bí mật từ Lorebook.
  *(Chờ tác giả chọn nhánh trước khi chấp bút).*

---

### Bước 3: Soạn Thảo Bản Nháp Đa Năng
Nội dung nháp được ghi vào `stories/<story_id>/chapters/draft.md`.

#### Cú pháp Annotation Routing ở dòng đầu:
1. **Viết chương mới (Bắt buộc /story-brief ở dòng 2)**:
   ```markdown
   /story-title Tên Chương Ở Dòng Này
   /story-brief Tóm tắt 1-2 câu về sự kiện mấu chốt để phục vụ load ngữ cảnh sau này
   (Nội dung chương truyện triển khai tại đây...)
   ```
2. **Cập nhật đề cương**:
   ```markdown
   /story-outline
   ## Mục tiêu Arc 2...
   - Chương 6: ...
   ```
3. **Ghi nhận phục bút (Manh mối/Nút thắt)**:
   ```markdown
   /story-foreshadow --clue "Bức thư của phụ thân" --chapter 5
   Lâm Phong tìm thấy bức thư giấu dưới đáy rương có dấu niêm phong màu đỏ.
   ```
4. **Giải quyết phục bút**:
   ```markdown
   /story-foreshadow --clue "Bức thư của phụ thân" --resolve --chapter 12
   Lâm Phong đã mở bức thư và biết sự thật về huyết mạch gia tộc.
   ```
5. **Cập nhật nhân vật & Lorebook**:
   - Nhân vật: `/story-character --name "<Tên>" --chapter <N>`
   - Bối cảnh: `/story-lore --entry "<Tên mục>" --chapter <N>`
6. **Tóm tắt mốc (Mỗi 10 chương)**:
   - `/story-summary --from <N> --to <M>`

*(Hỗ trợ cả dạng ngắn: `/Title`, `/Brief`, `/Outline`, `/Foreshadow`, `/Character`, `/Lore`, `/Summary`)*

---

### Bước 4: Kiểm Soát Chất Lượng Văn Phong (Quality Gate từ .agents)
Trước khi lưu, chạy lệnh tự động kiểm tra:
```powershell
python manage_story.py check
```
Lệnh này tự động kích hoạt bộ script của `.agents`:
1. `scripts/normalize-punctuation.js`: Chuẩn hóa dấu câu, đối thoại, dấu ngoặc kép.
2. `scripts/check-ai-patterns.js`: Quét và báo động các cấu trúc câu văn mẫu máy móc (AI-slop).
Đồng thời đối chiếu [references/show-dont-tell.md](references/show-dont-tell.md) để đảm bảo chiều sâu cảm xúc.

---

### Bước 5: Lưu Trữ Tự Động
Chạy lệnh lưu:
```powershell
python manage_story.py save
```
Console in ra thông báo `[SUCCESS]`, file chương được lưu vào `chapters/`, `story.json` được cập nhật, và file `draft.md` được reset.

---

## 🌐 TÍCH HỢP CÔNG CỤ TỪ .AGENTS

Hệ thống tích hợp trực tiếp các công nghệ mạnh nhất từ kho `.agents`:

1. **Dashboard Trực Quan (Web UI)**:
   ```powershell
   python manage_story.py dashboard
   ```
   Mở giao diện Web trên trình duyệt xem cây thư mục, đọc duyệt chương, tra cứu nhân vật và bối cảnh.
2. **Công thức thể loại chuyên sâu**:
   Truy cập thư mục [references/genre-styles/](references/genre-styles/) (chứa các công thức: Huyền huyễn, Đô thị, Trinh thám, Kinh dị...).
3. **Hệ sinh thái vệ tinh**:
   - `/story-review`: Thẩm định đối kháng đa vai (Logic, Nhịp điệu, Tính cách nhân vật).
   - `/story-cover`: Thiết kế bìa tiểu thuyết AI.
   - `/story-scan`: Quét xu hướng và bảng xếp hạng truyện hot trên thị trường.
   - `/story-import`: Nghịch đảo file text truyện cũ thành dữ liệu cấu trúc chuẩn.

---

## 🛠️ THAM CHIẾU LỆNH NHANH (CLI REFERENCE)

| Lệnh CLI | Công dụng |
|---|---|
| `python manage_story.py context` | Lấy toàn bộ ngữ cảnh tối ưu token cho chương tiếp theo |
| `python manage_story.py save` | Quét nháp `draft.md` và tự động lưu/phân loại theo Annotation |
| `python manage_story.py check` | **[.agents tool]** Quét lỗi văn mẫu AI và chuẩn hóa dấu câu nháp |
| `python manage_story.py dashboard` | **[.agents tool]** Mở giao diện Web quản lý truyện trên trình duyệt |
| `python manage_story.py outline` | Hiển thị đề cương hiện tại |
| `python manage_story.py foreshadow` | Liệt kê tất cả phục bút đang mở (chưa giải) |
| `python manage_story.py list` | Danh sách các chương và trạng thái file |
| `python manage_story.py status` | Xem thông tin tổng quan của tác phẩm |
