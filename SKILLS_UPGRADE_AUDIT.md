# BÁO CÁO KIỂM TOÁN VÀ KHẢO SÁT NÂNG CẤP HỆ THỐNG SKILLS (SVB-STORY)
**Repository:** `svb-story` (`c:\Novels\CreateSkills\story-flow`)  
**Remote Git:** `https://github.com/7binh/svb-story.git`  
**Commit cơ sở kiểm toán:** `622e324` (`feat: add /story-study skill, 5-axis style engine and style enforcement pipeline`)  
**Ngày thực hiện:** 21/10/2026  
**Chế độ kiểm toán:** DISCOVERY & AUDIT ONLY (Không thay đổi mã nguồn, không xóa sửa file hiện có, không commit Git)  
**Kiểm toán viên:** Senior AI Agent Architect  

---

## 1. MỤC TIÊU VÀ PHẠM VI KIỂM TOÁN

### 1.1. Mục tiêu
Cuộc kiểm toán được thực hiện nhằm rà soát độc lập, toàn diện và khách quan toàn bộ hệ thống Skills, cấu trúc instruction hierarchy, cơ chế điều phối CLI, luồng dữ liệu, các script vệ tinh và tài liệu trong repository `svb-story`. Mục đích là thu thập đầy đủ bằng chứng kỹ thuật, xác định các nợ kỹ thuật (technical debt), lỗ hổng vận hành, sự không nhất quán giữa tài liệu và mã nguồn, cũng như các điểm nghẽn kiến trúc trước khi lập phương án nâng cấp tổng thể.

### 1.2. Phạm vi kiểm toán
- **Thư mục kiểm toán:** `c:\Novels\CreateSkills\story-flow` (toàn bộ các file được quản lý bởi Git và trạng thái working tree).
- **Các thành phần được kiểm tra:**
  1. Entrypoint điều phối trung tâm: `manage_story.py`.
  2. Toàn bộ 9 định nghĩa Skill trong `skills/`: `story`, `story-write`, `story-study`, `story-outline`, `story-deslop`, `story-review`, `story-cover`, `story-import`, `story-flow`.
  3. Toàn bộ 4 kịch bản tự động hóa trong `scripts/`: `style_analyzer.py`, `check-ai-patterns.js`, `normalize-punctuation.js`, `dashboard-server.mjs`.
  4. Toàn bộ tài liệu tham chiếu trong `references/`: `anti-slop.md`, `plot-branching.md`, `show-dont-tell.md`, cùng 10 file phong cách thể loại trong `references/genre-styles/`.
  5. Các tệp giao diện Web Dashboard trong `assets/`: `index.html`, `app.js`, `styles.css`, `tokens.css`.
  6. Thư mục dữ liệu tác phẩm `stories/` và các quy ước lưu trữ.
  7. Tài liệu hướng dẫn `README.md` và cấu hình bỏ qua `.gitignore`.

### 1.3. Nguyên tắc an toàn
Kiểm toán tuân thủ tuyệt đối 10 quy tắc an toàn: Không chỉnh sửa, xóa, di chuyển hoặc đổi tên file; không chạy Git commit, push, checkout; không cài đặt dependency; chỉ tạo duy nhất file báo cáo này tại thư mục gốc.

---

## 2. TRẠNG THÁI GIT VÀ MÔI TRƯỜNG KIỂM TOÁN

### 2.1. Trạng thái Git trước kiểm toán
- **Branch:** `main`
- **Upstream:** `origin/main` (đồng bộ hoàn toàn, không có commit đi trước hoặc đi sau).
- **Working Tree:** `clean` (không có file sửa đổi unstaged, không có staged changes).
- **Commit mới nhất:** `622e324` (`feat: add /story-study skill, 5-axis style engine and style enforcement pipeline`).
- **Lịch sử 4 commit gần nhất:**
  - `622e324`: Bổ sung skill `/story-study`, module `style_analyzer.py` 5 trục và pipeline tuân thủ văn phong.
  - `64d35bd`: Xóa `SKILL.md` ở thư mục gốc để bộ nạp `npx skills add` quét được toàn bộ các sub-skill trong `skills/`.
  - `adad8b1`: Tách module hóa thành 8 skill con chuyên biệt.
  - `6e29020`: Commit khởi tạo dự án StoryFlow (`svb-story`).

### 2.2. Trạng thái tệp bị bỏ qua (Ignored Files)
- Kiểm tra bằng lệnh `rtk git status --ignored` phát hiện duy nhất thư mục:
  - `scripts/__pycache__/` (chứa bytecode Python của `style_analyzer.cpython-312.pyc`).
- Không phát hiện file cấu hình nhạy cảm (`.env`), file token hay file khóa riêng tư nào trong working tree.

### 2.3. Môi trường thực thi
- **Hệ điều hành:** Windows 11 Pro (Kiến trúc x64, hệ thống tệp NTFS).
- **Python Runtime:** Python 3.12+ (đã xác thực khả năng thực thi qua `manage_story.py`).
- **Node.js Runtime:** Node.js v24.18.1 (sử dụng chạy các script JavaScript/ESM).
- **Hệ vỏ lệnh:** PowerShell 5.1 / PowerShell 7 với proxy tối ưu token RTK.

---

## 3. DANH MỤC TỔNG THỂ CÁC FILE VÀ THƯ MỤC

Dưới đây là bảng kiểm kê toàn bộ các tài nguyên trong repository:

| STT | Đường dẫn tương đối | Phân loại | Dung lượng (bytes) | Vai trò trong hệ thống | Tình trạng kiểm toán |
|---|---|---|---|---|---|
| 1 | `.gitignore` | Config | 95 | Khai báo các file bỏ qua (cache, `active_story.json`) | CONFIRMED |
| 2 | `manage_story.py` | Source (Python) | 46,252 | CLI Engine điều phối dữ liệu, trạng thái, bóc tách nháp và gọi scripts | CONFIRMED |
| 3 | `README.md` | Documentation | 4,794 | Hướng dẫn sử dụng và giới thiệu hệ sinh thái StoryFlow | CONFIRMED (Có sai lệch) |
| 4 | `skills/story/SKILL.md` | Instruction | 1,895 | Router Skill điều hướng tổng quan | CONFIRMED |
| 5 | `skills/story-write/SKILL.md` | Instruction | 3,577 | Skill quy trình viết 5 bước chuyên sâu | CONFIRMED |
| 6 | `skills/story-study/SKILL.md` | Instruction | 5,568 | Skill giải mã văn phong 5 trục & Style Pipeline | CONFIRMED |
| 7 | `skills/story-outline/SKILL.md` | Instruction | 3,091 | Skill đề cương thích ứng & phục bút | CONFIRMED |
| 8 | `skills/story-deslop/SKILL.md` | Instruction | 1,885 | Skill khử văn mẫu AI & Show Don't Tell | CONFIRMED |
| 9 | `skills/story-review/SKILL.md` | Instruction | 2,367 | Skill thẩm định phản biện 3 vai độc giả | CONFIRMED |
| 10 | `skills/story-cover/SKILL.md` | Instruction | 1,514 | Skill thiết kế prompt ảnh bìa tiểu thuyết AI | CONFIRMED |
| 11 | `skills/story-import/SKILL.md` | Instruction | 1,691 | Skill nghịch đảo bản thảo cũ vào cấu trúc truyện | CONFIRMED |
| 12 | `skills/story-flow/SKILL.md` | Instruction | 7,654 | Skill nguyên bản tổng quát (Monolithic Legacy) | CONFIRMED (Trùng lặp) |
| 13 | `scripts/style_analyzer.py` | Source (Python) | 15,546 | Module trích xuất 5 trục văn phong & sinh báo cáo Markdown | CONFIRMED |
| 14 | `scripts/check-ai-patterns.js` | Source (Node.js) | 76,860 | Quét văn mẫu AI (gốc `.agents`, tiếng Trung) | CRITICAL ERROR (Crash) |
| 15 | `scripts/normalize-punctuation.js` | Source (Node.js) | 13,895 | Chuẩn hóa dấu câu hội thoại (gốc `.agents`) | CRITICAL ERROR (Crash) |
| 16 | `scripts/dashboard-server.mjs` | Source (Node.js) | 34,002 | Server HTTP Web Dashboard cục bộ (gốc `.agents`) | DEFECTIVE (Lệch cấu trúc) |
| 17 | `references/anti-slop.md` | Reference | 1,483 | Danh sách đen từ ngữ sáo rỗng (tiếng Việt) | CONFIRMED |
| 18 | `references/plot-branching.md` | Reference | 1,811 | Quy chuẩn gợi ý 3 nhánh rẽ cốt truyện (A/B/C) | CONFIRMED |
| 19 | `references/show-dont-tell.md` | Reference | 2,056 | Hướng dẫn kỹ thuật cảm xúc vật lý & 5 giác quan | CONFIRMED |
| 20 | `references/genre-styles/世情打脸.md` | Reference (CN) | 16,410 | Tài liệu thể loại: Thế tình vả mặt / Luân thường | UNVERIFIED (Chưa Việt hóa) |
| 21 | `references/genre-styles/双男主.md` | Reference (CN) | 12,447 | Tài liệu thể loại: Song nam chủ / Đam mỹ | UNVERIFIED (Chưa Việt hóa) |
| 22 | `references/genre-styles/复仇打脸.md` | Reference (CN) | 14,767 | Tài liệu thể loại: Báo thù vả mặt | UNVERIFIED (Chưa Việt hóa) |
| 23 | `references/genre-styles/宅斗宫斗.md` | Reference (CN) | 15,574 | Tài liệu thể loại: Trạch đấu / Cung đấu | UNVERIFIED (Chưa Việt hóa) |
| 24 | `references/genre-styles/总裁豪门.md` | Reference (CN) | 17,204 | Tài liệu thể loại: Tổng tài hào môn | UNVERIFIED (Chưa Việt hóa) |
| 25 | `references/genre-styles/悬疑.md` | Reference (CN) | 13,729 | Tài liệu thể loại: Huyền nghi / Trinh thám | UNVERIFIED (Chưa Việt hóa) |
| 26 | `references/genre-styles/民俗怪谈.md` | Reference (CN) | 13,054 | Tài liệu thể loại: Dân tục quái đàm | UNVERIFIED (Chưa Việt hóa) |
| 27 | `references/genre-styles/沙雕脑洞.md` | Reference (CN) | 14,578 | Tài liệu thể loại: Hài hước não động | UNVERIFIED (Chưa Việt hóa) |
| 28 | `references/genre-styles/甜宠.md` | Reference (CN) | 12,003 | Tài liệu thể loại: Điềm sủng / Ngọt ngào | UNVERIFIED (Chưa Việt hóa) |
| 29 | `references/genre-styles/追妻火葬场.md` | Reference (CN) | 15,960 | Tài liệu thể loại: Truy thê hỏa táng tràng | UNVERIFIED (Chưa Việt hóa) |
| 30 | `assets/index.html` | Asset (HTML) | 10,502 | Giao diện Dashboard (OH STORY tiếng Trung) | DEFECTIVE (Chưa Việt hóa) |
| 31 | `assets/app.js` | Asset (JS) | 39,987 | Client script xử lý API Dashboard | DEFECTIVE (Khớp cấu trúc CN) |
| 32 | `assets/styles.css` | Asset (CSS) | 28,531 | Bảng kiểu giao diện Dashboard | CONFIRMED |
| 33 | `assets/tokens.css` | Asset (CSS) | 9,372 | Biến màu sắc & typography theme | CONFIRMED |
| 34 | `stories/.gitkeep` | Anchor | 0 | Giữ thư mục `stories/` trong Git | CONFIRMED |

---

## 4. BẢNG KIỂM TOÁN CHI TIẾT TỪNG SKILL

### 4.1. Skill: `story`
- **Slash command:** `/story` (hoặc `$story`, `/truyện`).
- **File path:** `skills/story/SKILL.md`.
- **Trigger:** Người dùng gõ `/story`, `$story`, hoặc hỏi: "viết truyện", "quản lý truyện", "mở dashboard".
- **Scope:** Trạm Router dẫn đường trung tâm, cung cấp bảng tra cứu lệnh, điều hướng đến các skill con chuyên biệt và cung cấp lệnh CLI quản trị cơ bản (`stories`, `select`, `init`, `status`).
- **Input:** Tùy ý từ tác giả (yêu cầu định hướng hoặc chuyển tác phẩm).
- **Output:** Danh sách gợi ý skill phù hợp hoặc thực thi lệnh chọn tác phẩm.
- **Workflow:** Tra cứu nhu cầu tác giả -> Hiển thị cú pháp slash command phù hợp -> Hướng dẫn lệnh CLI.
- **Dependencies:** `manage_story.py`.
- **Integration:** Trỏ trực tiếp đến 8 skill con còn lại.
- **Failure handling:** Không có logic tự xử lý lỗi, chỉ hướng dẫn văn bản.
- **Validation:** Không có kiểm thử tự động.
- **Observed gaps:** Không kiểm tra xem truyện hiện tại đã được chọn (`active_story.json`) chưa trước khi hướng dẫn.

### 4.2. Skill: `story-write`
- **Slash command:** `/story-write` (hoặc `/story-flow`).
- **File path:** `skills/story-write/SKILL.md`.
- **Trigger:** `/story-write`, `/story-flow`, "viết chương", "tiếp tục viết", "mở rộng nháp".
- **Scope:** Quy trình viết và hoàn thiện một chương truyện khép kín theo 5 bước, thực thi Style Enforcement Pipeline.
- **Input:** Ý tưởng, đoạn test thô của tác giả, hoặc đề cương chương kế tiếp.
- **Output:** File chương hoàn chỉnh tại `stories/<id>/chapters/chapter_XXXX.md`, index cập nhật trong `story.json`.
- **Workflow:** 
  1. `python manage_story.py context`: Đọc tóm tắt, 1 chương trước, mục tiêu chương và quy tắc văn phong active.
  2. Soạn nháp vào `stories/<id>/chapters/draft.md` với cú pháp `/story-title` và `/story-brief`.
  3. `python manage_story.py check`: Kiểm tra chất lượng và tự đối chiếu 5 trục văn phong.
  4. `python manage_story.py save`: Lưu chương vào kho dữ liệu.
  5. Cập nhật hồ sơ nhân vật/bối cảnh/tóm tắt mốc nếu cần.
- **Dependencies:** `manage_story.py`, `references/show-dont-tell.md`, `STYLE_PROFILE.md`.
- **Integration:** Kế thừa ngữ cảnh từ `story-study` (Style Rules), phối hợp với `story-deslop` và `story-review`.
- **Failure handling:** Bắt buộc có `/story-title` ở dòng 1; cảnh báo nếu thiếu chương liền trước.
- **Validation:** Dựa vào `manage_story.py check`.
- **Observed gaps:** Bước 3 phụ thuộc vào lệnh `check`, nhưng `check` hiện đang bị crash ngầm ở tầng Node.js script.

### 4.3. Skill: `story-study`
- **Slash command:** `/story-study`.
- **File path:** `skills/story-study/SKILL.md`.
- **Trigger:** `/story-study`, "học văn phong", "nghiên cứu văn phong", "học truyện mẫu".
- **Scope:** Giải mã văn phong từ 3 nguồn (thư mục, file, dán nháp `draft.md`), bóc tách 5 trục, sinh `style_profile.json` và `STYLE_PROFILE.md`, hỗ trợ quản lý Multi-Profile.
- **Input:** Đường dẫn file/thư mục văn bản mẫu (.txt, .md) hoặc văn bản dán trực tiếp dưới dòng `/story-study`.
- **Output:** Hồ sơ văn phong độc lập tại `stories/<id>/summaries/style_profiles/<name>/`, cập nhật `active_style_profile.json`.
- **Workflow:** Nạp văn bản mẫu -> Chạy `scripts/style_analyzer.py` -> Tính toán 5 trục -> Sinh Markdown báo cáo -> Lưu và kích hoạt profile -> Nạp vào chỉ dẫn `context`.
- **Dependencies:** `manage_story.py`, `scripts/style_analyzer.py`.
- **Integration:** Trực tiếp cung cấp bộ quy tắc cho `story-write` qua lệnh `context`.
- **Failure handling:** Báo lỗi nếu file rỗng, thư mục không có file hợp lệ; tự động fallback profile tên `default`.
- **Validation:** Bắt buộc profile phải có đủ 5 trục, có file JSON và Markdown riêng biệt.
- **Observed gaps:** Profile chỉ lưu cục bộ bên trong một truyện cụ thể (`stories/<id>/`), chưa có cơ chế chia sẻ profile dùng chung toàn cục giữa các truyện khác nhau.

### 4.4. Skill: `story-outline`
- **Slash command:** `/story-outline`.
- **File path:** `skills/story-outline/SKILL.md`.
- **Trigger:** `/story-outline`, "đề cương", "lên dàn ý", "gợi ý rẽ nhánh", "phục bút", "manh mối".
- **Scope:** Quản lý đề cương phân đoạn (`outline.md`), đề xuất 3 nhánh rẽ cốt truyện (Action / Emotion / Twist), quản lý danh sách phục bút (`foreshadow.json`).
- **Input:** Yêu cầu định hướng cốt truyện hoặc nội dung đề cương mới.
- **Output:** File `outline.md` và `foreshadow.json` được cập nhật qua annotation nháp hoặc hiển thị trên CLI.
- **Workflow:** Đọc `outline.md` -> Nếu bí ý thì đọc `references/plot-branching.md` đề xuất 3 nhánh A/B/C -> Tác giả duyệt -> Cập nhật đề cương hoặc ghi nhận phục bút vào `draft.md` rồi chạy `save`.
- **Dependencies:** `manage_story.py`, `references/plot-branching.md`.
- **Integration:** Cung cấp mục tiêu chương cho bước `context` của `story-write`.
- **Failure handling:** Thông báo nếu chưa có đề cương hoặc chưa có phục bút nào.
- **Validation:** Đối chiếu trạng thái "open" vs "resolved" của phục bút.
- **Observed gaps:** CLI chỉ hỗ trợ xem đề cương (`outline`) và xem phục bút (`foreshadow`), không có lệnh CLI trực tiếp để sửa đề cương hay giải quyết phục bút (bắt buộc phải ghi vào `draft.md`).

### 4.5. Skill: `story-deslop`
- **Slash command:** `/story-deslop`.
- **File path:** `skills/story-deslop/SKILL.md`.
- **Trigger:** `/story-deslop`, "khử văn mẫu", "khử AI", "tút lại văn", "chỉnh văn phong".
- **Scope:** Khử bỏ văn mẫu máy móc (AI-slop), loại bỏ từ ngữ sáo rỗng, áp dụng nguyên tắc Show Don't Tell và chiều sâu 5 giác quan.
- **Input:** Đoạn văn bản nghi ngờ có chất văn máy móc hoặc file `draft.md`.
- **Output:** Văn bản đã được viết lại tự nhiên, giàu chi tiết vật lý và cảm giác cơ thể.
- **Workflow:** Chạy `manage_story.py check` -> Tra cứu danh sách đen trong `references/anti-slop.md` -> Áp dụng kỹ thuật trong `references/show-dont-tell.md` -> Cắt gọt 20% từ ngữ giải thích trừu tượng.
- **Dependencies:** `manage_story.py`, `references/anti-slop.md`, `references/show-dont-tell.md`, `scripts/check-ai-patterns.js`.
- **Integration:** Hoạt động như trạm kiểm duyệt hỗ trợ cho bước 3 của `story-write`.
- **Failure handling:** Dựa vào mắt đọc và hướng dẫn thủ công của tác giả/AI.
- **Validation:** Tiêu chí 3/5 giác quan và không chứa cụm từ cấm kỵ.
- **Observed gaps:** Script `check-ai-patterns.js` bị crash vì thiếu module `style-whitelist.js`. Ngoài ra các pattern trong script là tiếng Trung, không quét được tiếng Việt.

### 4.6. Skill: `story-review`
- **Slash command:** `/story-review`.
- **File path:** `skills/story-review/SKILL.md`.
- **Trigger:** `/story-review`, "thẩm định", "soát lỗi", "review chương", "đánh giá chương".
- **Scope:** Đóng vai 3 độc giả phản biện độc lập (Logic & Lore, Pacing & Engagement, Character Voice & OOC) để rà soát chương trước khi lưu hoặc sau một Arc.
- **Input:** Nội dung chương cần thẩm định, đối chiếu với `character_bible.json`, `lorebook.json`, `outline.md`.
- **Output:** Báo cáo thẩm định gồm 3 phần: Điểm sáng, Lỗ hổng cần sửa (Crucial Fixes), Đánh giá chung (Đạt / Cần sửa).
- **Workflow:** Nhận chương -> Đọc hồ sơ nhân vật & lorebook -> Chạy qua 3 bộ câu hỏi kiểm tra -> Xuất báo cáo ngắn gọn.
- **Dependencies:** `character_bible.json`, `lorebook.json`, `foreshadow.json`.
- **Integration:** Phối hợp chặt chẽ trước khi chạy lệnh `save` trong `story-write`.
- **Failure handling:** Nếu thiếu file bối cảnh, cảnh báo và chỉ thẩm định dựa trên văn bản hiện có.
- **Validation:** Bắt buộc chỉ ra vị trí đoạn văn vi phạm thay vì nhận xét chung chung.
- **Observed gaps:** Chưa tích hợp thành lệnh tự động trong CLI, hoàn toàn là prompt instruction cho AI agent.

### 4.7. Skill: `story-cover`
- **Slash command:** `/story-cover`.
- **File path:** `skills/story-cover/SKILL.md`.
- **Trigger:** `/story-cover`, "tạo bìa", "làm bìa truyện", "thiết kế bìa", "vẽ bìa".
- **Scope:** Trích xuất metadata và không khí truyện để tạo prompt sinh ảnh bìa tiểu thuyết AI (Midjourney, DALL-E, SDXL, Imagen).
- **Input:** `story_config.json`, `character_bible.json`, `outline.md`.
- **Output:** Bộ prompt tiếng Anh chi tiết kèm tham số kỹ thuật (`--ar 2:3`, lighting, composition) và hướng dẫn bố cục typography.
- **Workflow:** Đọc config truyện -> Xác định thể loại, nhân vật tiêu điểm, tông màu -> Tạo prompt tiếng Anh chuẩn -> Gợi ý vị trí đặt tiêu đề và tên tác giả.
- **Dependencies:** `story_config.json`.
- **Integration:** Skill tiện ích độc lập, hỗ trợ hoàn thiện nhận diện tác phẩm.
- **Failure handling:** Báo lỗi nếu truyện chưa có metadata cơ bản.
- **Validation:** Kiểm tra có đầy đủ thông số tỷ lệ khung hình và bố cục chữ.
- **Observed gaps:** Chưa tích hợp trực tiếp API sinh ảnh (chỉ sinh prompt dạng text cho người dùng copy).

### 4.8. Skill: `story-import`
- **Slash command:** `/story-import`.
- **File path:** `skills/story-import/SKILL.md`.
- **Trigger:** `/story-import`, "nhập truyện", "import truyện", "phân tích truyện cũ".
- **Scope:** Nghịch đảo một file truyện cũ dài gồm nhiều chương thành cấu trúc dữ liệu đa tác phẩm chuẩn của StoryFlow.
- **Input:** File text/markdown truyện cũ nhiều chương hoặc nội dung dán trực tiếp.
- **Output:** Dự án mới tại `stories/<slug>/`, tách rời từng `chapter_XXXX.md`, khởi tạo `story.json`, `character_bible.json`, `rolling_summary.txt`.
- **Workflow:** Chạy `python manage_story.py init` -> Quét Regex nhận diện `Chương \d+` -> Tách file chương -> Cập nhật `story.json` -> Trích xuất nhân vật 5 chương đầu vào `character_bible.json`.
- **Dependencies:** `manage_story.py`.
- **Integration:** Là cầu nối đưa tác phẩm cũ vào luồng viết tiếp của `story-write`.
- **Failure handling:** Cảnh báo nếu không nhận diện được cấu trúc chương bằng Regex.
- **Validation:** Số lượng file chương sinh ra khớp với số lượng chương tìm thấy.
- **Observed gaps:** Toàn bộ logic Regex bóc tách chương và phân tích nhân vật hiện tại được quy định bằng văn bản hướng dẫn cho AI tự thực hiện, chưa được đóng gói thành một subcommand Python tự động (`python manage_story.py import --file <path>`).

### 4.9. Skill: `story-flow` (Legacy Monolith)
- **Slash command:** `/story-flow` (hoặc `/story-write`).
- **File path:** `skills/story-flow/SKILL.md`.
- **Trigger:** `/story-flow`, `/story-write`.
- **Scope:** Bản đặc tả kỹ thuật nguyên bản đầy đủ bao gồm cả quản lý dự án, quy trình viết 5 bước, đề cương, phục bút, kiểm tra chất lượng và tham chiếu CLI.
- **Input:** Tương tự `story-write`.
- **Output:** Tương tự `story-write`.
- **Workflow:** Trùng lặp hoàn toàn với quy trình trong `story-write`, `story-outline` và `story`.
- **Dependencies:** Toàn bộ hệ thống.
- **Integration:** Trùng lặp vai trò với `story-write`.
- **Failure handling:** Đầy đủ hướng dẫn xử lý lỗi annotation.
- **Validation:** Đối chiếu tương tự `story-write`.
- **Observed gaps:** 
  1. Trùng lặp trigger và nhiệm vụ với `story-write`.
  2. Dòng 128 đề cập đến `/story-scan` nhưng skill này không hề tồn tại trong repo.
  3. Dòng 124 nhắc đến các công thức thể loại "Huyền huyễn, Đô thị, Kinh dị..." nhưng trong `references/genre-styles/` chỉ có các file tiếng Trung với tên khác (`世情打脸.md`, `双男主.md`...).

---

## 5. BẢN ĐỒ CẤU TRÚC LỆNH VÀ SLASH COMMANDS

### 5.1. Ma trận đối chiếu Slash Commands vs CLI Commands vs Draft Annotations

| Slash Command | File Skill tương ứng | Lệnh CLI tương ứng trong manage_story.py | Cú pháp Annotation trong draft.md |
|---|---|---|---|
| `/story` | `skills/story/SKILL.md` | `stories`, `select`, `init`, `status`, `dashboard` | Không áp dụng |
| `/story-write` | `skills/story-write/SKILL.md` | `context`, `check`, `save` | `/story-title <Tên>` & `/story-brief <Tóm tắt>` (hoặc `/Title`, `/Brief`) |
| `/story-study` | `skills/story-study/SKILL.md` | `style --learn <p> [--profile <n>]`, `style --list`, `style --set <n>`, `style --show [n]` | `/story-study [--profile <tên>]` (dán văn bản bên dưới) |
| `/story-outline` | `skills/story-outline/SKILL.md` | `outline`, `foreshadow` | `/story-outline` (hoặc `/Outline [--append]`), `/story-foreshadow --clue "..." --chapter N` |
| `/story-deslop` | `skills/story-deslop/SKILL.md` | `check` | Không áp dụng trực tiếp |
| `/story-review` | `skills/story-review/SKILL.md` | Không có lệnh CLI tương ứng (hoàn toàn qua prompt) | Không áp dụng |
| `/story-cover` | `skills/story-cover/SKILL.md` | Không có lệnh CLI tương ứng (hoàn toàn qua prompt) | Không áp dụng |
| `/story-import` | `skills/story-import/SKILL.md` | `init` (chưa có subcommand `import`) | Không áp dụng |
| `/story-flow` | `skills/story-flow/SKILL.md` | Hợp nhất toàn bộ các lệnh CLI trên | Tương tự `/story-write` và `/story-outline` |

### 5.2. Sự chồng chéo và xung đột (Overlaps & Conflicts)
- **Xung đột `/story-flow` vs `/story-write`:** Cả hai skill đều khai báo trigger `/story-write` và `/story-flow` trong frontmatter YAML. Khi người dùng gõ `/story-write`, bộ định tuyến của Agent Harness có nguy cơ nạp cả hai file chỉ dẫn (tổng cộng hơn 11.200 bytes instruction), gây lãng phí context window và nguy cơ phân tán logic thực thi.
- **Phân tách trách nhiệm bị mờ nhạt:** `skills/story-flow/SKILL.md` đóng vai trò tài liệu "tất cả trong một", trong khi 8 skill còn lại được tách theo triết lý module hóa sâu (deep modules).

### 5.3. Các lệnh ma (Ghost Commands) phát hiện được
1. **Lệnh Slash Command ma: `/story-scan`**  
   - Xuất hiện tại: `skills/story-flow/SKILL.md` dòng 128 (`- /story-scan: Quét xu hướng và bảng xếp hạng truyện hot trên thị trường`).
   - Thực tế: Không tồn tại file `skills/story-scan/SKILL.md` hoặc bất kỳ script nào hỗ trợ tính năng này trong repository.
2. **Lệnh CLI ma: `append-summary`**  
   - Xuất hiện tại: `manage_story.py` dòng 365 (`python manage_story.py append-summary --from {lo} --to {hi} --text "..."`) và `skills/story-flow/SKILL.md` dòng 87.
   - Thực tế: Bộ phân tích tham số `argparse` trong `manage_story.py` (dòng 1005–1056) KHÔNG hề đăng ký subparser `append-summary`. Khi người dùng thực thi lệnh này, terminal báo lỗi:
     `manage_story.py: error: argument command: invalid choice: 'append-summary'`
     Lỗi này chặn đứng việc tóm tắt mốc qua CLI, buộc người dùng phải biết dùng annotation `/Summary` trong nháp.

---

## 6. KIẾN TRÚC CLI VÀ LOGIC ĐIỀU PHỐI CỦA MANAGE_STORY.PY

### 6.1. Cấu trúc tổng thể
`manage_story.py` (1.077 dòng code) được viết bằng Python thuần, sử dụng thư viện tiêu chuẩn (`os`, `json`, `argparse`, `sys`, `io`, `shutil`, `re`, `unicodedata`, `datetime`).

### 6.2. Cơ chế phân phối lệnh (Dispatch Mechanism)
Lệnh được phân phối qua dictionary `dispatch` ở dòng 1059:
```python
dispatch = {
    'init': action_init,
    'select': action_select,
    'stories': action_stories,
    'save': action_save,
    'context': action_context,
    'outline': action_outline,
    'foreshadow': action_foreshadow,
    'list': action_list,
    'status': action_status,
    'check': action_check,
    'dashboard': action_dashboard,
    'style': action_style,
}
```

### 6.3. Phân tích luồng Annotation Routing trong `action_save` (Dòng 500–656)
Hàm `action_save` đọc toàn văn file `draft.md` và dựa vào biểu thức chính quy ở dòng đầu tiên để phân luồng xử lý:
1. `lines[0].startswith('/Summary')` hoặc `/story-summary`: Ghi nối vào `rolling_summary.txt`.
2. `lines[0].startswith('/Lore')` hoặc `/story-lore`: Cập nhật `lorebook.json`.
3. `lines[0].startswith('/Character')` hoặc `/story-character`: Cập nhật `character_bible.json`.
4. `lines[0].startswith('/Outline')` hoặc `/story-outline`: Cập nhật `outline.md`.
5. `lines[0].startswith('/Foreshadow')` hoặc `/story-foreshadow`: Cập nhật `foreshadow.json`.
6. `lines[0].startswith('/story-study')` hoặc `/study`: Gọi `scripts/style_analyzer.py` phân tích văn phong.
7. `lines[0].startswith('/Title')` hoặc `/story-title`: Lưu thành chương mới `chapter_XXXX.md`.

### 6.4. Các lỗi logic và điểm nghẽn trong `action_save`
1. **Lỗi sụp đổ do dòng trống đầu file (Leading Newline Trap):**  
   Tại dòng 515-516:
   ```python
   lines = content.split('\n')
   first_line = lines[0].strip()
   ```
   Nếu người dùng hoặc AI vô tình chèn một dòng trống ở đầu file `draft.md`, `lines[0].strip()` sẽ trả về chuỗi rỗng `""`. Khi đó, toàn bộ 7 nhánh kiểm tra `startswith` đều thất bại, code nhảy vào nhánh `else:` và báo lỗi `[ERROR] Nháp chưa có Annotation hợp lệ ở dòng đầu`, từ chối lưu file dù các dòng tiếp theo có annotation hợp lệ.
2. **Giới hạn đơn tác vụ (Single-operation Lockout):**  
   Mỗi lần chạy `save`, hàm xử lý ngay lập tức ghi đè reset file `draft.md` về nội dung `"Viết chương mới tại đây..."` và kết thúc (`return`). Người dùng không thể vừa lưu chương mới vừa cập nhật trạng thái nhân vật hay bối cảnh trong cùng một lần lưu.
3. **Thứ tự kiểm tra tham số cứng nhắc trong soạn chương:**  
   Dòng 619-626 kiểm tra tuần tự: Dòng 2 bắt buộc phải là `/Brief` hoặc `/story-brief`, sau đó mới đến dòng tiếp theo là `/Force`. Nếu người dùng đảo thứ tự (`/Force` ở dòng 2 và `/Brief` ở dòng 3), tham số `/Brief` sẽ bị coi là một phần nội dung chương truyện.

### 6.5. Xử lý lỗi trong `action_check` (Dòng 829–870) — LỖI PHÊ DUYỆT GIẢ MẠO (FALSE POSITIVE GATE)
Tại dòng 848–868:
```python
res = subprocess.run(['node', pat_script, draft_file], capture_output=True, text=True, encoding='utf-8')
if res.stdout.strip():
    print(f"  {res.stdout.strip()}")
else:
    print("  ✓ Không phát hiện văn mẫu AI nghiêm trọng.")
```
- Khi script Node.js gặp lỗi cú pháp, crash, hoặc thiếu module dependency (`MODULE_NOT_FOUND`), Node.js in thông báo lỗi ra **`stderr`** và trả về exit code khác 0.
- `manage_story.py` hoàn toàn **không kiểm tra `res.returncode` và không đọc `res.stderr`**.
- Do `res.stdout` lúc crash là rỗng, chương trình nhảy vào nhánh `else:` và in ra màn hình:
  `✓ Không phát hiện văn mẫu AI nghiêm trọng.`
- **Hậu quả:** Bộ kiểm soát chất lượng bị vô hiệu hóa hoàn toàn trong thực tế nhưng vẫn thông báo thành công cho AI và tác giả.

---

## 7. LUỒNG DỮ LIỆU, LIFECYCLE VÀ CẤU TRÚC THƯ MỤC STORIES

### 7.1. Cấu trúc thư mục tác phẩm chuẩn
Khi một tác phẩm được tạo bằng `python manage_story.py init --title "Tên" --id "slug"`:
```text
stories/<slug>/
├── story_config.json          # Metadata cơ bản (tiêu đề, tác giả, thể loại, số chương hiện tại)
├── story.json                 # Index toàn bộ các chương, đường dẫn file và tóm tắt ngắn (brief)
├── chapters/
│   ├── draft.md               # File nháp tương tác đa năng giữa Tác giả và AI
│   └── chapter_XXXX.md        # Các chương chính thức đã được lưu (đánh số 4 chữ số: 0001, 0002...)
└── summaries/
    ├── rolling_summary.txt    # Tóm tắt tích lũy cuốn chiếu theo từng khối 10 chương
    ├── outline.md             # Đề cương mục tiêu Arc và các chương tiếp theo
    ├── foreshadow.json        # Sổ theo dõi manh mối / phục bút (open / resolved)
    ├── character_bible.json   # Hồ sơ nhân vật và lịch sử cập nhật theo chương
    ├── lorebook.json          # Bối cảnh thế giới, thế lực, địa danh, quy tắc tu luyện
    ├── active_style_profile.json # Lưu profile văn phong đang hoạt động
    └── style_profiles/        # Thư mục lưu các Style Profiles độc lập
        └── <profile_name>/
            ├── style_profile.json  # Dữ liệu phân tích 5 trục (máy đọc)
            └── STYLE_PROFILE.md   # Bộ quy tắc sáng tác & chỉ dẫn thực thi (người & AI đọc)
```

### 7.2. Quản lý trạng thái đa tác phẩm (Multi-Story State)
- Trạng thái truyện đang hoạt động được lưu tại file duy nhất: `active_story.json` ở thư mục gốc của repository (nội dung: `{"active_story": "<slug>"}`).
- Tệp này được cấu hình bỏ qua trong `.gitignore` để tránh xung đột môi trường cá nhân khi commit lên Git.
- **Rủi ro:** Nếu file `active_story.json` bị mất hoặc chưa được tạo, tất cả các lệnh thao tác (`context`, `save`, `check`, `style`, `outline`, `foreshadow`) đều dừng lại và báo lỗi yêu cầu chạy `select` hoặc `init`.

### 7.3. Vòng đời dữ liệu của một chương truyện (Chapter Lifecycle)
1. **Khởi động ngữ cảnh (`context`):**
   - Đọc `rolling_summary.txt` (từ chương 1 đến mốc bội số 10 gần nhất: $M = \lfloor N/10 \rfloor \times 10$).
   - Đọc các dòng brief tóm tắt của các chương lẻ từ $M+1$ đến $N-1$ trong `story.json`.
   - Đọc toàn văn duy nhất chương $N$ liền kề để bắt nhịp hành văn.
   - Đọc mục tiêu đề cương chương $N+1$ từ `outline.md`.
   - Đọc các phục bút đang chờ từ `foreshadow.json`.
   - Đọc chỉ dẫn nhanh 3 dòng của Style Profile đang active.
2. **Soạn thảo (`drafting`):**
   - AI/Tác giả viết vào `draft.md`. Bắt buộc khai báo `/story-title` và `/story-brief`.
3. **Kiểm tra chất lượng (`check`):**
   - Chạy script chuẩn hóa và quét lỗi văn mẫu.
4. **Lưu trữ (`save`):**
   - `draft.md` được đọc và ghi ra `chapter_{N+1:04d}.md`.
   - Cập nhật số chương trong `story_config.json`.
   - Cập nhật index chương và brief vào `story.json`.
   - File `draft.md` được reset về trắng.
   - Nếu $N+1$ chia hết cho 10: In thông báo cảnh báo cột mốc cần tóm tắt cuốn chiếu.

---

## 8. PHÂN TÍCH STYLE ENGINE VÀ TÍNH NĂNG HỌC VĂN PHONG

Tính năng Style Engine được bổ sung tại commit `622e324` nhằm thực thi yêu cầu bóc tách 5 trục và pipeline tuân thủ văn phong.

### 8.1. Đánh giá kỹ thuật module `scripts/style_analyzer.py`
Module triển khai hàm `analyze_texts(sources, text_list, profile_id)` thực hiện trích xuất 5 trục:
1. **Trục 1: Cấu trúc & Nhịp câu (Syntax & Rhythm):**
   - Tách câu dựa trên Regex nhìn sau dấu ngắt: `re.split(r'(?<=[.!?…])\s+', clean)`.
   - Phân loại 3 mức độ dài: Ngắn (< 10 từ), Vừa (10–22 từ), Dài (> 22 từ).
   - Thống kê tần suất dấu chấm lửng (`...`, `…`), gạch ngang (`—`), chấm than (`!`), hỏi chấm (`?`).
2. **Trục 2: Mật độ giác quan (Sensory Immersion):**
   - Tra cứu từ điển đối chiếu tĩnh `SENSORY_LEXICON` chia làm 4 nhóm: Thị giác (`visual`), Thính giác (`auditory`), Xúc giác & Cơ thể (`tactile_visceral`), Khứu & Vị giác (`olfactory_gustatory`).
   - Tính toán mật độ xuất hiện trên 1.000 từ và xác định giác quan chủ đạo.
3. **Trục 3: Tỷ lệ phân bổ nội dung (Content Distribution):**
   - Quét hội thoại qua dấu ngoặc kép (`"..."`, `“...”`, `「...」`) và gạch đầu dòng (`^[—–-]\s*`).
   - Ước lượng độc thoại nội tâm qua từ khóa chỉ thị (`nghĩ thầm`, `thầm nhủ`, `trong lòng`...).
   - Tính toán tỷ lệ phần trăm giữa Hội thoại vs Tự sự/Hành động vs Độc thoại nội tâm.
4. **Trục 4: Khẩu khí & Tông giọng (Tone & Voice):**
   - Phân loại qua heuristic dựa trên nhịp câu và mật độ cảm thán: Dồn dập căng thẳng, Trầm tĩnh chậm rãi, Kịch tính hóa cao, hoặc Cân bằng khách quan.
5. **Trục 5: Từ vựng & Biện pháp tu từ (Rhetoric & Lexicon):**
   - Đo mật độ từ khóa so sánh (`như`, `tựa như`, `ngỡ như`...).
   - Nhận diện từ láy tiếng Việt: Dựa trên lặp phụ âm đầu giữa 2 từ liên tiếp kết hợp danh sách từ mồi.

### 8.2. Các điểm hạn chế và nợ kỹ thuật của Style Analyzer
1. **Tokenization tiếng Việt thô sơ:**
   Hàm `tokenize_words` tách từ qua khoảng trắng (`\s+`). Trong tiếng Việt, đơn vị có nghĩa là từ ghép (2–3 âm tiết như "thời gian", "lung linh", "bất ngờ"). Việc tách theo khoảng trắng thực chất chỉ đếm số lượng âm tiết (syllables), dẫn đến việc tính toán độ dài câu theo từ bị lệch so với ngữ pháp thực tế.
2. **Regex hội thoại không hỗ trợ xuống dòng:**
   `re.findall(r'["“「](.*?)["”」]', full_text)` thiếu cờ `re.DOTALL`. Nếu đoạn thoại của nhân vật kéo dài qua nhiều đoạn văn có ngắt dòng, Regex sẽ bỏ sót toàn bộ đoạn thoại này.
3. **Nhận diện từ láy quá hạn hẹp:**
   Dòng 149 của `style_analyzer.py` chỉ kiểm tra 10 từ mồi cố định (`['róc', 'lung', 'thì', 'thoang', 'lập', 'chầm', 'lặng', 'run', 'hun', 'vồn']`). Hàng ngàn từ láy giàu sức gợi của tiếng Việt ("thao thức", "dồn dập", "le lói", "chập chờn", "hun hút", "loang lổ") đều bị bỏ qua.
4. **Cô lập cục bộ của Profile:**
   Hồ sơ văn phong được lưu cứng tại `stories/<id>/summaries/style_profiles/`. Khi người dùng tạo một tác phẩm mới (`init`), họ buộc phải chạy lại phân tích từ đầu hoặc sao chép thủ công file profile giữa các thư mục, do thiếu một thư mục hồ sơ văn phong dùng chung cấp hệ thống (`global_style_profiles/`).

---

## 9. KHẢO SÁT REFERENCES, TEMPLATES, SCRIPTS VÀ ASSETS

### 9.1. Khảo sát thư mục `references/`
- **Các tài liệu chất lượng cao (Đã chuẩn hóa tiếng Việt):**
  - `references/anti-slop.md` (1.483 bytes): Tốt, danh sách đen từ ngữ dịch thô tiếng Trung và công thức cắt gọt 20%.
  - `references/plot-branching.md` (1.811 bytes): Rất tốt, chuẩn hóa 3 nhánh đề xuất Action / Emotion / Twist.
  - `references/show-dont-tell.md` (2.056 bytes): Rất tốt, hướng dẫn chi tiết về phản ứng cơ thể và kích hoạt 5 giác quan.
- **Thư mục phong cách thể loại `references/genre-styles/` (10 files):**
  - Toàn bộ 10 file (`世情打脸.md`, `双男主.md`, `复仇打脸.md`, `宅斗宫斗.md`, `总裁豪门.md`, `悬疑.md`, `民俗怪谈.md`, `沙雕脑洞.md`, `甜宠.md`, `追妻火葬场.md`) được sao chép trực tiếp từ kho mã `.agents` của Trung Quốc.
  - **Tên file chứa ký tự tiếng Trung Unicode:** Gây khó khăn khi tham chiếu đường dẫn trên một số shell Windows không hỗ trợ UTF-8 đầy đủ.
  - **Nội dung 100% bằng tiếng Trung giản thể:** Dẫn dắt theo thuật ngữ của các mạng văn học mạng Trung Quốc (Phan Cà Chua - 番茄, Thất Miêu - 七猫, Hắc Nham - 黑岩).
  - **Chưa được Việt hóa và thích ứng:** Các quy tắc này chưa được chuyển dịch thành thuật ngữ sáng tác tiếng Việt và chưa có sự tương thích với phong cách tiểu thuyết mạng tại Việt Nam.

### 9.2. Khảo sát thư mục `scripts/`
- `scripts/style_analyzer.py`: Hoạt động ổn định, không phụ thuộc thư viện ngoài.
- `scripts/check-ai-patterns.js`:
  - **CRITICAL BUG:** Dòng 5 gọi `const { loadStyleWhitelist, maskStyleText } = require('./style-whitelist.js');`. File `style-whitelist.js` **KHÔNG TỒN TẠI** trong thư mục `scripts/`.
  - Toàn bộ 1.586 dòng code chứa các regex phát hiện mẫu câu tiếng Trung (`了下/了一下`, `指尖/指节`, `这一刻终于明白`). Hoàn toàn không có tác dụng kiểm tra ngữ văn tiếng Việt.
- `scripts/normalize-punctuation.js`:
  - **CRITICAL BUG:** Dòng 5 cũng gọi `require('./style-whitelist.js')` và bị crash tương tự.
  - Tập trung xử lý dấu ngoặc kép Trung Quốc (`“”`, `「」`) và dấu chấm lửng 6 chấm của tiếng Trung.
- `scripts/dashboard-server.mjs`:
  - Dòng 25–27: Hardcode quét các thư mục tên tiếng Trung (`正文`, `大纲`, `设定`, `追踪`) và file `正文.md`.
  - Không quét cấu trúc `stories/<id>/chapters/` và `summaries/` của StoryFlow.
  - Kết quả: Khi khởi chạy Dashboard bằng `python manage_story.py dashboard`, server mở giao diện nhưng báo 0 dự án và 0 văn bản.

### 9.3. Khảo sát thư mục `assets/` (Web Dashboard)
- `assets/index.html`: Giao diện mang thương hiệu "OH STORY 本地写作工作台" bằng tiếng Trung. Các nhãn điều hướng: "跳到文稿台", "拆文库", "正在辨认书架...".
- `assets/app.js`: Tương thích với API của server tiếng Trung, chưa được quốc tế hóa hoặc bản địa hóa sang tiếng Việt.

---

## 10. HIỆN TRẠNG KIỂM THỬ, FIXTURES VÀ TÀI LIỆU

### 10.1. Tình trạng kiểm thử tự động (Automated Tests)
- **Kết quả kiểm toán:** `NOT FOUND` (Không tồn tại).
- Không có thư mục `tests/` trong repository.
- Không có bất kỳ test script nào (pytest, unittest, jest, vitest) cho `manage_story.py`, `style_analyzer.py` hay các lệnh CLI.
- Mọi hoạt động kiểm tra từ trước đến nay đều được thực hiện thủ công thông qua gõ lệnh ad-hoc.

### 10.2. Tình trạng Fixtures và Dữ liệu mẫu (Samples)
- **Kết quả kiểm toán:** `NOT FOUND` (Không tồn tại).
- Thư mục `stories/` hoàn toàn trống (chỉ có file rỗng `.gitkeep`).
- Không có thư mục `samples/` chứa các đoạn văn mẫu để kiểm tra tính năng `style --learn`.
- Thiếu các file fixture chuẩn để kiểm tra tính toàn vẹn của việc bóc tách chương trong `story-import`.

### 10.3. Hiện trạng tài liệu (Documentation)
- File `README.md` tồn tại nhưng phản ánh sai cấu trúc thực tế:
  - Dòng 42 mô tả file `SKILL.md` nằm ở thư mục gốc (thực tế đã bị xóa từ commit `64d35bd` để phục vụ `npx skills add`).
  - Dòng 45–47 mô tả thư mục `skills/` chỉ chứa `skills/story-flow/SKILL.md` (thực tế thư mục này chứa 9 skill con độc lập).
  - Thiếu tài liệu đặc tả API nội bộ và bảng mã lỗi CLI.

---

## 11. BẢNG ĐỐI CHIẾU HIỆN TRẠNG VÀ MỤC TIÊU NÂNG CẤP

| Tiêu chí / Mục tiêu | Trạng thái hiện tại | Mức độ hoàn thiện (%) | Đánh giá kỹ thuật |
|---|---|---|---|
| **Bộ 9 Skills con chuẩn npx** | Đủ 9 file trong `skills/` | 90% | Hoàn chỉnh về mặt instruction, nhưng có sự trùng lặp giữa `story-flow` và `story-write`. |
| **Trạm Router `/story`** | Hoạt động tốt | 85% | Bảng điều hướng rõ ràng, cần cập nhật thêm các lệnh CLI còn thiếu. |
| **Quy trình viết `/story-write`** | Hoạt động qua CLI | 70% | Bị ảnh hưởng bởi lỗ hổng nuốt lỗi của `action_check` và hạn chế dòng trống trong `draft.md`. |
| **Học văn phong `/story-study`** | Hoạt động tốt qua Python | 75% | Bóc tách 5 trục và sinh Markdown chuẩn; hạn chế về từ điển từ láy và thiếu profile global. |
| **Đề cương thích ứng `/story-outline`** | Hoàn thành tốt | 80% | Hướng dẫn 3 nhánh rẽ rất sắc sảo; CLI thiếu lệnh chỉnh sửa trực tiếp. |
| **Khử văn mẫu AI `/story-deslop`** | Hỏng một phần | 40% | Hướng dẫn lý thuyết rất tốt, nhưng script kỹ thuật bị crash do thiếu `style-whitelist.js`. |
| **Thẩm định phản biện `/story-review`** | Hoàn thành lý thuyết | 70% | Bộ rubric 3 vai rõ ràng; chưa có script tự động hỗ trợ. |
| **Tạo prompt bìa `/story-cover`** | Hoàn thành lý thuyết | 80% | Prompt tiếng Anh chi tiết, đúng tỷ lệ chuẩn tiểu thuyết. |
| **Nhập truyện cũ `/story-import`** | Hoàn thành lý thuyết | 50% | Chưa có subcommand CLI tự động hóa bằng Python, còn phụ thuộc vào AI đọc thủ công. |
| **Web Dashboard** | Hỏng về mặt tích hợp | 25% | Server và Asset chạy được nhưng tìm sai cấu trúc thư mục và toàn bộ bằng tiếng Trung. |
| **Kiểm thử tự động & CI** | Hoàn toàn chưa có | 0% | Chưa có bất kỳ test suite nào. |

---

## 12. PHÂN TÍCH RỦI RO KỸ THUẬT

### 12.1. Rủi ro mức độ Nghiêm trọng (Critical)
1. **Rủi ro phê duyệt chất lượng giả tạo (Silent Gate Failure):**  
   Script `check-ai-patterns.js` và `normalize-punctuation.js` crash 100% khi chạy qua `python manage_story.py check` nhưng màn hình vẫn báo thành công. Tác giả và AI tin rằng bản nháp đã sạch slop trong khi không có bất kỳ bộ lọc nào thực sự chạy.
2. **Rủi ro mất dữ liệu hoặc từ chối ghi nháp (Draft Save Rejection):**  
   Nếu file `draft.md` có bất kỳ dòng trắng nào ở dòng 1, toàn bộ nội dung chương vừa viết sẽ không thể lưu được và có nguy cơ bị ghi đè nếu tác giả thao tác nhầm.

### 12.2. Rủi ro mức độ Cao (High)
3. **Rủi ro Dashboard không thể sử dụng:**  
   Dashboard là tính năng trực quan quan trọng nhất để người dùng theo dõi cây truyện, nhưng hiện tại hoàn toàn không nhận diện được các tác phẩm trong thư mục `stories/`.
4. **Rủi ro xung đột bộ nạp Skill (Instruction Confusion):**  
   Sự hiện diện song song của `story-flow` và `story-write` với cùng trigger `/story-write` khiến Agent Harness nạp thừa thông tin, có thể dẫn đến việc thực thi không nhất quán giữa hướng dẫn mới và hướng dẫn cũ.

### 12.3. Rủi ro mức độ Trung bình (Medium)
5. **Rào cản ngôn ngữ và tài sản không đồng nhất trong `references/genre-styles/`:**  
   10 file tiếng Trung trong `genre-styles` tạo cảm giác một dự án chắp vá, chưa hoàn thiện bản địa hóa, và AI có thể đọc nhầm tài liệu tiếng Trung khi viết truyện tiếng Việt.
6. **Lỗi lệnh CLI không tồn tại (`append-summary`):**  
   Gây ức chế trải nghiệm người dùng khi hệ thống tự đề xuất một lệnh mà chính CLI lại từ chối thực thi.

---

## 13. NHỮNG GIẢ ĐỊNH CẦN NGƯỜI DÙNG XÁC NHẬN

1. **Giả định về vai trò của Skill `story-flow`:**  
   *Giả định:* `story-flow` là skill ban đầu (monolith) trước khi tách ra 8 skill con. Khi đã có `story-write` và `story`, có nên chuyển `story-flow` thành alias trỏ về `story-write` hoặc tái định nghĩa nó thành Skill thực thi tự động toàn trình (Autonomous Full-Flow)?
2. **Giả định về bộ công cụ JavaScript từ `.agents`:**  
   *Giả định:* Việc sử dụng Node.js để chạy `check-ai-patterns.js` và `normalize-punctuation.js` gây phụ thuộc 2 runtime (Python + Node.js). Có nên chuyển toàn bộ logic khử slop và chuẩn hóa dấu câu tiếng Việt sang Python thuần bên trong `scripts/` hoặc `manage_story.py` để chỉ cần duy nhất môi trường Python?
3. **Giả định về thư mục tài liệu thể loại tiếng Trung (`references/genre-styles/`):**  
   *Giả định:* Người dùng có nhu cầu viết các thể loại văn học mạng đặc thù Trung Quốc (Hào môn, Cung đấu, Vả mặt, Truy thê) nhưng cần phiên bản dịch nghĩa và chuyển thể hoàn toàn sang tiếng Việt, hay muốn thay thế bằng các thể loại phổ biến tại Việt Nam (Tiên hiệp, Kiếm hiệp, Đô thị, Trinh thám, Lịch sử)?
4. **Giả định về kho Style Profile dùng chung:**  
   *Giả định:* Cần có một thư mục `profiles/` toàn cục ở cấp repository để khi học văn phong từ một tác giả (ví dụ: Kim Dung, Nam Cao), profile đó có thể áp dụng ngay cho nhiều tác phẩm khác nhau mà không cần phân tích lại.

---

## 14. THÔNG TIN VÀ TÀI LIỆU CÒN THIẾU

1. **File `style-whitelist.js`:** Module bị thiếu khiến các script Node.js hiện tại không thể chạy.
2. **Tập mẫu kiểm thử (Sample Benchmark Datasets):** Cần ít nhất 2–3 trích đoạn truyện mẫu bằng tiếng Việt (ngắn, vừa, dài) để làm fixture kiểm tra tự động cho `style_analyzer.py`.
3. **Bộ từ điển tiếng Việt chuẩn cho phân tích văn phong:** Thiếu danh sách từ láy tiếng Việt đầy đủ và từ điển cảm giác cơ thể / biểu hiện cảm xúc tiếng Việt chuyên sâu.
4. **Tài liệu đặc tả kiến trúc chuyển đổi (Migration Architecture Spec):** Hướng dẫn cấu trúc cho Dashboard tương thích hoàn toàn với StoryFlow.

---

## 15. DANH MỤC CÁC ĐIỂM BẤT NHẤT VÀ NỢ KỸ THUẬT

| Mã nợ | Vị trí phát hiện | Loại nợ kỹ thuật | Mô tả chi tiết | Mức độ nghiêm trọng |
|---|---|---|---|---|
| **TD-01** | `scripts/check-ai-patterns.js:5` | Dependency Missing | Thiếu file `style-whitelist.js`, gây crash Node.js runtime khi gọi `manage_story.py check`. | CRITICAL |
| **TD-02** | `scripts/normalize-punctuation.js:5` | Dependency Missing | Thiếu file `style-whitelist.js`, gây crash Node.js runtime khi gọi `manage_story.py check`. | CRITICAL |
| **TD-03** | `manage_story.py:848-868` | Silent Error Swallowing | Nuốt lỗi `stderr` và `returncode` của subprocess, thông báo đỗ kiểm tra dù script bị crash. | CRITICAL |
| **TD-04** | `manage_story.py:515-516` | Robustness Flaw | Dòng trống đầu tiên trong `draft.md` làm vô hiệu hóa toàn bộ cơ chế Annotation Routing. | HIGH |
| **TD-05** | `scripts/dashboard-server.mjs:25-27` | Structural Incompatibility | Server chỉ quét thư mục tên tiếng Trung (`正文`, `大纲`), không quét `stories/<id>/chapters/`. | HIGH |
| **TD-06** | `assets/index.html` & `app.js` | Localization Missing | Giao diện Web Dashboard hiển thị hoàn toàn bằng tiếng Trung ("OH STORY 写作台"). | HIGH |
| **TD-07** | `skills/story-flow` vs `story-write` | Instruction Overlap | Hai skill tranh chấp cùng trigger `/story-write` và `/story-flow`, trùng lặp 80% nội dung. | HIGH |
| **TD-08** | `manage_story.py:365` | Ghost CLI Command | In thông báo bảo người dùng chạy `append-summary` nhưng lệnh này không tồn tại trong `argparse`. | MEDIUM |
| **TD-09** | `skills/story-flow/SKILL.md:128` | Ghost Slash Command | Liệt kê slash command `/story-scan` nhưng không có skill tương ứng trong hệ thống. | MEDIUM |
| **TD-10** | `references/genre-styles/*` | Non-ASCII & Foreign Lang | 10 file tên tiếng Trung và nội dung tiếng Trung, chưa được chuyển thể sang tiếng Việt. | MEDIUM |
| **TD-11** | `README.md:42, 46-47` | Stale Documentation | Diagram kiến trúc trong README vẫn vẽ file `SKILL.md` ở gốc và chỉ có 1 skill con trong `skills/`. | MEDIUM |
| **TD-12** | `scripts/style_analyzer.py:149` | Inadequate Heuristic | Từ điển từ láy chỉ có 10 từ mồi tĩnh, bỏ sót phần lớn từ láy tiếng Việt. | LOW |
| **TD-13** | Toàn bộ repository | Missing Test Suite | Không có bất kỳ unit test hoặc integration test nào. | HIGH |

---

## 16. CÁC CÂU HỎI KIẾN TRÚC CHƯA THỂ TỰ QUYẾT ĐỊNH

Các vấn đề sau đây đòi hỏi sự định hướng và quyết định chiến lược từ phía Người dùng / Tác giả trước khi tiến hành nâng cấp:

1. **Định hướng môi trường thực thi của StoryFlow (Single Runtime vs Dual Runtime):**
   - *Phương án A (Python Pure - Khuyến nghị):* Viết lại toàn bộ tính năng kiểm tra dấu câu, lọc slop và server dashboard sang Python thuần. Dự án sẽ chỉ phụ thuộc duy nhất vào Python 3 (không cần cài Node.js).
   - *Phương án B (Dual Runtime Python + Node.js):* Giữ nguyên kiến trúc lai, bổ sung `style-whitelist.js`, Việt hóa script Node.js và nâng cấp `dashboard-server.mjs`.
2. **Số phận của Skill `story-flow`:**
   - *Phương án A:* Giữ `story-flow` làm Skill toàn trình hợp nhất cho các Agent tự hành cấp cao (Autonomous Runner), trong khi `story-write` dành cho tác giả tương tác từng bước (Interactive). Tách biệt rõ trigger: `/story-flow` cho tự hành, `/story-write` cho tương tác.
   - *Phương án B:* Hợp nhất hoặc loại bỏ `story-flow` để tránh trùng lặp, chỉ giữ duy nhất bộ 8 skill chuyên biệt.
3. **Xử lý thư mục 10 thể loại tiếng Trung (`references/genre-styles/`):**
   - *Phương án A:* Dịch thuật và chuyển thể toàn bộ 10 file sang tiếng Việt, đổi tên file thành tiếng Việt không dấu hoặc tiếng Anh (ví dụ: `the-tinh-va-mat.md`, `tong-tai-hao-mon.md`).
   - *Phương án B:* Biên soạn lại bộ công thức thể loại mới hoàn toàn theo cấu trúc tiểu thuyết phổ biến tại Việt Nam (Tiên hiệp/Tu chân, Đô thị/Dị năng, Huyền huyễn, Trinh thám/Kinh dị, Dã sử/Xuyên không).
4. **Phạm vi lưu trữ Style Profiles (Cục bộ vs Toàn cục):**
   - *Phương án A:* Chỉ lưu trong từng truyện (`stories/<id>/summaries/style_profiles/`).
   - *Phương án B (Khuyến nghị):* Thiết kế kho lưu trữ 2 cấp: Cấp hệ thống (`style_library/<profile>/`) để dùng chung cho mọi truyện, và Cấp tác phẩm (`stories/<id>/...`) để override tùy biến riêng.

---

## 17. KHUYẾN NGHỊ CHUẨN BỊ CHO GIAI ĐOẠN LẬP PHƯƠNG ÁN

Dựa trên các phát hiện kiểm toán, lộ trình nâng cấp nên được chia thành 4 bước tuần tự sau khi người dùng phê duyệt định hướng:

1. **Giai đoạn 1: Vá lỗi khẩn cấp và bảo vệ dữ liệu (P0 - Immediate Fixes)**
   - Sửa hàm `action_check` trong `manage_story.py` để bắt lỗi exit code và hiển thị `stderr` từ subprocess (chấm dứt tình trạng báo đỗ giả mạo).
   - Khôi phục file `style-whitelist.js` hoặc thay thế bằng cơ chế kiểm tra slop trực tiếp.
   - Nâng cấp `action_save` để loại bỏ lỗi dòng trống đầu file `draft.md`.
   - Bổ sung subcommand CLI `append-summary` vào `manage_story.py`.
2. **Giai đoạn 2: Chuẩn hóa bộ Skill và Instruction Hierarchy (P1)**
   - Tách biệt dứt điểm trigger giữa `story-flow` và `story-write`.
   - Dọn dẹp các lệnh ma (`/story-scan`).
   - Cập nhật sơ đồ hệ thống trong `README.md` khớp 100% với thực tế 9 skills trong `skills/`.
3. **Giai đoạn 3: Nâng cấp Style Engine & Bản địa hóa (P1)**
   - Mở rộng thuật toán bóc tách từ láy tiếng Việt và hoàn thiện bóc tách hội thoại đa dòng trong `scripts/style_analyzer.py`.
   - Chuyển thể và đổi tên 10 file phong cách thể loại trong `references/genre-styles/` sang tiếng Việt chuẩn.
   - Thiết lập kho lưu trữ Style Profiles toàn cục (Global Style Library).
4. **Giai đoạn 4: Cải tạo Dashboard & Thiết lập Test Suite (P2)**
   - Cập nhật logic quét thư mục của `dashboard-server.mjs` để nhận diện cấu trúc `stories/<story_id>/`.
   - Việt hóa toàn bộ giao diện `assets/index.html` và `assets/app.js`.
   - Viết bộ kiểm thử tự động `tests/test_manage_story.py` và `tests/test_style_analyzer.py` để đảm bảo độ tin cậy lâu dài.

---

## 18. NHẬT KÝ BẰNG CHỨNG VÀ TÀI LIỆU THAM KHẢO

1. **Bằng chứng Git Commit:**
   - `622e324` (2026-10-21): Thêm `story-study` skill và `style_analyzer.py`.
   - `64d35bd` (2026-10-21): Gỡ bỏ root `SKILL.md` để hỗ trợ `npx skills add`.
2. **Bằng chứng kiểm tra lỗi thực thi lệnh (Execution Logs):**
   - Kiểm tra `node scripts/check-ai-patterns.js`:
     `Error: Cannot find module './style-whitelist.js'` (Exit code: 1).
   - Kiểm tra `node scripts/normalize-punctuation.js`:
     `Error: Cannot find module './style-whitelist.js'` (Exit code: 1).
   - Kiểm tra `python manage_story.py append-summary`:
     `manage_story.py: error: argument command: invalid choice: 'append-summary'` (Exit code: 2).
3. **Bằng chứng quét tệp:**
   - Toàn bộ 34 tệp đã được kiểm kê chi tiết mã hash và dung lượng trong working tree.
   - Không có file nào ngoài báo cáo này bị tạo mới hoặc sửa đổi.

---
*Báo cáo kiểm toán được lập hoàn tất và lưu trữ tại `SKILLS_UPGRADE_AUDIT.md`.*
