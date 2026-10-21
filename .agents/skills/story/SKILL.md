---
name: story
description: "Trạm điều phối trung tâm (Central Router) cho hệ sinh thái sáng tác StoryFlow. Tự động nhận diện ý định tự nhiên của tác giả, kiểm tra trạng thái truyện và định tuyến vào workflow chuẩn xác (viết tiếp, viết mới, viết dài, lập đề cương, phân tích văn phong, khử văn mẫu, thẩm định, tạo bìa, nhập truyện). Kích hoạt: /story, $story, /truyện, 'viết truyện', 'quản lý truyện'."
---

# /story: Trạm Điều Phối Sáng Tác & Quản Trị Ngữ Cảnh Trung Tâm

Chào mừng bạn đến với **StoryFlow Router**. Đây là điểm tiếp nhận duy nhất cho mọi nhu cầu sáng tác và quản lý tiểu thuyết. Bạn chỉ cần mô tả mong muốn bằng ngôn ngữ tự nhiên, hệ thống sẽ tự động phân tích ngữ cảnh, kiểm tra tác phẩm hiện hành và chọn đúng workflow tối ưu nhất mà không cần bạn phải nhớ tên các công cụ con.

---

## 🧠 MA TRẬN NHẬN DIỆN Ý ĐỊNH & ĐỊNH TUYẾN TỰ ĐỘNG

Khi nhận lệnh `/story` kèm yêu cầu tự nhiên, Router thực hiện quy trình 3 bước:
1. **Kiểm tra trạng thái dự án:** Chạy kiểm tra tác phẩm đang được chọn:
   ```powershell
   python manage_story.py status
   ```
2. **Phân loại ý định của người dùng:**
   - *Viết tiếp / Viết chương mới:* Người dùng nói "viết tiếp", "viết chương tiếp theo", "chương 5", "triển khai cảnh này".
   - *Viết dài tự hành:* Người dùng muốn viết hàng loạt chương tự động, "viết từ chương 3 đến 5", "chạy tự động cho xong Arc 1".
   - *Sáng tác tác phẩm mới:* Người dùng nói "mở truyện mới", "ý tưởng mới", "tạo bộ truyện tiên hiệp mới".
   - *Lập đề cương / Phát triển plot:* Người dùng nói "lên dàn ý", "bí ý tưởng", "cho 3 hướng rẽ", "theo dõi phục bút".
   - *Học & Áp dụng văn phong:* Người dùng nói "học văn phong file này", "phân tích cách viết Kim Dung", "tạo style profile".
   - *Khử văn mẫu AI / Trau chuốt câu từ:* Người dùng nói "khử AI", "tút lại đoạn này", "văn bị máy móc", "bỏ từ sáo rỗng".
   - *Thẩm định đối kháng:* Người dùng nói "review chương này", "soát lỗi logic", "kiểm tra OOC", "đánh giá chất lượng".
   - *Nhập bản thảo cũ:* Người dùng nói "import truyện cũ", "tách file 50 chương", "nạp bản thảo có sẵn".
   - *Tạo prompt ảnh bìa:* Người dùng nói "làm ảnh bìa", "prompt vẽ bìa", "thiết kế bìa sách".
3. **Định tuyến vào Workflow tương ứng:**

| Mục tiêu của bạn | Router tự động chuyển giao | Hành động của Router & Agent |
|---|---|---|
| **Viết từng chương tương tác** | `skills/story-write/SKILL.md` | Đọc `outline.md` và `summaries/`, nạp 5 lớp ngữ cảnh, cùng tác giả soạn và duyệt từng cảnh/chương. |
| **Viết dài tự hành (End-to-End)** | `skills/story-flow/SKILL.md` | Chu trình tự hành: Context → Soạn nháp → Audit kép → Sửa lỗi → Cập nhật Memory → Lưu chương liên hoàn. |
| **Bí ý tưởng / Đề cương / Phục bút** | `skills/story-outline/SKILL.md` | Đề xuất 3 nhánh rẽ (Action / Emotion / Twist), quản lý đề cương Arc, theo dõi sổ tay phục bút `foreshadow.json`. |
| **Học văn phong truyện mẫu** | `skills/story-study/SKILL.md` | Phân tích 5 trục (nhịp câu, giác quan, tỷ lệ thoại, khẩu khí, tu từ), xuất Style Profile Schema 2.0.0. |
| **Khử văn mẫu AI / Tút văn** | `skills/story-deslop/SKILL.md` | Áp dụng Show-Don't-Tell, lọc blacklist sáo rỗng, chuẩn hóa dấu câu an toàn, tôn trọng `.deslop-whitelist`. |
| **Thẩm định phản biện 4 cấp** | `skills/story-review/SKILL.md` | Đóng 3 vai (Logic/Canon, Tiết tấu/Pacing, Chiều sâu tâm lý/Voice), phân loại lỗi theo 4 cấp độ chuẩn xác. |
| **Thiết kế prompt ảnh bìa** | `skills/story-cover/SKILL.md` | Đọc metadata và không khí truyện, sinh prompt Midjourney/SDXL/DALL-E chuẩn tỷ lệ tiểu thuyết `--ar 2:3`. |
| **Nhập bản thảo có sẵn** | `skills/story-import/SKILL.md` | Phân rã file raw nhiều chương, lập chỉ mục chương, tái dựng Canon/Timeline mà không sửa đổi bản gốc. |
| **Cài đặt / Đồng bộ môi trường** | `skills/story-setup/SKILL.md` | Kiểm tra tính toàn vẹn của runtime và workspace, đồng bộ công cụ thực thi nếu cần. |

---

## ⚡ NGUYÊN TẮC ĐỊNH TUYẾN AGENT-NATIVE (ROUTER RULES)

1. **Không hỏi thừa (Zero Needless Interruption):**
   - Nếu người dùng đã nói "viết tiếp chương 3 cho truyện Dạ Ma", Router kiểm tra `status`. Nếu truyện đang chọn là `da-ma` hoặc tồn tại trong danh sách, tự động chọn và nạp ngữ cảnh viết, **tuyệt đối không hỏi lại** "Bạn có muốn viết tiếp không?".
   - Chỉ hỏi khi thiếu thông tin cốt tử (ví dụ: người dùng nói "viết tiếp đi" nhưng workspace chưa từng có truyện nào được tạo hoặc có 2 truyện cùng tên).
2. **Không vô tình ghi đè / tạo mới truyện (No Accidental Story Reset):**
   - Khi người dùng muốn viết tiếp, Router luôn ưu tiên truyện đang hoạt động (`active_story`). Không bao giờ chạy `python manage_story.py init` đè lên truyện cũ trừ khi người dùng nói rõ "tạo truyện mới hoàn toàn".
3. **Phân biệt phạm vi cảnh đơn lẻ vs Viết tiểu thuyết dài:**
   - Yêu cầu viết một đoạn ngắn/phân cảnh đơn giản: Sử dụng ngay kỹ thuật chấp bút tương tác trong `story-write`, không bắt buộc nạp toàn bộ pipeline dài tập.
   - Yêu cầu viết trường thiên nhiều chương: Hướng dẫn kích hoạt `story-flow` (chế độ Autonomous hoặc Interactive).
4. **Cơ chế Fallback (Nền tảng không hỗ trợ gọi chéo sub-skill):**
   - Nếu môi trường agent không cho phép một Skill trực tiếp kích hoạt Skill khác qua lệnh gọi hệ thống, Agent chủ động đọc nội dung file `skills/<target-skill>/SKILL.md` và thực thi tuần tự các bước hướng dẫn trong file đó. Agent không được báo lỗi hay dừng lại chỉ vì thiếu lệnh gọi tool tự động.

---

## 🛠️ THAO TÁC NHANH VỚI TÁC PHẨM (CLI QUICK ACTIONS)

Khi cần tra cứu trạng thái hoặc can thiệp trực tiếp vào dữ liệu hệ thống:
```powershell
# Xem danh sách và chọn truyện làm việc
python manage_story.py stories
python manage_story.py select --id <slug_truyen>

# Khởi tạo truyện mới nếu chưa có
python manage_story.py init --title "Tên Truyện" --author "Bút Danh" --genre "Thể Loại"

# Kiểm tra tình trạng tác phẩm hiện hành
python manage_story.py status

# Nạp 5 lớp ngữ cảnh tối ưu token cho chương tiếp theo
python manage_story.py context

# Quét lỗi văn phong & dấu câu bản nháp
python manage_story.py check

# Quản lý Narrative Memory & Timeline
python manage_story.py memory --timeline
python manage_story.py memory --audit

# Mở Web Dashboard giao diện trực quan
python manage_story.py dashboard
```
