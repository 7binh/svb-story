---
name: story-deslop
description: "Biên tập và khử văn mẫu AI (Anti-Slop), trau chuốt câu từ theo nguyên tắc Show, Don't Tell, chuẩn hóa dấu câu an toàn và hỗ trợ .deslop-whitelist. Hỗ trợ tách biệt chế độ phát hiện (Scan) và chế độ sửa chữa (Fix). Kích hoạt: /story-deslop, 'khử văn mẫu', 'khử AI', 'tút lại văn', 'chỉnh văn phong', 'soát từ sáo rỗng'."
---

# /story-deslop: Biên Tập Ngữ Cảnh & Khử Văn Mẫu AI (Anti-Slop)

Chuyên trách việc loại bỏ cảm giác máy móc, văn dịch thô và các khuôn mẫu sáo rỗng thường gặp trong văn xuôi do AI tạo ra; trả lại nhịp thở tự nhiên, sinh động và chiều sâu cảm xúc cho tiếng Việt văn học.

---

## 🛡️ NGUYÊN TẮC BẢO TOÀN NGHỆ THUẬT (GUARDRAILS)

Quá trình khử slop **tuyệt đối không** biến thành việc kiểm duyệt máy móc hoặc thay thế từ ngữ thô bạo:
1. **Bảo toàn cốt truyện & Nhân quả:** Không làm thay đổi bất kỳ sự kiện, hành động, kết quả hay quy tắc thế giới nào trong Story Canon.
2. **Bảo toàn giọng điệu nhân vật (Voice):** Nhân vật cộc cằn, học giả uyên bác, hay kẻ gian xảo phải giữ nguyên khẩu khí và từ ngữ đặc trưng của họ.
3. **Tôn trọng lựa chọn nghệ thuật (Artistic Intent):** Các phép lặp có chủ đích nhằm nhấn mạnh tâm trạng, dòng ý thức, hoặc tiếng lóng địa phương phải được bảo toàn nguyên vẹn.
4. **Hỗ trợ Whitelist cục bộ (`.deslop-whitelist`):** Nếu một từ/cụm từ nằm trong file `.deslop-whitelist` của bộ truyện, hệ thống xem đó là lựa chọn nghệ thuật hợp lệ và bỏ qua cảnh báo.

---

## 🔍 HAI CHẾ ĐỘ TÁC NGHIỆP: SCAN VS FIX

Hệ thống tách bạch rõ ràng giữa phân tích và chỉnh sửa:

### 1. Chế độ Phát hiện Vấn đề (Detection / Scan Mode)
Chỉ quét và lập báo cáo chẩn đoán, **không tự ý thay đổi bản thảo**:
- **Chạy công cụ cơ học:**
  ```powershell
  python manage_story.py check [--file path/to/chapter.md]
  ```
- **Chẩn đoán ngữ cảnh (AI Agent Diagnostic):**
  - Chỉ ra vị trí cụ thể (đoạn, câu).
  - Phân tích vì sao cách diễn đạt đó bị sáo rỗng hoặc mang tính dịch thô.
  - Đề xuất 2-3 phương án viết lại tự nhiên để tác giả lựa chọn.

### 2. Chế độ Sửa chữa Trực tiếp (Fix / Rewrite Mode)
Trực tiếp trau chuốt văn bản theo phương án đã được duyệt:
- Tinh chỉnh câu chữ trực tiếp trong file chương `chapters/chapter_XXXX.md` hoặc `draft.md`.
- Chạy lại lệnh `check` để xác nhận không còn lỗi kỹ thuật.

---

## 🧹 QUY TRÌNH BIÊN TẬP 3 TẦNG CHUYÊN SÂU

### Tầng 1: Quét Kỹ Thuật Cơ Học & Chuẩn Hóa Dấu Câu
Chạy công cụ Native Python:
```powershell
python manage_story.py check
```
- Module `scripts/vn_checker.py` tự động phát hiện:
  * Khoảng trắng thừa trước dấu câu (` ,`, ` .`, ` ?`).
  * Thiếu khoảng trắng sau dấu câu khi nối từ.
  * Dấu ngoặc kép thoại chưa đóng hoặc chuỗi chấm bất thường (`..`, `....`).
  * Các cụm từ thuộc danh mục blacklist tiếng Việt nghiêm trọng.
- Khi cần chuẩn hóa nhanh dấu câu mà không đổi từ ngữ:
  ```powershell
  python scripts/vn_checker.py path/to/chapter.md --normalize
  ```

---

### Tầng 2: Thanh Lọc Danh Sách Đen Cụm Từ Sáo Rỗng (Anti-Slop Blacklist)
Đối chiếu trực tiếp với tài liệu [../../references/anti-slop.md](../../references/anti-slop.md):

| Cụm từ văn mẫu AI (Slop) | Nhược điểm ngữ nghĩa | Cách viết lại tự nhiên |
|---|---|---|
| *"Không thể không thừa nhận rằng..."* | Thừa thãi, dịch thô từ tiếng Trung/Anh | Bỏ hẳn cụm từ này, đi thẳng vào suy nghĩ hoặc hành động. |
| *"Không thể phủ nhận rằng..."* | Giọng thuyết minh triết lý gượng gạo | Chuyển thành độc thoại nội tâm hoặc hành vi cụ thể. |
| *"Bầu không khí bỗng ngưng đọng lại..."* | Sáo rỗng, lặp đi lặp lại | Tả âm thanh thực tế: tiếng nuốt nước bọt, tiếng tàn thuốc rơi, tiếng gió đập vào cửa. |
| *"Trong mắt lóe lên một tia phức tạp..."* | Lười biếng, mơ hồ | Tả phản ứng sinh lý: đồng tử co rút, hàng mày nhíu chặt, cái liếc mắt nhanh. |
| *"Con đường phía trước còn rất dài..."* | Đúc kết sến sẩm ở cuối chương | Kết thúc bằng câu hỏi mở, tiếng bước chân trong đêm hoặc một hành động dứt khoát. |
| *"Như thể thời gian đã ngừng trôi..."* | Cliche thiếu sức nặng | Tả chi tiết giác quan chậm lại: tiếng giọt máu rơi xuống sàn đá, tiếng kim đồng hồ điểm tích tắc. |
| *"Trong lòng không khỏi dâng lên..."* | Dán nhãn cảm xúc gián tiếp | Tả phản ứng cơ thể: lồng ngực đập thình thịch, cổ họng nghẹn cứng. |

- **Quy tắc Cắt gọt 20%:** Nếu một đoạn văn có 3 câu giải thích cảm xúc trừu tượng liên tiếp, xóa bỏ 2 câu giải thích và giữ lại 1 câu hành động vật lý rõ nét nhất.

---

### Tầng 3: Nâng Cấp Theo Kỹ Thuật Show, Don't Tell & Chiều Sâu Giác Quan
Đối chiếu tài liệu [../../references/show-dont-tell.md](../../references/show-dont-tell.md):
1. **Hữu hình hóa cảm xúc qua phản ứng cơ thể:** Thay vì viết "hắn cảm thấy sợ hãi", hãy miêu tả: da gà nổi cộm, khớp ngón tay siết chặt đến trắng bệch, hơi thở gấp gáp phả ra từng luồng khí trắng.
2. **Kích hoạt ít nhất 3/5 giác quan trong mỗi phân cảnh:**
   - Thị giác (Visual): Ánh sáng le lói, bóng đổ vắt ngang sàn đá.
   - Thính giác (Auditory): Tiếng cọt kẹt của bản lề cửa mục, tiếng nước nhỏ giọt đều đặn.
   - Khứu giác (Olfactory): Mùi ẩm mốc của rêu phong, mùi khét nồng của dầu đèn.
   - Xúc giác (Tactile): Cơn gió buốt thấu xương lùa qua kẽ áo, sự nham nhở của chuôi kiếm sứt mẻ.
   - Vị giác (Gustatory): Vị tanh mặn nơi đầu lưỡi.
3. **Đối thoại đa tầng có Subtext & Beat:**
   - Xen kẽ hành động thể chất nhỏ (nhấp ngụm trà, gõ nhẹ ngón tay lên bàn) giữa các câu thoại.
   - Thể hiện sự đấu trí: Lời nói bề ngoài điềm đạm nhưng ngầm thăm dò đối phương.
