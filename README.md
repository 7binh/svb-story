# StoryFlow — Hệ Thống Sáng Tác & Quản Trị Tiểu Thuyết Đa Tác Phẩm (Author-Led Story Engine)

> **StoryFlow** kết hợp triết lý kiểm soát của tác giả (từ `agent_story_writer`) với bộ công cụ kiểm duyệt chất lượng, giải mã văn phong 5 trục, đề cương thích ứng và giao diện trực quan (từ `.agents`).

---

## 🧭 DANH SÁCH 10 SKILL CON TÍCH HỢP TRONG HỆ SINH THÁI

Khi bạn cài đặt repository này qua `npx skills add 7binh/svb-story`, bạn sẽ sở hữu trọn bộ 10 skill con tương ứng với các lệnh slash command chuyên biệt:

| Lệnh Slash Command | Tên Skill | Chức Năng Chính | Entrypoint CLI / File |
|---|---|---|---|
| `/story-setup` | `story-setup` | **Khởi tạo & Cài đặt môi trường**: Tự động tải `manage_story.py`, scripts, references sau khi add skills. | `scripts/setup_workspace.py` |
| `/story` | `story` | **Trạm điều phối trung tâm (Router)**: Điều hướng yêu cầu, chuyển tác phẩm, tra cứu trạng thái. | `manage_story.py stories/select/init` |
| `/story-write` | `story-write` | **Quy trình viết tương tác 5 bước**: Tuân thủ Style Enforcement Pipeline (context → draft → check → save). | `manage_story.py context/save/check` |
| `/story-flow` | `story-flow` | **Điều phối toàn trình tự hành (Orchestrator)**: Chu trình tự hành khép kín cho AI Agent. | `manage_story.py` |
| `/story-study` | `story-study` | **Học & Giải mã văn phong 5 trục**: Phân tích từ thư mục, file hoặc dán nháp; tạo Style Profile (story & global). | `manage_story.py style` |
| `/story-outline` | `story-outline` | **Đề cương & Phục bút**: Hoạch định Arc, gợi ý 3 nhánh rẽ cốt truyện (Action/Emotion/Twist), theo dõi manh mối. | `manage_story.py outline/foreshadow` |
| `/story-deslop` | `story-deslop` | **Khử văn mẫu AI**: Loại bỏ câu từ sáo rỗng qua `vn_checker`, áp dụng Show-Don't-Tell và chiều sâu giác quan. | `manage_story.py check` |
| `/story-review` | `story-review` | **Thẩm định phản biện đa góc nhìn**: 3 vai độc giả khó tính soát lỗi Logic, Nhịp điệu, Nhân vật. | Rubric hướng dẫn AI |
| `/story-cover` | `story-cover` | **Thiết kế ảnh bìa AI**: Tự động tạo prompt sinh ảnh bìa chuyên nghiệp từ thông số truyện. | Prompt Generator |
| `/story-import` | `story-import` | **Nhập bản thảo cũ**: Phân rã file truyện cũ nhiều chương vào cấu trúc chuẩn đa tác phẩm. | `manage_story.py init` & Regex bóc tách |

---

## 📋 BẢNG COMMAND REGISTRY CHUẨN HÓA

| Lệnh Slash Command | Cú pháp CLI tương ứng | Annotation trong `draft.md` | Tác vụ & Side Effects |
|---|---|---|---|
| `/story-setup` | `python scripts/setup_workspace.py` | Không áp dụng | Khởi tạo môi trường, kéo `manage_story.py`, scripts, references sau khi add skill. |
| `/story` | `python manage_story.py stories`<br>`python manage_story.py select --id <slug>`<br>`python manage_story.py init --title "..."` | Không áp dụng | Khởi tạo, chọn hoặc xem danh mục tác phẩm. Cập nhật `active_story.json`. |
| `/story-write` | `python manage_story.py context`<br>`python manage_story.py check`<br>`python manage_story.py save` | Dòng 1: `/story-title <Tên>`<br>Dòng 2: `/story-brief <Tóm tắt>` | Nạp ngữ cảnh, kiểm tra slop, sao lưu nháp vào `.draft_backups/`, lưu chương mới `chapter_XXXX.md`. |
| `/story-study` | `python manage_story.py style --learn <path> [--profile <n>] [--scope story\|global]`<br>`python manage_story.py style --list`<br>`python manage_story.py style --set <n>` | Dòng 1: `/story-study [--profile <n>] [--scope story\|global]` | Bóc tách 5 trục văn phong, tạo `style_profile.json` và `STYLE_PROFILE.md`. Bảo toàn nguồn mẫu. |
| `/story-outline` | `python manage_story.py outline`<br>`python manage_story.py foreshadow` | Dòng 1: `/story-outline` hoặc `/story-foreshadow --clue "..." --chapter N` | Cập nhật đề cương `outline.md` hoặc danh sách manh mối `foreshadow.json`. |
| — | `python manage_story.py memory [--timeline\|--character <n>\|--secrets\|--audit\|--query <q>]` | Không áp dụng | Quản lý Narrative Memory Engine: timeline nhân quả, trạng thái nhân vật, bí mật, quét mâu thuẫn continuity. |
| `/story-flow` | Toàn bộ chu trình lệnh trên | Tương tự `/story-write` | Điều phối toàn trình tự động với chốt chặn an toàn bản nháp. |
| — | `python manage_story.py append-summary --from X --to Y --text "..."` | Dòng 1: `/story-summary --from X --to Y` | Nối tóm tắt mốc vào `rolling_summary.txt`. |
| — | `python manage_story.py dashboard` | Không áp dụng | Khởi chạy máy chủ Web Dashboard cục bộ xem cây truyện. |

---

## 🚀 CÀI ĐẶT BẰNG NPX SKILLS

Sau khi đưa repository này lên GitHub, bạn có thể cài đặt skill này vào bất kỳ dự án nào bằng lệnh:

```bash
npx skills add 7binh/svb-story
```

Hệ thống sẽ tự động quét thư mục `skills/` và nạp trọn bộ cả 9 skill con độc lập.

---

## 📂 CẤU TRÚC HỆ THỐNG

```text
story-flow/
├── manage_story.py            # CLI Engine điều phối trung tâm (init, select, context, save, check, style...)
├── README.md                  # Tài liệu hướng dẫn hệ thống
├── .gitignore                 # Chặn commit rác, cache, active_story.json
├── style_library/             # Thư viện Style Profiles dùng chung toàn cục (Global)
│   └── <global_profile_id>/
│       ├── style_profile.json # Dữ liệu phân tích 5 trục (Schema 2.0.0)
│       └── STYLE_PROFILE.md   # Quy tắc sáng tác & chỉ dẫn thực thi
├── skills/                    # Bộ 10 Skills con tương thích npx skills add
│   ├── story-setup/SKILL.md   # Khởi tạo & Đồng bộ công cụ thực thi
│   ├── story/SKILL.md         # Router Skill điều phối
│   ├── story-write/SKILL.md   # Quy trình viết 7 bước tương tác
│   ├── story-flow/SKILL.md    # Orchestrator tự hành toàn trình
│   ├── story-study/SKILL.md   # Style Engine 5 trục & Multi-Profile
│   ├── story-outline/SKILL.md # Đề cương & Phục bút
│   ├── story-deslop/SKILL.md  # Khử văn mẫu AI & Show-Don't-Tell
│   ├── story-review/SKILL.md  # Thẩm định phản biện 4 cấp độ
│   ├── story-cover/SKILL.md   # Tạo prompt ảnh bìa tiểu thuyết AI
│   └── story-import/SKILL.md  # Nghịch đảo truyện cũ nhiều chương
├── scripts/                   # Bộ công cụ kỹ thuật
│   ├── setup_workspace.py     # Script tự động kéo mã nguồn về dự án mới
│   ├── narrative_memory.py    # Narrative Memory Engine (Canon, Timeline, Character State, Secrets)
│   ├── vn_checker.py          # Kiểm tra dấu câu & khử slop tiếng Việt (Native Python)
│   ├── style_analyzer.py      # Module bóc tách 5 trục văn phong (Schema 2.0.0)
│   ├── style-whitelist.js     # Quản lý ngoại lệ danh sách trắng
│   ├── check-ai-patterns.js   # Quét mẫu câu sáo rỗng mở rộng
│   ├── normalize-punctuation.js # Chuẩn hóa dấu câu
│   └── dashboard-server.mjs   # Máy chủ Web Dashboard cục bộ (Node.js)
├── assets/                    # Giao diện Web Dashboard (HTML/CSS/JS)
├── references/                # Tài liệu tham chiếu sáng tác chuyên sâu
│   ├── LITERARY_EVALUATION_RUBRIC.md # Khung đánh giá định tính văn học 8 trục
│   ├── show-dont-tell.md      # Kỹ thuật cảm xúc vật lý & 5 giác quan
│   ├── plot-branching.md      # Quy chuẩn gợi ý 3 nhánh rẽ cốt truyện
│   ├── anti-slop.md           # Danh sách đen loại bỏ văn mẫu AI
│   └── genre-styles/          # 10 công thức thể loại & INDEX_VI.md
├── tests/                     # Bộ kiểm thử tự động (unittest framework — 35 tests)
│   ├── test_p0_data_integrity.py     # Kiểm tra bảo vệ dữ liệu & Quality Gate
│   ├── test_style_engine.py          # Kiểm tra 5 trục văn phong & Profile
│   ├── test_skills_integrity.py      # Kiểm tra tính toàn vẹn của 9 Skills
│   ├── test_narrative_memory.py      # Kiểm thử Narrative Memory Engine
│   ├── test_long_novel_regression.py # 10 kịch bản kiểm thử tiểu thuyết dài tập
│   └── test_full_regression.py       # Kiểm thử hồi quy toàn diện
└── stories/                   # Thư mục lưu trữ các tác phẩm
    └── <story_id>/
        ├── story_config.json  # Metadata truyện
        ├── story.json         # Index danh sách chương & brief
        ├── chapters/
        │   ├── draft.md       # File nháp tương tác (Annotation Routing)
        │   ├── .draft_backups/ # Bản sao lưu an toàn trước khi reset nháp
        │   └── chapter_*.md   # Các chương hoàn chỉnh
        └── summaries/
            ├── memory/        # Narrative Memory Database (Phase 2)
            │   ├── canon.json             # Dữ kiện chân lý có nguồn gốc (Provenance)
            │   ├── events.json            # Trục thời gian chuỗi sự kiện nhân quả
            │   ├── characters_state.json  # Trạng thái tiến trình nhân vật (Chấn thương, Vật phẩm)
            │   ├── knowledge.json         # Ma trận bí mật & kiến thức nhân vật
            │   └── conflicts.json         # Nhật ký tranh chấp mâu thuẫn
            ├── rolling_summary.txt        # Tóm tắt cuốn chiếu mỗi 10 chương
            ├── outline.md                 # Đề cương phân đoạn & kế hoạch chương
            ├── foreshadow.json            # Sổ theo dõi phục bút / manh mối
            ├── character_bible.json       # Hồ sơ nhân vật
            ├── lorebook.json              # Thiết lập thế giới & bối cảnh
            ├── active_style_profile.json  # Lưu profile đang active (story hoặc global)
            └── style_profiles/            # Hồ sơ văn phong riêng của tác phẩm
```
