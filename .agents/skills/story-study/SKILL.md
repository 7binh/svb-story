---
name: story-study
description: "Học và giải mã văn phong từ truyện mẫu (thư mục, file hoặc dán nháp trực tiếp). Bóc tách 5 trục, tạo Style Profile độc lập (story hoặc global), thiết lập Style Enforcement Pipeline bắt buộc khi viết chương mới. Kích hoạt: /story-study, 'học văn phong', 'nghiên cứu văn phong', 'học truyện mẫu'."
---

# /story-study: Giải Mã Văn Phong Truyện Mẫu (Style Engine 2.0)

Trợ lý chuyên trách việc **nghiên cứu, bóc tách và chuyển hóa văn phong** từ các tác phẩm mẫu thành bộ quy tắc sáng tác có thể thực thi và kiểm chứng lâu dài.

---

## 🎯 NGUYÊN TẮC CỐT LÕI (Leading Words)

1. **Benchmark Ingestion (Nạp Mẫu Đa Dạng)**: Tiếp nhận văn bản mẫu qua 3 hình thức (thư mục, file đơn, dán nháp). Chỉ trích xuất kỹ thuật kể chuyện và quy luật cú pháp, tuyệt đối không sao chép nguyên văn tình tiết.
2. **5-Axis Decomposition (Bóc Tách 5 Trục)**: Phân tích định lượng (âm tiết, mật độ giác quan, tỷ lệ thoại) và định tính rõ ràng giữa số liệu đo được vs nhận định ước lượng (estimated).
3. **Style Fingerprint & Style Rules**: Sinh ra hai thành phần độc lập: *Vân tay đặc trưng* (máy đọc JSON) và *Quy tắc sáng tác* (người & AI đọc Markdown).
4. **Data Safety**: Không bao giờ làm mất đoạn văn mẫu của tác giả; tự động lưu bản sao nguồn mẫu vào profile.
5. **Two-Tier Storage (Story & Global)**: Hỗ trợ lưu trữ profile cấp tác phẩm (`story`) hoặc thư viện cấp hệ thống (`global`) để tái sử dụng cho nhiều bộ truyện.

---

## 📥 3 HÌNH THỨC CUNG CẤP TRUYỆN MẪU

### Hình thức 1: Thư mục chứa nhiều truyện mẫu
Áp dụng khi bạn có một kho tài liệu mẫu gồm nhiều file `.txt` hoặc `.md`:
```powershell
python manage_story.py style --learn ./samples/my-stories/ --profile my-style --scope story
```
*(Nếu muốn lưu vào thư viện dùng chung toàn cục, thêm cờ `--scope global`)*.
- Hệ thống quét đệ quy các file hợp lệ, bỏ qua cache và thư mục profile.
- Báo cáo rõ tổng số file đã đọc, số file rỗng hoặc lỗi.

### Hình thức 2: File truyện mẫu có sẵn
Áp dụng khi bạn muốn học trực tiếp từ 1 chương hoặc 1 cuốn sách cụ thể:
```powershell
python manage_story.py style --learn ./samples/chapter-01.txt --profile kim-dung --scope global
```

### Hình thức 3: Dán đoạn trích trực tiếp vào nháp (draft.md)
Áp dụng khi bạn muốn test nhanh một cảnh tâm đắc (1.000 – 3.000 chữ) mà không cần chuẩn bị file:
1. Mở `stories/<active_story_id>/chapters/draft.md`.
2. Dòng 1: `/story-study --profile <tên_profile> [--scope story|global]` (nếu không ghi tên, mặc định lưu vào `default`).
3. Dòng 2 trở đi: Dán đoạn văn mẫu cần học.
4. Chạy lệnh:
   ```powershell
   python manage_story.py save
   ```
- *Bảo vệ dữ liệu:* Văn bản mẫu trong `draft.md` được giữ nguyên trạng kèm thông báo xác nhận và bản sao được lưu an toàn tại thư mục profile.

---

## 🔬 5 TRỤC BÓC TÁCH VĂN PHONG (STYLE DECOMPOSITION)

Hệ thống bóc tách thành **Style Fingerprint (Schema 2.0.0)**:

1. **Cấu trúc & Nhịp câu (Syntax & Rhythm)**:
   - Đo lường theo đơn vị âm tiết (syllable units): câu ngắn (< 10 âm tiết), câu vừa (10–22 âm tiết), câu dài (> 22 âm tiết).
   - Tần suất dấu câu tạo nhịp thở: chấm lửng (`...`), gạch ngang (`—`), cảm thán (`!`), hỏi (`?`).
2. **Mật độ Giác quan & Tả cảnh (Sensory Immersion)**:
   - Đo lường mật độ Thị giác, Thính giác, Xúc giác/Cơ thể, Khứu/Vị giác trên 1.000 âm tiết.
   - Xác định giác quan chủ đạo và chức năng miêu tả (Show, Don't Tell).
3. **Tỷ lệ Phân bổ Nội dung (Content Ratios)**:
   - Hỗ trợ thoại nhiều dòng và nhiều loại dấu thoại (`""`, `“”`, `「」`, `『』`, `—`).
   - Định lượng % Hội thoại vs Tự sự/Hành động vs Độc thoại nội tâm.
4. **Khẩu khí & Tông giọng (Tone & Voice - Estimated)**:
   - Gắn nhãn ước lượng heuristic: Dồn dập căng thẳng, Trầm tĩnh chậm rãi, Kịch tính đối thoại, hoặc Cân bằng trần thuật.
5. **Từ vựng & Biện pháp tu từ (Rhetoric & Lexicon)**:
   - Tần suất ví von/ẩn dụ (như, tựa như...).
   - Nhận diện từ láy biểu cảm tiếng Việt có chọn lọc.

---

## 🎭 ĐẶC ĐIỂM LINH HOẠT THEO TỪNG LOẠI CẢNH (SCENE VARIANTS)
Hệ thống không áp đặt tỷ lệ cứng nhắc cho toàn bộ truyện, mà cung cấp chỉ dẫn biến thiên:
- **Cảnh hành động / xung đột:** Đẩy cao tỷ lệ câu ngắn (> 45%), rút ngắn thoại dưới 10 từ/lượt, nhịp dồn dập.
- **Cảnh tâm lý / lắng đọng:** Tăng tỷ lệ câu dài (> 30%), mở rộng khoảng lặng giữa các câu thoại.
- **Cảnh đối thoại:** Thoại sắc bén kèm beat hành động nhỏ; tránh thoại trơ trọi không phản ứng cơ thể.

---

## 🗂️ QUẢN LÝ ĐA HỒ SƠ VĂN PHONG (MULTI-PROFILE)

| Lệnh CLI | Chức năng |
|---|---|
| `python manage_story.py style --list [--scope all\|story\|global]` | Liệt kê tất cả Style Profiles hiện có và đánh dấu profile đang active. |
| `python manage_story.py style --set <name> [--scope story\|global]` | Chuyển sang sử dụng profile `<name>`. |
| `python manage_story.py style --show [<name>]` | Xem toàn văn hồ sơ `STYLE_PROFILE.md` và các quy tắc sáng tác chi tiết. |
| `python manage_story.py style --learn <path> --profile <name> [--scope story\|global]` | Học từ file/thư mục và lưu vào profile chỉ định (không ghi đè profile khác). |

---

## ✅ TIÊU CHÍ NGHIỆM THU (ACCEPTANCE CRITERIA)
Một profile chỉ được xem là hoàn chỉnh khi:
- Đủ 5 trục phân tích với số liệu âm tiết và tỷ lệ phân bổ rõ ràng.
- Tách rời file dữ liệu `style_profile.json` và file quy tắc `STYLE_PROFILE.md`.
- Ghi rõ mức độ tin cậy và giới hạn phân tích (confidence & limitations).
- Tự động hiển thị 3 dòng chỉ dẫn ngắn gọn và đường dẫn quy tắc mỗi khi chạy `context`.
- Không sao chép nguyên văn đoạn trích bản quyền mà khái quát thành kỹ thuật kể chuyện.
