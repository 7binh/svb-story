---
name: story-review
description: "Thẩm định phản biện đối kháng độc lập 4 cấp độ sau khi viết chương hoặc hoàn tất một Arc truyện. Soát lỗi logic bối cảnh, tính nhất quán (continuity), nhịp điệu (pacing) và tính cách nhân vật (OOC). Kích hoạt: /story-review, 'thẩm định', 'soát lỗi', 'review chương', 'đánh giá chương', 'kiểm tra logic'."
---

# /story-review: Thẩm Định Phản Biện Đối Kháng 4 Cấp Độ

Đóng vai trò là **Hội Đồng Độc Giả Khó Tính**, tiến hành rà soát đối kháng đa góc nhìn trên bản thảo để phát hiện các lỗ hổng logic, mâu thuẫn nhân quả, sự lệch nhịp kể hoặc nguy cơ biến dạng tính cách nhân vật (*Out Of Character - OOC*) trước khi hoàn thiện tác phẩm.

> **Nguyên tắc phân định ranh giới:**
> - Thẩm định là hoạt động đánh giá và lập báo cáo chẩn đoán; **tuyệt đối không tự ý sửa đổi văn bản gốc** khi chưa có sự đồng ý của tác giả.
> - Không bao giờ khẳng định bản thảo "hoàn toàn không có lỗi" chỉ vì không bắt được lỗi trong một lượt đọc; luôn nêu rõ phạm vi và giới hạn của lần rà soát.

---

## 🎭 3 VAI THẨM ĐỊNH ĐỐI KHÁNG ĐỘC LẬP

Khi nhận lệnh `/story-review`, Agent kích hoạt đồng thời 3 lăng kính chuyên môn kết hợp chạy lệnh kiểm định tự động:
```powershell
python manage_story.py memory --audit [--file path/to/chapter.md]
```

### 1. Vai 1: Chuyên Gia Logic, Canon & Continuity (Logic & Lore Reviewer)
- **Nhiệm vụ:** Đối chiếu trực tiếp với Story Canon, Causal Timeline (`events.json`), và trạng thái nhân vật (`characters_state.json`).
- **Câu hỏi kiểm tra:**
  * Có quy tắc thế giới, giới hạn cảnh giới hay luật lệ bối cảnh nào bị vi phạm không?
  * Dòng thời gian và quan hệ nhân quả có bị đảo ngược không?
  * Nhân vật có đang tự nhiên lành lặn vết thương cũ hoặc sử dụng vật phẩm đã mất không?
  * Có nhân vật nào hành động dựa trên bí mật mà họ chưa từng được chứng kiến hoặc nghe kể không?

### 2. Vai 2: Độc Giả Đại Chúng & Tiết Tấu (Pacing & Engagement Reviewer)
- **Nhiệm vụ:** Đánh giá nhịp độ câu chuyện, độ căng thẳng và sức hút giữ chân độc giả.
- **Câu hỏi kiểm tra:**
  * Chương này có bị lê thê giải thích bối cảnh quá nhiều (Exposition Dump) hay chuyển biến quá vội vàng thiếu căn cứ?
  * Xung đột trọng tâm có đủ sức nặng và có nguyên nhân thuyết phục không?
  * Cuối chương có để lại điểm treo móc (Hook/Cliffhanger) kích thích sự tò mò không?

### 3. Vai 3: Nhà Phê Bình Nhân Vật & Cảm Xúc (Character Voice & Psychology Reviewer)
- **Nhiệm vụ:** Rà soát chiều sâu tâm lý, giọng điệu nhân vật và nguy cơ OOC.
- **Câu hỏi kiểm tra:**
  * Khẩu khí của từng nhân vật có nhất quán với địa vị, tuổi tác và tính cách của họ không?
  * Động cơ hành động có bén rễ từ tổn thương quá khứ hay bị biến thành "con rối của cốt truyện" (Plot Puppet)?
  * Niềm tin của nhân vật (dù đúng hay sai) có được thể hiện chân thực qua hành vi không?

---

## 📋 HỆ THỐNG PHÂN LOẠI 4 CẤP ĐỘ PHÁT HIỆN (4-TIER AUDIT RUBRIC)

Mọi phát hiện trong quá trình thẩm định bắt buộc phải được phân loại theo đúng 4 cấp độ:

### 1. 🔴 Lỗi Nghiêm Trọng (Critical Invariant)
- **Định nghĩa:** Vi phạm các bất biến logic cốt tử: phá vỡ Canon thế giới, đảo lộn nhân quả, rò rỉ bí mật sai đối tượng, trạng thái chấn thương thể xác bị lãng quên, vật phẩm tự dịch chuyển.
- **Yêu cầu xử lý:** Bắt buộc chỉ ra bằng chứng cụ thể (trích dẫn dòng văn bản) và **phải khắc phục** trước khi lưu chương.

### 2. 🟡 Lệch Đáng Kể (Significant Flaw)
- **Định nghĩa:** Suy giảm chất lượng trần thuật: động cơ nhân vật bị khiên cưỡng, nhịp điệu chuyển cảnh quá gắt gao, giải thích cảm xúc trừu tượng (Tell thay vì Show), thiếu tương tác giác quan.
- **Yêu cầu xử lý:** Khuyến nghị chỉnh sửa cụ thể kèm phương án viết lại.

### 3. 🟢 Lệch Mềm (Soft Variance)
- **Định nghĩa:** Các biến thiên nhỏ về hình thức: độ dài câu trung bình hơi lệch so với Style Profile mẫu, tỷ lệ đối thoại/trần thuật dao động nhưng vẫn trong phạm vi chấp nhận được của phân cảnh.
- **Yêu cầu xử lý:** Tùy chọn cân nhắc, tác giả tự quyết định.

### 4. 🎨 Lựa Chọn Nghệ Thuật Hợp Lệ (Artistic Choice)
- **Định nghĩa:** Các hiện tượng đặc thù được tác giả chủ ý sử dụng vì mục đích nghệ thuật: phép ẩn dụ độc đáo, độc thoại dòng ý thức, đảo trật tự kể chuyện (Flashback), hiểu lầm kịch tính (Dramatic Irony), hoặc ngôn ngữ địa phương của nhân vật.
- **Yêu cầu xử lý:** **Bảo toàn nguyên vẹn**, nghiêm cấm việc chỉnh sửa máy móc làm phẳng văn phong.

---

## 📝 MẪU BÁO CÁO THẨM ĐỊNH CHUẨN (AUDIT REPORT TEMPLATE)

```markdown
# BÁO CÁO THẨM ĐỊNH CHƯƠNG: [Tên Chương / Phân Cảnh]
*Thời gian thực hiện: YYYY-MM-DD | Đối tượng: chapters/chapter_XXXX.md*

### 🌟 1. Điểm Sáng Đáng Ghi Nhận
- [Nhận xét 1: Chi tiết làm tốt về không khí, nhịp điệu hoặc khẩu khí đối thoại]
- [Nhận xét 2: Khắc họa tâm lý hoặc tương tác giác quan ấn tượng]

### 🔍 2. Bảng Phân Loại Phát Hiện
| Cấp độ | Vị trí (Đoạn/Dòng) | Hiện tượng & Trích dẫn bằng chứng | Lý do vi phạm | Đề xuất giải pháp |
|---|---|---|---|---|
| 🔴 Critical | Đoạn 4 | "Lâm Phong dùng tay phải vung kiếm..." | Chương 2 ghi nhận gãy tay phải, chưa được chữa trị | Chuyển sang tay trái hoặc miêu tả cơn đau dữ dội |
| 🟡 Significant | Đoạn 12 | "Nàng cảm thấy vô cùng đau đớn..." | Tell thay vì Show; lạm dụng dán nhãn cảm xúc | Hữu hình hóa qua nhịp thở đứt quãng và giọt mồ hôi |
| 🟢 Soft | Toàn chương | Tỷ lệ thoại 52% (hơi cao so với profile 40%) | Cảnh đàm phán nên thoại nhiều hơn bình thường | Có thể giữ nguyên nếu hợp không khí |
| 🎨 Artistic | Đoạn 8 | Dòng ý thức dài 4 câu liên tiếp không ngắt | Khắc họa sự hoảng loạn tột độ của nhân vật | Bảo toàn nguyên vẹn |

### ⚖️ 3. Kết Luận & Hướng Dẫn Kế Tiếp
- **Đánh giá trạng thái:** [SẴN SÀNG LƯU / CẦN KHẮC PHỤC LỖI CRITICAL]
- **Hành động đề xuất cho tác giả:** [Nêu 1-2 bước cụ thể để hoàn thiện bản thảo]
```
