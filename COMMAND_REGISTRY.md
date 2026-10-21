# BẢNG ĐĂNG KÝ LỆNH THỰC THI (COMMAND REGISTRY)

Tài liệu này ghi nhận đầy đủ và chính xác toàn bộ các câu lệnh thực thi có thật trong hệ thống StoryFlow. Không có bất kỳ câu lệnh giả tưởng (ghost commands) nào được liệt kê tại đây.

---

## 1. NHÓM LỆNH QUẢN TRỊ DỰ ÁN & TÁC PHẨM (PROJECT LIFECYCLE)

### `python manage_story.py init`
- **Mục đích:** Khởi tạo cấu trúc dữ liệu cho một tác phẩm mới trong hệ thống đa tác phẩm.
- **Đầu vào (Arguments):**
  - `--title <str>` *(Bắt buộc)*: Tên tác phẩm.
  - `--author <str>` *(Tùy chọn, mặc định: "Vô danh")*: Bút danh tác giả.
  - `--genre <str>` *(Tùy chọn, mặc định: "Chưa phân loại")*: Thể loại tác phẩm.
  - `--description <str>` *(Tùy chọn)*: Mô tả ngắn gọn về truyện.
  - `--id <str>` *(Tùy chọn, mặc định: tự động slugify từ title)*: Định danh thư mục tác phẩm (`story_id`).
- **Đầu ra (Outputs):**
  - Tạo thư mục `stories/<story_id>/` gồm:
    * `chapters/` (chứa các file chương `chapter_XXXX.md` và `draft.md`).
    * `summaries/` (chứa `outline.md`, `rolling_summary.txt`, `character_bible.json`, `lorebook.json`, `foreshadow.json`).
    * `summaries/memory/` (chứa 5 database JSON của Narrative Memory Engine).
    * `story_config.json` và `story.json`.
  - Tự động đặt tác phẩm mới làm tác phẩm hoạt động (`active_story.json`).
- **Side Effects:** Cập nhật `active_story.json` tại thư mục gốc.
- **Skill liên quan:** `story`, `story-setup`, `story-import`.
- **Giới hạn:** Nếu `story_id` đã tồn tại, lệnh sẽ báo lỗi để tránh ghi đè tác phẩm cũ.

---

### `python manage_story.py select`
- **Mục đích:** Chuyển đổi tác phẩm làm việc hiện hành.
- **Đầu vào:**
  - `--id <story_id>` *(Bắt buộc)*: Định danh tác phẩm cần làm việc.
- **Đầu ra:** Ghi nhận `active_story.json` với `active_story: <story_id>`.
- **Side Effects:** Tất cả các lệnh thao tác ngữ cảnh tiếp theo (`context`, `save`, `check`, `memory`) sẽ trỏ vào tác phẩm này.
- **Skill liên quan:** `story`.
- **Giới hạn:** Báo lỗi nếu thư mục `stories/<story_id>` không tồn tại.

---

### `python manage_story.py stories`
- **Mục đích:** Liệt kê toàn bộ các bộ truyện hiện có trong workspace.
- **Đầu vào:** Không có.
- **Đầu ra:** Bảng danh sách các tác phẩm gồm: ID, Tên truyện, Tác giả, Thể loại, Số chương đã viết, và đánh dấu `[ACTIVE]` cho truyện đang chọn.
- **Side Effects:** Không thay đổi dữ liệu (Read-only).
- **Skill liên quan:** `story`.

---

### `python manage_story.py status`
- **Mục đích:** Hiển thị chi tiết tình trạng tác phẩm đang hoạt động.
- **Đầu vào:** Không có.
- **Đầu ra:** Tên truyện, tác giả, thể loại, tổng số chương, Style Profile đang kích hoạt, và đường dẫn thư mục làm việc.
- **Side Effects:** Không thay đổi dữ liệu (Read-only).
- **Skill liên quan:** `story`, `story-write`, `story-flow`.

---

### `python manage_story.py list`
- **Mục đích:** Liệt kê danh sách tất cả các chương đã viết trong tác phẩm hiện hành.
- **Đầu vào:** Không có.
- **Đầu ra:** Danh sách số chương, tiêu đề chương, ngày tạo và dung lượng từ tóm tắt trong `story.json`.
- **Side Effects:** Read-only.
- **Skill liên quan:** `story`, `story-flow`.

---

## 2. NHÓM LỆNH SÁNG TÁC & LƯU TRỮ (DRAFTING & STORAGE)

### `python manage_story.py context`
- **Mục đích:** Nạp và tổng hợp toàn bộ 5 lớp ngữ cảnh tối ưu token phục vụ việc viết chương tiếp theo.
- **Đầu vào:** Không có.
- **Đầu ra:** Console in ra:
  - Lớp A: Mục tiêu chương tiếp theo từ `outline.md` và luật thế giới.
  - Lớp B: Chấn thương chưa lành, vật phẩm đang giữ, bí mật chưa lộ.
  - Lớp C: Các tranh chấp mở (nếu có).
  - Lớp D: Chỉ dẫn Style Profile đang kích hoạt.
  - Lớp E: Đoạn trích kết thúc của chương liền trước.
- **Side Effects:** Read-only.
- **Skill liên quan:** `story-write`, `story-flow`.

---

### `python manage_story.py save`
- **Mục đích:** Phân tách bản nháp từ `chapters/draft.md`, sao lưu an toàn và lưu vào kho dữ liệu chính thức.
- **Đầu vào:**
  - `--title <str>` *(Tùy chọn)*: Tiêu đề chương nếu không gắn thẻ trong nháp.
  - `--summary <str>` *(Tùy chọn)*: Tóm tắt 1-2 câu diễn biến.
  - `--force` *(Tùy chọn)*: Cho phép ghi đè chương cũ nếu cần.
- **Hỗ trợ Annotation trong `draft.md`:**
  - `/story-title [Tên Chương]` & `/story-brief [Tóm Tắt]`: Lưu thành chương mới `chapters/chapter_XXXX.md`.
  - `/story-study [--profile <name>] [--scope story|global]`: Học văn phong từ đoạn trích nháp.
  - `/story-outline`: Cập nhật toàn bộ nội dung vào `summaries/outline.md`.
  - `/story-foreshadow --clue "<name>" [--chapter N] [--resolve]`: Ghi nhận hoặc giải quyết manh mối.
- **Side Effects:**
  - Tự động sao lưu bản nháp cũ vào `chapters/.draft_backups/draft_YYYYMMDD_HHMMSS.md`.
  - Ghi nguyên tử vào `chapters/chapter_XXXX.md`.
  - Cập nhật số chương trong `story.json` và thêm sự kiện vào `events.json`.
  - Reset `draft.md` về trạng thái ban đầu một cách an toàn.
- **Bảo vệ dữ liệu:** Nếu cú pháp lỗi hoặc file nháp trống, lệnh thoát với mã lỗi và giữ nguyên 100% nội dung `draft.md`.
- **Skill liên quan:** `story-write`, `story-flow`, `story-outline`, `story-study`.

---

### `python manage_story.py append-summary`
- **Mục đích:** Nối bản tóm tắt tích lũy của một chặng nhiều chương vào `summaries/rolling_summary.txt`.
- **Đầu vào:**
  - `--from <int>` *(Bắt buộc)*: Chương bắt đầu.
  - `--to <int>` *(Bắt buộc)*: Chương kết thúc.
  - `--text <str>` *(Bắt buộc)*: Nội dung tóm tắt chặng.
- **Đầu ra:** Thêm khối `=== CHƯƠNG X–Y: [Tóm tắt] ===` vào `rolling_summary.txt`.
- **Side Effects:** Cập nhật file tóm tắt cuốn chiếu.
- **Skill liên quan:** `story-flow`.

---

### `python manage_story.py outline`
- **Mục đích:** Xem nội dung đề cương hiện hành.
- **Đầu vào:** Không có.
- **Đầu ra:** In toàn văn nội dung `summaries/outline.md`.
- **Side Effects:** Read-only.
- **Skill liên quan:** `story-outline`.

---

### `python manage_story.py foreshadow`
- **Mục đích:** Xem danh sách toàn bộ các manh mối, phục bút đang mở và đã giải quyết.
- **Đầu vào:** Không có.
- **Đầu ra:** Danh sách phân loại theo trạng thái (Open / Resolved) từ `summaries/foreshadow.json`.
- **Side Effects:** Read-only.
- **Skill liên quan:** `story-outline`.

---

## 3. NHÓM LỆNH KIỂM SOÁT CHẤT LƯỢNG (QUALITY GATE & DESLOP)

### `python manage_story.py check`
- **Mục đích:** Chốt chặn kiểm soát cơ học chất lượng văn phong, phát hiện cụm từ sáo rỗng AI và lỗi dấu câu tiếng Việt.
- **Đầu vào:**
  - `--file <path>` *(Tùy chọn, mặc định: kiểm tra `chapters/draft.md`)*: Đường dẫn đến file chương bất kỳ cần kiểm tra (ví dụ `chapters/chapter_0005.md`).
- **Đầu ra:**
  - Quét dấu câu: khoảng trắng thừa trước dấu câu, thiếu khoảng trắng sau dấu câu, ngoặc kép thoại lẻ.
  - Quét văn mẫu AI: đối chiếu danh sách đen các cụm từ sáo rỗng tiếng Việt.
  - Áp dụng `.deslop-whitelist` cục bộ: tự động bỏ qua các cụm từ nằm trong whitelist.
  - Thoát mã `0` nếu đạt tiêu chuẩn, thoát mã `1` nếu có lỗi sáo rỗng nghiêm trọng cần khắc phục.
- **Side Effects:** Read-only.
- **Skill liên quan:** `story-write`, `story-flow`, `story-deslop`.

---

### `python scripts/vn_checker.py`
- **Mục đích:** Công cụ Native Python độc lập để kiểm tra hoặc chuẩn hóa nhanh dấu câu.
- **Đầu vào:**
  - `<filepath>`: File cần kiểm tra.
  - `--normalize` *(Tùy chọn)*: Chuẩn hóa tự động khoảng trắng quanh dấu câu và 3 chấm mà không đổi từ ngữ.
- **Side Effects:** Ghi đè file nếu có cờ `--normalize`.
- **Skill liên quan:** `story-deslop`.

---

## 4. NHÓM LỆNH PHÂN TÍCH VĂN PHONG (STYLE ENGINE 2.0)

### `python manage_story.py style`
- **Mục đích:** Bóc tách 5 trục văn phong từ truyện mẫu và quản lý hồ sơ Style Profiles.
- **Đầu vào:**
  - `--learn <path>`: Đường dẫn file `.txt`, `.md` hoặc thư mục chứa các file mẫu để phân tích.
  - `--profile <name>`: Tên định danh cho profile cần tạo.
  - `--scope <story|global|all>` *(Mặc định: story)*: Phạm vi lưu trữ (cục bộ theo truyện hoặc toàn cục dùng chung).
  - `--set <name>`: Kích hoạt profile `<name>` làm style hoạt động cho truyện hiện hành.
  - `--list`: Liệt kê tất cả Style Profiles hiện có và đánh dấu profile active.
  - `--show [<name>]`: Xem toàn văn hướng dẫn quy tắc sáng tác trong `STYLE_PROFILE.md`.
- **Đầu ra:**
  - Xuất 2 file độc lập: `style_profile.json` (dữ liệu máy đọc chuẩn Schema 2.0.0) và `STYLE_PROFILE.md` (quy tắc con người và AI đọc).
  - Lưu bản sao mẫu nguồn vào `source_sample.txt`.
- **Side Effects:** Cập nhật `summaries/active_style_profile.json` hoặc thư viện `style_library/`.
- **Skill liên quan:** `story-study`.

---

## 5. NHÓM LỆNH BỘ NHỚ TRUYỆN DÀI (NARRATIVE MEMORY ENGINE)

### `python manage_story.py memory`
- **Mục đích:** Quản lý và truy vấn bộ nhớ nhân quả, chân lý thế giới, trạng thái tiến trình nhân vật và kiểm định continuity.
- **Các cờ chức năng (Sub-flags):**
  - `--timeline`: Hiển thị toàn bộ trục thời gian sự kiện nhân quả (Causal Timeline).
  - `--character <name>`: Xem hồ sơ chi tiết, chấn thương thể chất, túi đồ vật phẩm và tiến trình tâm lý của nhân vật `<name>`.
  - `--secrets`: Xem ma trận bí mật (thông tin nào nhân vật nào biết / chưa biết).
  - `--audit [--file <path>]`: Kiểm định tính toàn vẹn và quét mâu thuẫn (rò rỉ bí mật, chấn thương bị quên, vật phẩm tự dịch chuyển).
  - `--query <keyword>`: Tìm kiếm dữ kiện/sự kiện theo từ khóa.
  - `--add-event --chapter <N> --title "<title>" --summary "<summary>"`: Ghi nhận sự kiện lịch sử mới vào Timeline.
  - `--add-fact --subject "..." --predicate "..." --object "..." [--type world_truth|character_belief] [--state confirmed|inferred|disputed] [--chapter N]`: Ghi nhận dữ kiện thế giới hoặc niềm tin nhân vật vào Canon.
- **Đầu ra & Side Effects:**
  - Cập nhật các file JSON trong `summaries/memory/`: `canon.json`, `events.json`, `characters_state.json`, `knowledge.json`, `conflicts.json`.
  - Tự động xuất chiếu lại các file Markdown dễ đọc cho tác giả: `summaries/characters.md`, `summaries/timeline.md`, và `summaries/canon.md`.
- **Skill liên quan:** `story`, `story-write`, `story-flow`, `story-review`.

---

## 6. NHÓM LỆNH GIAO DIỆN & TIỆN ÍCH (DASHBOARD & BOOTSTRAP)

### `python manage_story.py dashboard`
- **Mục đích:** Khởi chạy máy chủ Web Dashboard cục bộ để xem trực quan cây thư mục truyện, danh sách chương và tiến trình nhân vật trên trình duyệt web.
- **Đầu vào:** Không có.
- **Đầu ra:** Khởi chạy `scripts/dashboard-server.mjs`, mở cổng HTTP nội bộ (mặc định: `http://localhost:3000`).
- **Skill liên quan:** `story`.

---

### `python scripts/setup_workspace.py`
- **Mục đích:** Tự động kiểm tra và đồng bộ hạ tầng StoryFlow (`manage_story.py`, `scripts/`, `references/`, `assets/`, `style_library/`) vào một workspace mới sau khi người dùng cài đặt bằng `npx skills add`.
- **Skill liên quan:** `story-setup`.
