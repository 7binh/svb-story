---
name: story-study
description: "Học và giải mã văn phong từ truyện mẫu (thư mục, file hoặc dán nháp). Kết hợp đo lường định lượng 5 trục (Style Engine 2.0.0) với phân tích văn học ngữ nghĩa của AI Agent; tạo và áp dụng Style Profile đa cấp độ (story & global). Kích hoạt: /story-study, 'học văn phong', 'nghiên cứu văn phong', 'học truyện mẫu', 'phân tích phong cách'."
---

# /story-study: Giải Mã Văn Phong Truyện Mẫu (Style Engine 2.0)

Chuyên trách việc **nghiên cứu, bóc tách và chuyển hóa văn phong** từ các tác phẩm mẫu thành hồ sơ phong cách (Style Profile) có thể kiểm chứng và tái lập, phục vụ sáng tác dài tập mà không sao chép nguyên văn tình tiết.

---

## 🎯 PHÂN ĐỊNH TRÁCH NHIỆM: AGENT LITERARY ANALYSIS & PYTHON METRICS

Hệ thống kết hợp sức mạnh phân tích ngữ nghĩa sâu của AI Agent với độ chuẩn xác toán học của Python:
1. **Agent trực tiếp đảm nhiệm (Phân tích Văn học & Ngữ nghĩa):**
   - Đọc và cảm nhận nhịp điệu, không khí và giọng điệu nghệ thuật của tác giả mẫu.
   - **Tách bạch phong cách vs Nội dung:** Nhận diện đâu là kỹ thuật kể chuyện (dồn dập, đối thoại ngầm, dùng giác quan) và đâu là nội dung câu chuyện riêng của tác phẩm mẫu (tên nhân vật, bối cảnh, võ công) để không sao chép tình tiết bản quyền.
   - Biên soạn file hướng dẫn sáng tác `STYLE_PROFILE.md` với các quy tắc vàng dễ hiểu cho con người và AI.
   - So sánh văn bản chương vừa viết với hồ sơ mẫu để đưa ra góp ý nâng tầm văn chương.
2. **Python `scripts/style_analyzer.py` đảm nhiệm (Đo lường Định lượng Xác định):**
   - Đếm chính xác số âm tiết (syllables), độ dài câu trung bình, và phân bổ câu ngắn/vừa/dài.
   - Thống kê tần suất dấu câu nhịp thở (chấm lửng `...`, gạch ngang `—`, cảm thán `!`, hỏi `?`).
   - Quét mật độ giác quan (Thị giác, Thính giác, Xúc giác, Khứu/Vị giác) trên 1.000 âm tiết.
   - Tính toán tỷ lệ hội thoại, độc thoại nội tâm và trần thuật hành động.
   - Định dạng và xác thực file `style_profile.json` theo đúng chuẩn **Style Profile Schema 2.0.0**.

---

## 📥 3 HÌNH THỨC CUNG CẤP TRUYỆN MẪU

### 1. Thư mục chứa nhiều truyện mẫu
Áp dụng khi bạn có kho tài liệu mẫu gồm nhiều file `.txt` hoặc `.md`:
```powershell
python manage_story.py style --learn ./samples/my-stories/ --profile my-style --scope story
```
*(Thêm `--scope global` nếu muốn đưa vào thư viện dùng chung cho tất cả các bộ truyện trong workspace).*

### 2. File truyện mẫu có sẵn
Áp dụng khi học trực tiếp từ 1 chương hoặc 1 trích đoạn sách:
```powershell
python manage_story.py style --learn ./samples/chapter-01.txt --profile kim-dung --scope global
```

### 3. Dán đoạn trích trực tiếp vào nháp (`draft.md`)
Áp dụng khi muốn học nhanh một đoạn văn tâm đắc (1.000 – 3.000 chữ):
1. Dán vào `stories/<slug>/chapters/draft.md`:
   ```markdown
   /story-study --profile <ten_profile> [--scope story|global]
   (Đoạn văn trích mẫu cần học dán tại đây...)
   ```
2. Chạy lệnh:
   ```powershell
   python manage_story.py save
   ```
- *Bảo vệ dữ liệu:* Đoạn trích mẫu trong `draft.md` được giữ nguyên trạng và bản sao được lưu an toàn tại `style_profiles/<ten_profile>/source_sample.txt`.

---

## 🔬 5 TRỤC BÓC TÁCH VĂN PHONG (STYLE DECOMPOSITION)

Hồ sơ văn phong được bóc tách và lưu theo **Schema 2.0.0**:

1. **Cấu trúc & Nhịp câu (Syntax & Rhythm):**
   - Đo lường theo âm tiết (syllable units): Câu ngắn (< 10 âm tiết), câu vừa (10–22 âm tiết), câu dài (> 22 âm tiết).
   - Tần suất các dấu câu tạo nhịp thở văn học (`...`, `—`, `!`, `?`).
2. **Mật độ Giác quan & Tả cảnh (Sensory Immersion):**
   - Đo lường mật độ 4 nhóm giác quan trên 1.000 âm tiết (Thị giác, Thính giác, Xúc giác/Cơ thể, Khứu/Vị giác).
   - Xác định giác quan chủ đạo và chức năng miêu tả (Show, Don't Tell).
3. **Tỷ lệ Phân bổ Nội dung (Content Distribution):**
   - Hỗ trợ thoại nhiều dòng và nhiều định dạng ngoặc thoại (`""`, `“”`, `「」`, `『』`, `—`).
   - Định lượng % Đối thoại vs Trần thuật/Hành động vs Độc thoại nội tâm.
4. **Khẩu khí & Tông giọng (Tone & Voice - Estimated):**
   - Gắn nhãn ước lượng: Dồn dập căng thẳng, Trầm tĩnh chậm rãi (Slow-burn), Kịch tính đối thoại, hoặc Cân bằng trần thuật.
5. **Từ vựng & Biện pháp tu từ (Rhetoric & Lexicon):**
   - Tần suất ví von/ẩn dụ (`như`, `tựa như`, `ngỡ như`).
   - Nhận diện từ láy biểu cảm tiếng Việt có chọn lọc.

---

## 🎭 CHỈ DẪN BIẾN THIÊN THEO LOẠI CẢNH (SCENE VARIANTS)

Hệ thống không áp đặt con số cứng nhắc cho mọi cảnh mà hướng dẫn biến thiên linh hoạt:
- **Cảnh hành động / xung đột:** Đẩy cao tỷ lệ câu ngắn (> 45%), rút ngắn thoại dưới 10 từ/lượt, nhịp dồn dập, động từ dứt khoát.
- **Cảnh tâm lý / lắng đọng:** Tăng tỷ lệ câu dài (> 30%), mở rộng khoảng lặng giữa các câu thoại, tập trung xúc giác và nhiệt độ không gian.
- **Cảnh đối thoại:** Thoại sắc bén kèm beat hành động nhỏ; tránh thoại trần trụi thiếu phản ứng cơ thể.

---

## 🗂️ QUẢN LÝ ĐA HỒ SƠ VĂN PHONG (MULTI-PROFILE)

| Lệnh CLI | Chức năng |
|---|---|
| `python manage_story.py style --list [--scope all\|story\|global]` | Liệt kê tất cả Style Profiles hiện có và đánh dấu profile đang active. |
| `python manage_story.py style --set <name> [--scope story\|global]` | Chuyển sang kích hoạt sử dụng profile `<name>`. |
| `python manage_story.py style --show [<name>]` | Xem toàn văn quy tắc sáng tác trong `STYLE_PROFILE.md`. |
| `python manage_story.py style --learn <path> --profile <name>` | Phân tích mẫu và xuất hồ sơ hoàn chỉnh. |

---

## ✅ TIÊU CHÍ NGHIỆM THU STYLE PROFILE
Một profile chuẩn xác khi:
- Tách bạch 2 file: `style_profile.json` (dữ liệu máy đọc) và `STYLE_PROFILE.md` (quy tắc người và AI đọc).
- Có đầy đủ số liệu 5 trục và ghi nhận rõ ràng mức độ tin cậy (`confidence_and_limitations`).
- Tự động hiển thị chỉ dẫn ngắn gọn mỗi khi chạy `python manage_story.py context`.
- Không sao chép nguyên văn đoạn trích có bản quyền vào văn bản truyện mới.
