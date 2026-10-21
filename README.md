# StoryFlow — Hệ Thống Sáng Tác & Quản Trị Tiểu Thuyết Agent-Native (Markdown-First)

> **StoryFlow** là kiến trúc sáng tác tiểu thuyết dài hạn tối ưu cho AI Coding Agents (Google Antigravity, Claude Code, OpenCode...). Hệ thống kết hợp triết lý **Markdown-First** (tác giả và AI làm việc trực tiếp trên các tài liệu Markdown chuẩn mực) với **Bộ công cụ thực thi xác định** (Deterministic Execution Tools) giúp bảo toàn tính bất biến logic, quản lý Narrative Memory nhiều tầng và bảo vệ dữ liệu tuyệt đối.

---

## 🧭 DANH SÁCH 10 SKILL TÍCH HỢP TRONG HỆ SINH THÁI

Hệ thống được thiết kế theo hướng Agent-native: Người dùng chỉ cần bắt đầu bằng `/story` kèm yêu cầu tự nhiên, hoặc kích hoạt trực tiếp các lệnh slash command chuyên biệt:

| Lệnh Slash Command | Tên Skill | Trách Nhiệm & Vai Trò Agent-Native | Điểm Vào Chính |
|---|---|---|---|
| `/story` | `story` | **Trạm điều phối trung tâm (Central Router)**: Tự động nhận diện ý định tự nhiên, kiểm tra trạng thái truyện và định tuyến vào workflow thích hợp nhất mà không hỏi thừa. | `manage_story.py status/select/init` |
| `/story-write` | `story-write` | **Sáng tác tương tác 7 bước (Author-Led)**: Đồng hành cùng tác giả qua từng cảnh/chương, hỗ trợ viết khám phá không đề cương (pantser), chỉnh sửa cục bộ không ghi đè, và bám sát Canon. | `chapters/chapter_XXXX.md` & `draft.md` |
| `/story-flow` | `story-flow` | **Điều phối toàn trình tự hành (Orchestrator)**: Chu trình tự hành khép kín cho truyện dài: Nạp ngữ cảnh → Soạn nháp → Audit kép → Tự sửa lỗi → Cập nhật Memory → Lưu chương liên hoàn. | `manage_story.py context/save/memory` |
| `/story-study` | `story-study` | **Giải mã văn phong 5 trục (Style Engine 2.0)**: AI trực tiếp bóc tách kỹ thuật kể chuyện, kết hợp đo lường định lượng âm tiết; tạo và quản lý Style Profile đa cấp độ (story & global). | `manage_story.py style` |
| `/story-outline` | `story-outline` | **Đề cương thích ứng & Phục bút**: Hoạch định cấu trúc Arc/Chương, gợi ý 3 nhánh rẽ (Action/Emotion/Twist), quản lý sổ tay phục bút và ma trận bí mật; phân biệt rõ kế hoạch tương lai vs sự kiện lịch sử. | `summaries/outline.md` & `foreshadow.json` |
| `/story-deslop` | `story-deslop` | **Biên tập ngữ cảnh & Khử văn mẫu AI**: Loại bỏ câu từ sáo rỗng qua bộ lọc tiếng Việt, áp dụng Show-Don't-Tell, chuẩn hóa dấu câu an toàn và hỗ trợ `.deslop-whitelist`. | `scripts/vn_checker.py` |
| `/story-review` | `story-review` | **Thẩm định phản biện đối kháng 4 cấp độ**: 3 vai độc giả khó tính (Logic/Canon, Tiết tấu/Pacing, Chiều sâu tâm lý/Voice); phân loại lỗi theo 4 cấp độ (Critical, Significant, Soft, Artistic Choice). | [references/LITERARY_EVALUATION_RUBRIC.md](references/LITERARY_EVALUATION_RUBRIC.md) |
| `/story-cover` | `story-cover` | **Thiết kế prompt ảnh bìa AI**: Trích xuất metadata, bối cảnh và cảm xúc truyện; tạo prompt tối ưu cho Midjourney v6 (`--ar 2:3`), SDXL, DALL-E 3 kèm hướng dẫn bố cục typography. | Markdown Prompt Generator |
| `/story-import` | `story-import` | **Nghịch đảo bản thảo cũ nhiều chương**: Phân rã file raw, lập chỉ mục chương, tái dựng Narrative Memory, phân định sự thật vs suy luận mà không sửa đổi file gốc. | `manage_story.py init` & Import Pipeline |
| `/story-setup` | `story-setup` | **Khởi tạo & Cài đặt môi trường**: Tự động tải `manage_story.py`, scripts, references sau khi add skills vào một workspace mới. | `scripts/setup_workspace.py` |

---

## 📚 TÀI LIỆU HƯỚNG DẪN CHI TIẾT

- 📖 **[USAGE_GUIDE.md](USAGE_GUIDE.md)**: Hướng dẫn độc lập cho **14 tình huống sáng tác thực tế** (viết tương tác, viết khám phá, viết dài tự hành, có/không có mẫu phong cách, có/chưa có đề cương, tiếp tục truyện cũ, biên tập cục bộ, khử slop, review 4 cấp, tạo bìa, kết hợp nhiều nhu cầu).
- 📋 **[COMMAND_REGISTRY.md](COMMAND_REGISTRY.md)**: Bảng đăng ký toàn bộ câu lệnh CLI, cờ tham số, đầu vào, đầu ra, tác vụ ngầm (side-effects) và giới hạn kỹ thuật.
- 📖 **[GLOSSARY.md](GLOSSARY.md)**: Bảng thuật ngữ chuẩn hóa các khái niệm cốt lõi (Canon, Invariants, Dramatic Irony, Causal Timeline, 5-Axis Decomposition, 4-Tier Rubric...).
- 🏛️ **[ADR 0001: Native Markdown-First Architecture](docs/adr/0001-native-markdown-first-architecture.md)**: Quyết định kiến trúc kết hợp giữa giao diện Markdown trực tiếp và công cụ Python xác định.

---

## ⚡ BẮT ĐẦU NHANH BẰNG `/story`

Người dùng chỉ cần đưa ra yêu cầu tự nhiên, hệ thống sẽ tự động định tuyến:
```text
/story Tôi muốn viết tiếp chương tiếp theo cho truyện đang chọn.
/story Khởi tạo bộ truyện tiên hiệp mới tên 'Dạ Ma Chi Đạo', tác giả Lãnh Phong.
/story Học văn phong từ file 'samples/kiem-hiep.txt' và tạo profile 'co-long-style'.
/story Hãy soát lỗi logic và thẩm định phản biện cho Chương 5 vừa viết.
```

Hoặc thao tác trực tiếp qua CLI:
```powershell
# Xem danh sách và chọn truyện làm việc
python manage_story.py stories
python manage_story.py select --id <slug_truyen>

# Kiểm tra tình trạng tác phẩm hiện hành
python manage_story.py status

# Nạp 5 lớp ngữ cảnh tối ưu token trước khi viết
python manage_story.py context

# Quét lỗi văn phong & dấu câu bản nháp
python manage_story.py check

# Quản lý Narrative Memory & Timeline
python manage_story.py memory --timeline
python manage_story.py memory --audit

# Mở Web Dashboard giao diện trực quan
python manage_story.py dashboard
```

---

## 📂 CẤU TRÚC THƯ MỤC CHUẨN

```text
story-flow/
├── manage_story.py            # CLI Engine điều phối trung tâm (init, select, context, save, check, style, memory...)
├── USAGE_GUIDE.md             # Hướng dẫn quy trình khép kín cho 14 tình huống sáng tác
├── COMMAND_REGISTRY.md        # Bảng đăng ký đầy đủ các câu lệnh thực thi
├── README.md                  # Giới thiệu kiến trúc và hướng dẫn tổng quan
├── GLOSSARY.md                # Bảng thuật ngữ chuyên ngành sáng tác
├── .gitignore                 # Chặn commit rác, cache, active_story.json
├── style_library/             # Thư viện Style Profiles dùng chung toàn cục (Global)
│   └── <global_profile_id>/
│       ├── style_profile.json # Dữ liệu phân tích 5 trục (Schema 2.0.0)
│       └── STYLE_PROFILE.md   # Quy tắc sáng tác & chỉ dẫn thực thi
├── skills/                    # Bộ 10 Skills con tương thích Agent Skills Spec
│   ├── story/SKILL.md         # Router Skill trung tâm
│   ├── story-write/SKILL.md   # Quy trình viết 7 bước tương tác
│   ├── story-flow/SKILL.md    # Orchestrator tự hành toàn trình
│   ├── story-study/SKILL.md   # Style Engine 5 trục & Multi-Profile
│   ├── story-outline/SKILL.md # Đề cương thích ứng & Phục bút
│   ├── story-deslop/SKILL.md  # Khử văn mẫu AI & Show-Don't-Tell
│   ├── story-review/SKILL.md  # Thẩm định phản biện 4 cấp độ
│   ├── story-cover/SKILL.md   # Tạo prompt ảnh bìa tiểu thuyết AI
│   ├── story-import/SKILL.md  # Nghịch đảo bản thảo truyện cũ
│   └── story-setup/SKILL.md   # Khởi tạo & Đồng bộ công cụ thực thi
├── scripts/                   # Bộ công cụ thực thi xác định (Deterministic Tools)
│   ├── setup_workspace.py     # Script bootstrap môi trường dự án mới
│   ├── narrative_memory.py    # Narrative Memory Engine (Canon, Timeline, Character State, Secrets)
│   ├── vn_checker.py          # Kiểm tra dấu câu, khử slop tiếng Việt & hỗ trợ .deslop-whitelist
│   ├── style_analyzer.py      # Bóc tách định lượng 5 trục văn phong (Schema 2.0.0)
│   └── dashboard-server.mjs   # Máy chủ Web Dashboard cục bộ (Node.js)
├── assets/                    # Giao diện Web Dashboard (HTML/CSS/JS)
├── references/                # Tài liệu tham chiếu văn học chuyên sâu
│   ├── LITERARY_EVALUATION_RUBRIC.md # Khung đánh giá định tính văn học 8 trục & 4 tiers
│   ├── show-dont-tell.md      # Kỹ thuật cảm xúc vật lý & 5 giác quan
│   ├── plot-branching.md      # Quy chuẩn gợi ý 3 nhánh rẽ cốt truyện
│   ├── anti-slop.md           # Danh sách đen loại bỏ văn mẫu AI
│   └── genre-styles/          # 10 công thức thể loại & INDEX_VI.md
├── tests/                     # Bộ kiểm thử tự động (unittest framework — 37 tests)
│   ├── test_p0_data_integrity.py     # Kiểm tra bảo vệ dữ liệu, atomic save & Quality Gate
│   ├── test_style_engine.py          # Kiểm tra 5 trục văn phong & Multi-Profile scoping
│   ├── test_skills_integrity.py      # Kiểm tra tính toàn vẹn và trigger của các Skills
│   ├── test_narrative_memory.py      # Kiểm thử Narrative Memory Engine
│   ├── test_long_novel_regression.py # 10 kịch bản kiểm thử tiểu thuyết dài tập
│   └── test_full_regression.py       # Kiểm thử hồi quy toàn diện
└── stories/                   # Thư mục lưu trữ các tác phẩm
    └── <story_id>/
        ├── chapters/          # Bản thảo và các chương chính thức (chapter_XXXX.md)
        ├── summaries/         # Đề cương, bản chiếu Markdown và hồ sơ phong cách
        └── story_config.json  # Cấu hình tác phẩm
```

---

## 🧪 KIỂM THỬ VÀ XÁC MINH HỆ THỐNG

Toàn bộ hệ sinh thái StoryFlow được bảo vệ bởi bộ kiểm thử tự động gồm **37 test cases** bao phủ toàn diện từ tính toàn vẹn dữ liệu, kiểm định continuity nhân quả đến cấu trúc metadata của các kỹ năng:

```powershell
python -m unittest discover -s tests
```
Tất cả các bài kiểm thử đều chạy trong môi trường cô lập tạm thời (`tempfile.mkdtemp`), đảm bảo không can thiệp hay làm thay đổi dữ liệu tác phẩm của người dùng.
