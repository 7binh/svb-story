# BỘ TIÊU CHÍ ĐÁNH GIÁ VĂN HỌC ĐỊNH TÍNH (LITERARY EVALUATION RUBRIC)
## DÀNH CHO TIỂU THUYẾT DÀI TẬP — SVB-STORY (PHASE 2)

> **Nguyên tắc phân định ranh giới:**  
> Các bài kiểm thử kỹ thuật (Unit Tests, Regression Fixtures, Regular Expressions, Heuristics) chỉ có thể xác minh **tính bất biến logic** (Invariants: nhân vật bị thương không vung tay, vật phẩm không tự dịch chuyển, bí mật không bị lộ sai đối tượng, cú pháp hợp lệ).  
> **Không có bất kỳ thuật toán code hay điểm số metric nào có thể tự động chứng minh một tác phẩm văn chương là "hay".**  
> Tài liệu này thiết lập khung đánh giá định tính (Qualitative Rubric) giúp AI Reviewer (`/story-review`) và Tác giả thẩm định chiều sâu nghệ thuật của tác phẩm.

---

## 1. 8 Trục Đánh Giá Văn Học Định Tính

### 1. Trục 1: Chiều Sâu Tâm Lý & Xung Đột Nội Tâm (Psychological Depth)
- **Thang đo:**
  - *Mức 1 (Nông cạn):* Nhân vật phản ứng phẳng, một chiều (chỉ có vui mừng hoặc tức giận), không có sự giằng xé hay hoài nghi bản thân.
  - *Mức 2 (Trung bình):* Có biểu hiện suy nghĩ nội tâm nhưng còn thuyết minh trực diện (Tell thay vì Show), cảm xúc chuyển đột ngột.
  - *Mức 3 (Sâu sắc):* Nhân vật có "vùng tối" và mâu thuẫn nội tâm (vừa muốn báo thù vừa trắc ẩn; vừa muốn che giấu bí mật vừa khao khát được thấu hiểu). Cảm xúc phản chiếu qua phản ứng sinh lý và hành vi vô thức.

### 2. Trục 2: Tính Thuyết Phục Của Động Cơ (Motivational Credibility)
- **Thang đo:**
  - *Mức 1:* Hành động vì tác giả muốn plot tiến triển (Plot Puppet), phi logic so với hoàn cảnh và quá khứ.
  - *Mức 2:* Có lý do bề mặt (cần tiền, trả thù) nhưng thiếu tính cấp thiết sống còn.
  - *Mức 3:* Động cơ bén rễ sâu xa từ vết thương tâm lý quá khứ (Ghost/Wound). Mọi lựa chọn khó khăn đều phải trả giá, cái giá phải trả thể hiện rõ nhân sinh quan của nhân vật.

### 3. Trục 3: Nhịp Kể & Biến Thiên Tiết Tấu (Narrative Pacing & Rhythm)
- **Thang đo:**
  - *Mức 1:* Nhịp đều đều gây buồn ngủ hoặc dồn dập từ đầu đến cuối khiến độc giả mệt mỏi; độ dài câu và đoạn văn bằng phẳng.
  - *Mức 2:* Có phân biệt giữa cảnh hành động và cảnh tĩnh nhưng chuyển đoạn còn đột ngột, thiếu nhịp chuyển (transitions).
  - *Mức 3:* Nhịp văn co giãn uyển chuyển: dồn dập, gãy gọn bằng câu ngắn trong giao tranh; giãn dài, đa tầng nhạc tính trong hoài niệm và đối thoại ngầm.

### 4. Trục 4: Khẩu Khí & Giọng Điệu Nhân Vật (Character Voice & Distinctiveness)
- **Thang đo:**
  - *Mức 1 (Giọng tác giả):* Mọi nhân vật đều nói năng giống hệt nhau, từ lão già, thiếu nữ đến kẻ sát nhân.
  - *Mức 2:* Có gán ghép khẩu ngữ bề ngoài (xưng hô, vài từ đệm) nhưng bản chất tư duy thoại vẫn giống nhau.
  - *Mức 3:* Mỗi nhân vật sở hữu một trường từ vựng, nhịp ngắt câu, vị thế quyền lực và thói quen ẩn dụ riêng biệt. Độc giả không cần nhìn tên người nói vẫn nhận ra ai đang cất lời.

### 5. Trục 5: Chất Lượng Đối Thoại Đa Tầng (Subtextual Dialogue)
- **Thang đo:**
  - *Mức 1 (Bộc bạch trực diện):* Nhân vật nghĩ gì nói nấy, đối thoại chỉ để giải thích thông tin bối cảnh cho độc giả (Exposition Dump).
  - *Mức 2:* Đối thoại tự nhiên hơn nhưng thiếu lớp nghĩa ngầm (Subtext), thiếu động thái thăm dò.
  - *Mức 3:* "Lời ít ý nhiều" — những điều không nói ra mới là trọng tâm. Đối thoại là một trận đấu trí vi mô: che giấu động cơ, tung hỏa mù, mượn chuyện phong cảnh để nói chuyện quyền lực.

### 6. Trục 6: Sự Tự Nhiên & Biểu Cảm Của Văn Xuôi (Prose Fluency & Sensorial Texture)
- **Thang đo:**
  - *Mức 1 (AI-Slop):* Lạm dụng các công thức sáo rỗng (*"không thể phủ nhận", "dường như có một tia phức tạp", "bầu không khí ngưng trệ"*).
  - *Mức 2:* Văn phong trôi chảy, đúng ngữ pháp nhưng còn khô khan, thiếu hình ảnh cảm giác.
  - *Mức 3 (Chất văn sống động):* Kích hoạt ít nhất 3 giác quan (âm thanh, mùi vị, nhiệt độ); động từ mạnh, tính từ giàu liên tưởng văn hóa; không lạm dụng từ chỉ cảm xúc trừu tượng.

### 7. Trục 7: Khả Năng Gieo Phục Bút & Trả Nợ Tình Tiết (Plant & Payoff Arc)
- **Thang đo:**
  - *Mức 1:* Giải quyết nút thắt bằng "Deus Ex Machina" (yếu tố bất ngờ trên trời rơi xuống cứu nguy không có cơ sở tiền đề).
  - *Mức 2:* Có cài cắm chi tiết nhưng quá lộ liễu, hoặc gieo mà quên gặt sau hàng chục chương.
  - *Mức 3:* Phục bút được gài ngầm tự nhiên dưới dạng chi tiết đời thường hoặc đồ vật tưởng chừng vô hại; khi payoff được kích hoạt, độc giả cảm thấy "bất ngờ nhưng hoàn toàn tất yếu".

### 8. Trục 8: Tính Nhất Quán Xuyên Suốt & Tiến Trình Trưởng Thành (Continuity & Arc Progression)
- **Thang đo:**
  - *Mức 1:* Nhân vật bị reset tính cách sau mỗi Arc, quên đi bài học cũ, lặp lại sai lầm ngớ ngẩn.
  - *Mức 2:* Nhân vật mạnh lên về chỉ số năng lực/võ công nhưng thế giới quan và tâm lý không tiến hóa.
  - *Mức 3:* Trưởng thành đi kèm mất mát: nhân vật thay đổi quan điểm sau từng biến cố bước ngoặt (Catalyst Event). Thế giới xung quanh phản ứng chân thực với những hành động của nhân vật.

---

## 2. Bảng Phân Định Giữa Lỗi Kỹ Thuật và Lựa Chọn Sáng Tạo

| Hiện Tượng Trong Bản Thảo | Phân Loại | Cách Xử Lý Đúng Đắn |
|---|---|---|
| Nhân vật bị gãy tay phải vung kiếm tay phải | **🔴 Lỗi kỹ thuật (Critical Invariant)** | Bắt buộc sửa: đổi tay hoặc thêm tình tiết đau đớn/trợ giúp |
| Nhân vật A nói lộ bí mật mà chỉ B và C biết | **🔴 Lỗi kỹ thuật (Secret Leakage)** | Bắt buộc sửa: cắt câu thoại hoặc bổ sung tình tiết biết trước |
| Đảo trật tự thời gian kể chuyện (Flashback) | **🎨 Lựa chọn nghệ thuật (Artistic Choice)** | **Bảo toàn:** Kiểm tra tính nhân quả không bị đảo lộn |
| Câu văn rất dài chứa nhiều hình ảnh ẩn dụ | **🎨 Lựa chọn nghệ thuật (Artistic Choice)** | **Bảo toàn:** Không được dùng máy móc cắt vụn câu văn |
| Nhân vật tin sai một sự thật thế giới (Hiểu lầm) | **🎨 Chủ ý cốt truyện (Dramatic Irony)** | **Bảo toàn:** Đánh dấu `character_belief` với `accuracy=False` |
| Đối thoại chứa tiếng lóng hoặc khẩu ngữ địa phương | **🎨 Sắc thái nhân vật (Character Flavor)** | **Bảo toàn:** Kiểm tra sự nhất quán trong khẩu khí |
