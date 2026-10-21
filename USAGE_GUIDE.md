# HƯỚNG DẪN VẬN HÀNH TOÀN DIỆN STORYFLOW (USAGE GUIDE)

Tài liệu này cung cấp quy trình khép kín từ đầu đến cuối cho **14 tình huống sáng tác thực tế** trong hệ sinh thái StoryFlow. Mỗi tình huống bao gồm điểm bắt đầu, lệnh chính xác, prompt mẫu bằng ngôn ngữ tự nhiên, các bước thực thi chi tiết, cách tiếp tục và xử lý sự cố.

---

## MỤC LỤC 14 TÌNH HUỐNG

1. [Tình huống 1: Viết thông thường (Interactive Scene/Chapter Writing)](#tình-huống-1-viết-thông-thường-interactive-scenechapter-writing)
2. [Tình huống 2: Viết khám phá, chưa có đề cương (Pantser / Exploratory Writing)](#tình-huống-2-viết-khám-phá-chưa-có-đề-cương-pantser--exploratory-writing)
3. [Tình huống 3: Viết truyện dài nhiều chương (Long-form Novel Pipeline)](#tình-huống-3-viết-truyện-dài-nhiều-chương-long-form-novel-pipeline)
4. [Tình huống 4: Tự động viết nhiều chương trong phạm vi cho phép (Autonomous Mode)](#tình-huống-4-tự-động-viết-nhiều-chương-trong-phạm-vi-cho-phép-autonomous-mode)
5. [Tình huống 5: Sáng tác có mẫu văn phong (Writing with Style Profile)](#tình-huống-5-sáng-tác-có-mẫu-văn-phong-writing-with-style-profile)
6. [Tình huống 6: Sáng tác không có mẫu văn phong (Writing with Default Style)](#tình-huống-6-sáng-tác-không-có-mẫu-văn-phong-writing-with-default-style)
7. [Tình huống 7: Sáng tác khi đã có đề cương (Writing with Established Outline)](#tình-huống-7-sáng-tác-khi-đã-có-đề-cương-writing-with-established-outline)
8. [Tình huống 8: Sáng tác khi chưa có đề cương (Writing without Outline)](#tình-huống-8-sáng-tác-khi-chưa-có-đề-cương-writing-without-outline)
9. [Tình huống 9: Tiếp tục tác phẩm có sẵn (Resuming an Existing Project)](#tình-huống-9-tiếp-tục-tác-phẩm-có-sẵn-resuming-an-existing-project)
10. [Tình huống 10: Biên tập một đoạn hoặc phân cảnh (Local Editing & Scene Polishing)](#tình-huống-10-biên-tập-một-đoạn-hoặc-phân-cảnh-local-editing--scene-polishing)
11. [Tình huống 11: Thẩm định và kiểm tra lỗi (Review & Audit 4 Tiers)](#tình-huống-11-thẩm-định-và-kiểm-tra-lỗi-review--audit-4-tiers)
12. [Tình huống 12: Khử văn phong máy móc (Anti-Slop & Deslop Purification)](#tình-huống-12-khử-văn-phong-máy-móc-anti-slop--deslop-purification)
13. [Tình huống 13: Tạo prompt ảnh bìa tiểu thuyết AI (Novel Cover Art Generation)](#tình-huống-13-tạo-prompt-ảnh-bìa-tiểu-thuyết-ai-novel-cover-art-generation)
14. [Tình huống 14: Kết hợp nhiều nhu cầu trong một yêu cầu (Multi-Intent Combined Workflows)](#tình-huống-14-kết-hợp-nhiều-nhu-cầu-trong-một-yêu-cầu-multi-intent-combined-workflows)

---

### Tình huống 1: Viết thông thường (Interactive Scene/Chapter Writing)
- **Điểm bắt đầu:** Đã có truyện đang hoạt động (`active_story`), muốn viết tiếp 1 chương mới dưới sự tương tác và duyệt từng bước.
- **Skill kích hoạt:** `story-write` (hoặc bắt đầu bằng `/story`).
- **Prompt mẫu:**
  > "/story Tôi muốn viết tiếp chương tiếp theo cho truyện đang chọn. Tập trung vào cảnh nhân vật chính đàm phán với bang chủ Thiết Huyết Bang trong tửu lầu lúc đêm muộn."
- **Quy trình thực thi:**
  1. Router `/story` nhận diện ý định viết tiếp, chạy `python manage_story.py status` để xác định truyện hiện hành và chương kế tiếp ($N$).
  2. Router chuyển tiếp vào `skills/story-write/SKILL.md`.
  3. Agent nạp ngữ cảnh 5 lớp: mục tiêu chương $N$, chấn thương hiện tại, túi đồ vật phẩm, ma trận bí mật và đoạn kết chương $N-1$.
  4. Lập kế hoạch phân cảnh: POV, điểm đầu - điểm cuối, mâu thuẫn chính, thông tin được phép tiết lộ.
  5. Soạn thảo văn xuôi trực tiếp vào `chapters/chapter_XXXX.md` (Native Markdown) hoặc `chapters/draft.md`.
  6. Chạy chốt chặn kiểm tra:
     ```powershell
     python manage_story.py check --file chapters/chapter_XXXX.md
     python manage_story.py memory --audit --file chapters/chapter_XXXX.md
     ```
  7. Sửa lỗi Critical (nếu có), trình bày bản thảo cho tác giả.
  8. Sau khi tác giả hài lòng, đồng bộ Narrative Memory:
     ```powershell
     python manage_story.py memory --add-event --chapter N --title "[Tiêu đề]" --summary "[Tóm tắt sự kiện]"
     ```
- **Cách tiếp tục:** Yêu cầu chuyển sang chương tiếp theo hoặc biên tập đoạn vừa viết.
- **Hành vi khi gặp lỗi:** Nếu phát hiện mâu thuẫn chấn thương (ví dụ tay gãy vung kiếm), Agent dừng lại và gợi ý sửa trước khi cập nhật Memory.

---

### Tình huống 2: Viết khám phá, chưa có đề cương (Pantser / Exploratory Writing)
- **Điểm bắt đầu:** Tác giả chưa có dàn ý cụ thể, chỉ có một cảm xúc hoặc một biến cố bất ngờ muốn thử nghiệm.
- **Skill kích hoạt:** `story-write`.
- **Prompt mẫu:**
  > "/story-write Tôi chưa có đề cương chương này. Cứ để nhân vật chính bất ngờ bị tập kích khi đang băng qua rừng phong đỏ. Xem phản xạ của hắn thế nào rồi tùy cơ ứng biến."
- **Quy trình thực thi:**
  1. Agent nạp trạng thái hiện thời của nhân vật từ `summaries/characters.md` (vũ khí đang mang, thương tích thể xác, tu vi).
  2. Không ép buộc đối chiếu mục tiêu Arc dài hạn; thiết lập xung đột cục bộ tại chỗ (Surprise Attack): kẻ tập kích là ai, động cơ là gì.
  3. Áp dụng kỹ thuật Show, Don't Tell: miêu tả tiếng xào xạc của lá phong khô, mùi ẩm ướt của đất rừng, nhịp thở đứt quãng khi né một mũi tên ngầm.
  4. Triển khai phân cảnh văn xuôi giàu cảm giác.
  5. Sau khi cảnh hoàn thành, Agent tổng kết:
     - Biến cố mới xảy ra: [Bị thích khách áo đen ám sát hụt].
     - Manh mối mới thu thập: [Tìm thấy lệnh bài Ma Tông rơi lại].
  6. Agent hỏi tác giả: *"Bạn có muốn ghi nhận biến cố này vào dòng sự kiện chính thức không?"*
  7. Nếu đồng ý, cập nhật Timeline và bổ sung vào `summaries/outline.md` cho các chương sau.
- **Hành vi khi gặp lỗi:** Nếu tình tiết khám phá vi phạm quy tắc thế giới trong `canon.md`, Agent cảnh báo để tác giả chọn: điều chỉnh tình tiết hoặc sửa Canon thế giới.

---

### Tình huống 3: Viết truyện dài nhiều chương (Long-form Novel Pipeline)
- **Điểm bắt đầu:** Bắt đầu một bộ tiểu thuyết trường thiên dài hàng chục chương hoặc một Arc truyện mới.
- **Skill kích hoạt:** `story` → `story-flow` & `story-outline`.
- **Prompt mẫu:**
  > "/story Tôi muốn khởi tạo bộ truyện tiên hiệp dài tập 'Dạ Ma Chi Đạo', tác giả Lãnh Phong. Cần xây dựng Arc 1 gồm 10 chương từ phế tích gia tộc đến khi gia nhập Thanh Vân Môn."
- **Quy trình thực thi:**
  1. Khởi tạo dự án:
     ```powershell
     python manage_story.py init --title "Dạ Ma Chi Đạo" --author "Lãnh Phong" --genre "Tiên Hiệp" --id "da-ma-chi-dao"
     ```
  2. Kích hoạt `story-outline` để lập dàn ý tổng quan và chi tiết Arc 1 (Chương 1 đến 10), lưu vào `summaries/outline.md`.
  3. Khởi tạo Canon thế giới (hệ thống cảnh giới, các môn phái, lời tiên tri) và nhân vật chính vào `summaries/canon.md` và `summaries/characters.md`.
  4. Bắt đầu viết từ Chương 1 qua chu trình `story-flow`.
  5. Mỗi khi hoàn tất 5-10 chương, chạy lệnh tóm tắt mốc để nén ngữ cảnh:
     ```powershell
     python manage_story.py append-summary --from 1 --to 10 --text "[Tóm tắt đại ý Arc 1]"
     ```
- **Cách tiếp tục:** Chạy `python manage_story.py status` để kiểm tra số chương hiện có và tiến hành viết chương tiếp theo.
- **Hành vi khi gặp lỗi:** Nếu bộ nhớ quá tải token, Agent ưu tiên nạp `rolling_summary.txt` và tóm tắt ngắn của các chương gần nhất thay vì đọc toàn văn các chương cũ.

---

### Tình huống 4: Tự động viết nhiều chương trong phạm vi cho phép (Autonomous Mode)
- **Điểm bắt đầu:** Đã có sẵn đề cương chi tiết cho các chương tiếp theo (ví dụ: Chương 3, 4, 5). Tác giả muốn AI tự hành viết trọn vẹn chặng này mà không dừng lại hỏi từng câu.
- **Skill kích hoạt:** `story-flow` (Autonomous Mode).
- **Prompt mẫu:**
  > "/story-flow Chạy chế độ tự hành viết liên tiếp từ Chương 3 đến Chương 5 theo đề cương có sẵn trong outline.md. Tự kiểm tra slop và cập nhật Memory sau mỗi chương."
- **Quy trình thực thi chu trình lặp (Autonomous Loop):**
  - **Vòng lặp Chương 3:**
    1. Đọc mục tiêu Chương 3 từ `outline.md` và đoạn kết Chương 2.
    2. Chấp bút viết hoàn chỉnh `chapters/chapter_0003.md`.
    3. Chạy kiểm tra: `python manage_story.py check --file chapters/chapter_0003.md` và `memory --audit`.
    4. Sửa các lỗi từ ngữ sáo rỗng hoặc dấu câu nếu có.
    5. Cập nhật Memory: `python manage_story.py memory --add-event --chapter 3 --title "..." --summary "..."`.
  - **Vòng lặp Chương 4:**
    1. Đọc mục tiêu Chương 4 từ `outline.md` và đoạn kết Chương 3.
    2. Viết `chapters/chapter_0004.md`, chạy audit, sửa lỗi, đồng bộ Memory.
  - **Vòng lặp Chương 5:**
    1. Viết `chapters/chapter_0005.md`, chạy audit, sửa lỗi, đồng bộ Memory.
  - **Kết thúc chặng:** Agent xuất báo cáo tổng hợp: Đã hoàn thành 3 chương (tổng 7.200 chữ), các sự kiện đã ghi nhận, và mục tiêu của Chương 6.
- **Fail-Safe (Dừng khẩn cấp):** Nếu ở Chương 4 phát sinh tình huống bất ngờ cần thay đổi số phận nhân vật quan trọng hoặc mâu thuẫn Canon thế giới, Agent tạm dừng ngay lập tức, báo cáo vị trí và chờ tác giả chỉ đạo.

---

### Tình huống 5: Sáng tác có mẫu văn phong (Writing with Style Profile)
- **Điểm bắt đầu:** Bạn có file truyện mẫu yêu thích (ví dụ trích đoạn Kim Dung, Cổ Long hoặc truyện cá nhân) và muốn áp dụng giọng văn này.
- **Skill kích hoạt:** `story-study` → `story-write`.
- **Prompt mẫu:**
  > "/story-study Hãy phân tích văn phong từ file 'samples/kiem-hiep-mau.txt', tạo profile tên 'co-long-style'. Sau đó áp dụng profile này để viết chương tiếp theo."
- **Quy trình thực thi:**
  1. Chạy phân tích định lượng 5 trục:
     ```powershell
     python manage_story.py style --learn samples/kiem-hiep-mau.txt --profile co-long-style --scope story
     ```
  2. Agent thực hiện phân tích văn học ngữ nghĩa: bóc tách nhịp ngắt câu, mật độ đối thoại, cách dùng hình ảnh ẩn dụ (không sao chép tình tiết nhân vật mẫu).
  3. Kích hoạt profile làm việc:
     ```powershell
     python manage_story.py style --set co-long-style
     ```
  4. Chạy `python manage_story.py context` để kiểm tra các chỉ dẫn văn phong (ví dụ: câu ngắn > 45%, nhịp thở dồn dập, đối thoại đa tầng).
  5. Chấp bút chương mới tuân thủ nghiêm ngặt theo các chỉ số và gợi ý của profile `co-long-style`.
- **Hành vi khi gặp lỗi:** Nếu bản nháp bị lệch phong cách (ví dụ câu quá dài, giải thích trừu tượng), bước audit sẽ cảnh báo Soft Variance để điều chỉnh.

---

### Tình huống 6: Sáng tác không có mẫu văn phong (Writing with Default Style)
- **Điểm bắt đầu:** Không có file mẫu, muốn viết tự nhiên với phong cách tiếng Việt chuẩn mực, giàu cảm xúc và hình ảnh giác quan.
- **Skill kích hoạt:** `story-write`.
- **Prompt mẫu:**
  > "/story-write Tôi không có văn mẫu. Hãy viết chương 1 theo phong cách trần thuật ngôi thứ ba cân bằng, áp dụng triệt để Show, Don't Tell và chiều sâu 5 giác quan."
- **Quy trình thực thi:**
  1. Hệ thống tự động sử dụng cấu hình mặc định (Balanced 3rd Person Voice).
  2. Nạp quy tắc từ [references/show-dont-tell.md](references/show-dont-tell.md) và [references/anti-slop.md](references/anti-slop.md).
  3. Chấp bút với các nguyên tắc chuẩn:
     - Tỷ lệ thoại 30-40%, xen kẽ động tác cơ thể (beat).
     - Kích hoạt ít nhất 3/5 giác quan trong mỗi khung cảnh.
     - Loại bỏ hoàn toàn các từ ngữ sáo rỗng (*"không thể phủ nhận", "như ngưng đọng"*).
  4. Chạy `python manage_story.py check` để đảm bảo văn phong trong sáng, thuần Việt.

---

### Tình huống 7: Sáng tác khi đã có đề cương (Writing with Established Outline)
- **Điểm bắt đầu:** File `summaries/outline.md` đã được biên soạn chi tiết từng chương.
- **Skill kích hoạt:** `story-write`.
- **Prompt mẫu:**
  > "/story-write Bám sát đề cương Chương 4 trong outline.md: 'Lạc lối trong Vạn Ma Quật và cuộc đối đầu với Xích Luyện Xà'. Viết chi tiết khoảng 2.000 chữ."
- **Quy trình thực thi:**
  1. Agent đọc trực tiếp `summaries/outline.md`, trích xuất mục tiêu và trở lực của Chương 4.
  2. Đối soát với `summaries/characters.md` xem nhân vật đang ở trạng thái nào sau Chương 3 (vết thương độc chưa khỏi, pháp bảo đã hao tổn).
  3. Viết văn xuôi bám sát diễn biến đã định: vào hang động → cạm bẫy trận pháp → Xích Luyện Xà xuất hiện → trận chiến giằng co → lối thoát hiểm mở ra.
  4. Lưu chương và cập nhật Timeline.
- **Lưu ý:** Không tự ý chèn thêm các sự kiện làm thay đổi kế hoạch của Chương 5 nếu không có sự đồng ý của tác giả.

---

### Tình huống 8: Sáng tác khi chưa có đề cương (Writing without Outline)
- **Điểm bắt đầu:** Tác phẩm mới tạo, `outline.md` đang trống hoặc chỉ có 1 dòng ý tưởng sơ khai.
- **Skill kích hoạt:** `story-outline`.
- **Prompt mẫu:**
  > "/story-outline Tôi chỉ có ý tưởng: 'Một đầu bếp hiện đại xuyên không về thế giới ma pháp, mở quán ăn cứu rỗi các ma vương'. Giúp tôi lập dàn ý Arc 1 gồm 5 chương."
- **Quy trình thực thi:**
  1. Agent phân tích ý tưởng: xác định Hook chính, xung đột trung tâm (văn hóa ẩm thực vs ma pháp bạo lực), và động cơ nhân vật.
  2. Đề xuất cấu trúc Arc 1 (Chương 1 - 5) theo mô hình 3 hồi kinh điển:
     - Chương 1: Biến cố xuyên không, quán ăn đổ nát, món khai vị đầu tiên.
     - Chương 2: Vị khách đặc biệt đầu tiên (tiểu yêu quái đói lử) và tin đồn lan truyền.
     - Chương 3: Trở lực xuất hiện: bang phái địa phương đến tống tiền bảo kê.
     - Chương 4: Khách hàng quyền lực (thị vệ của Ma Vương) ghé quán và thử thách món ăn.
     - Chương 5: Đỉnh điểm Arc: cứu sống thuộc hạ Ma Vương qua món canh giải độc, nhận được sự bảo hộ đầu tiên.
  3. Ghi đề cương vào `summaries/outline.md`.
  4. Hỏi tác giả: *"Bạn có muốn chỉnh sửa điểm nào trước khi bắt tay viết Chương 1 không?"*

---

### Tình huống 9: Tiếp tục tác phẩm có sẵn (Resuming an Existing Project)
- **Điểm bắt đầu:** Mở lại dự án sau vài ngày hoặc chuyển sang phiên làm việc mới, muốn nắm lại tiến độ và viết tiếp.
- **Skill kích hoạt:** `story`.
- **Prompt mẫu:**
  > "/story Tôi muốn tiếp tục viết bộ truyện 'Vu Su Huyen Thoai'. Hiện tại truyện đang dừng ở đâu và mục tiêu tiếp theo là gì?"
- **Quy trình thực thi:**
  1. Chạy lệnh kiểm tra danh sách và trạng thái:
     ```powershell
     python manage_story.py select --id vu-su-huyen-thoai
     python manage_story.py status
     ```
  2. Nạp ngữ cảnh nén:
     ```powershell
     python manage_story.py context
     ```
  3. Agent báo cáo tóm tắt cho tác giả:
     - Số chương hiện có: 14 chương.
     - Chương vừa viết xong: Chương 14 (Tóm tắt: Lâm Phong phá vỡ phong ấn tầng 2).
     - Trạng thái nhân vật: Đang bị kiệt sức linh lực, nắm giữ chìa khóa Cổ Giới.
     - Manh mối chưa giải: Bức thư màu đen chưa mở.
     - Mục tiêu Chương 15: Tiến vào tế đàn cổ đại.
  4. Sẵn sàng viết Chương 15 ngay khi tác giả gõ "Viết tiếp".

---

### Tình huống 10: Biên tập một đoạn hoặc phân cảnh (Local Editing & Scene Polishing)
- **Điểm bắt đầu:** Đã có file chương hoàn chỉnh, nhưng một đoạn thoại hoặc cảnh chiến đấu bị gượng ép, muốn viết lại riêng đoạn đó.
- **Skill kích hoạt:** `story-write` hoặc `story-deslop`.
- **Prompt mẫu:**
  > "/story-write Trong file 'chapters/chapter_0005.md', đoạn đối thoại từ dòng 40 đến 65 giữa Lâm Phong và sư tỷ bị khô khan quá. Hãy viết lại đoạn này cho sắc sảo hơn, có nhiều cử chỉ cơ thể và ẩn ý ngầm, giữ nguyên các đoạn còn lại."
- **Quy trình thực thi:**
  1. Agent đọc đoạn văn được chỉ định bằng công cụ `read_file`.
  2. Giữ nguyên bối cảnh và mục đích của cuộc đối thoại.
  3. Áp dụng kỹ thuật Subtext & Beat:
     - Thêm cử chỉ: ánh mắt lướt qua chuôi kiếm, cái nghiêng đầu dò xét, chén trà nguội ngắt trên bàn.
     - Thay câu thoại bộc bạch trực diện bằng lời nói bóng gió, hai tầng nghĩa.
  4. Dùng `edit_file` thay thế chính xác khối văn bản từ dòng 40 đến 65 trong `chapters/chapter_0005.md`.
  5. Chạy `python manage_story.py check --file chapters/chapter_0005.md` để đảm bảo không lỗi dấu câu.
  6. Tuyệt đối không viết lại toàn bộ chương làm mất đi những câu chữ ưng ý khác của tác giả.

---

### Tình huống 11: Thẩm định và kiểm tra lỗi (Review & Audit 4 Tiers)
- **Điểm bắt đầu:** Vừa viết xong một chương dài hoặc một Arc, cần thẩm định toàn diện tính logic và chất lượng văn chương.
- **Skill kích hoạt:** `story-review`.
- **Prompt mẫu:**
  > "/story-review Hãy đóng vai độc giả khó tính thẩm định toàn bộ Chương 8 vừa viết. Soát kỹ lỗi logic chấn thương và xem nhịp điệu có bị quá nhanh không."
- **Quy trình thực thi:**
  1. Chạy công cụ kiểm tra tự động:
     ```powershell
     python manage_story.py memory --audit --file chapters/chapter_0008.md
     ```
  2. Agent kích hoạt 3 vai phản biện độc lập:
     - Vai 1: Soát Logic bối cảnh & Continuity (đối chiếu `characters_state.json`, `events.json`).
     - Vai 2: Đánh giá Tiết tấu & Nhịp thở (câu dài ngắn, điểm treo móc cuối chương).
     - Vai 3: Soát Giọng điệu & Tính cách nhân vật (nguy cơ OOC, động cơ hành động).
  3. Xuất Báo cáo Thẩm định 4 Cấp độ:
     - 🔴 Critical: Chỉ ra lỗi logic bắt buộc sửa (nếu có).
     - 🟡 Significant: Đề xuất cải thiện chuyển cảnh và tương tác giác quan.
     - 🟢 Soft: Nhận xét về độ dài câu.
     - 🎨 Artistic Choice: Ghi nhận và bảo toàn các nét phá cách nghệ thuật.
- **Lưu ý:** Agent không tự ý sửa bản thảo, chỉ đề xuất để tác giả quyết định.

---

### Tình huống 12: Khử văn phong máy móc (Anti-Slop & Deslop Purification)
- **Điểm bắt đầu:** Bản thảo có nhiều câu sáo rỗng (*"không thể không thừa nhận", "bầu không khí ngưng đọng"*), muốn làm sạch câu từ.
- **Skill kích hoạt:** `story-deslop`.
- **Prompt mẫu:**
  > "/story-deslop Quét và làm sạch văn mẫu AI cho file 'chapters/chapter_0003.md'. Áp dụng danh sách ngoại lệ .deslop-whitelist nếu có."
- **Quy trình thực thi:**
  1. **Bước quét chẩn đoán (Scan Mode):**
     Chạy kiểm tra tự động:
     ```powershell
     python manage_story.py check --file chapters/chapter_0003.md
     ```
  2. Liệt kê các vị trí vi phạm cụ thể kèm đoạn trích và phân tích nhược điểm.
  3. **Bước sửa chữa có kiểm soát (Fix Mode):**
     - Áp dụng nguyên tắc Cắt gọt 20%: xóa các câu giải thích trừu tượng thừa thãi.
     - Thay thế các cụm từ sáo rỗng bằng hành động thể chất và chi tiết giác quan cụ thể.
     - Bỏ qua các từ ngữ nằm trong file `.deslop-whitelist`.
  4. Lưu file và chạy lại lệnh kiểm tra để xác nhận đạt chuẩn 100%.

---

### Tình huống 13: Tạo prompt ảnh bìa tiểu thuyết AI (Novel Cover Art Generation)
- **Điểm bắt đầu:** Đã có thông tin truyện hoặc ý tưởng bìa, cần tạo prompt vẽ ảnh chuẩn cho AI Art.
- **Skill kích hoạt:** `story-cover`.
- **Prompt mẫu:**
  > "/story-cover Thiết kế bộ prompt vẽ ảnh bìa cho truyện 'Dạ Ma Chi Đạo'. Nhân vật chính là kiếm sĩ cô độc trên đỉnh núi tuyết, tông màu u tối điểm xuyết kim sắc."
- **Quy trình thực thi:**
  1. Agent trích xuất tên truyện, thể loại, ngoại hình nhân vật từ dự án.
  2. Phân bổ bố cục 3 phần: khoảng trống phía trên cho Tựa đề, điểm nhấn nhân vật ở giữa, khoảng trống phía dưới cho Tên tác giả.
  3. Xuất trọn bộ prompt tiếng Anh tối ưu cho Midjourney v6 (`--ar 2:3 --v 6.0`), DALL-E 3 và Stable Diffusion XL.
  4. Kèm hướng dẫn lựa chọn font chữ và vị trí đặt typography phù hợp với không khí truyện.

---

### Tình huống 14: Kết hợp nhiều nhu cầu trong một yêu cầu (Multi-Intent Combined Workflows)
- **Điểm bắt đầu:** Tác giả đưa ra yêu cầu phức tạp gồm nhiều công đoạn: học văn phong, lập đề cương rồi viết luôn chương 1.
- **Skill kích hoạt:** `story` (Central Router điều phối chuỗi tuần tự).
- **Prompt mẫu:**
  > "/story Hãy học văn phong từ file 'samples/kiem-hiep.txt' đặt tên profile là 'kiem-hiep-co-dien', sau đó lập đề cương 3 chương đầu cho bộ truyện mới 'Bạch Y Hiệp Khách' và viết luôn Chương 1."
- **Quy trình xử lý tuần tự của Router:**
  1. **Công đoạn 1 (Style):** Gọi `story-study` phân tích file mẫu và tạo profile `kiem-hiep-co-dien`.
  2. **Công đoạn 2 (Init):** Chạy `python manage_story.py init --title "Bạch Y Hiệp Khách" --id "bach-y-hiep-khach"` và kích hoạt profile vừa tạo.
  3. **Công đoạn 3 (Outline):** Gọi `story-outline` biên soạn đề cương 3 chương đầu vào `summaries/outline.md`.
  4. **Công đoạn 4 (Write):** Gọi `story-write` nạp ngữ cảnh Chương 1, áp dụng Style Profile vừa học, chấp bút hoàn thiện `chapters/chapter_0001.md`, chạy audit và đồng bộ Memory.
  5. **Báo cáo tổng kết:** Trình bày kết quả cả 4 công đoạn rõ ràng cho tác giả trong một phản hồi duy nhất.
