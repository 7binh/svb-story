# StoryFlow — Hệ Thống Sáng Tác & Quản Trị Tiểu Thuyết Đa Tác Phẩm (Author-Led Story Engine)

> **StoryFlow** kết hợp triết lý kiểm soát của tác giả (từ `agent_story_writer`) với bộ công cụ kiểm duyệt chất lượng, đề cương thích ứng và giao diện trực quan (từ `.agents`).

---

## 💡 ĐIỂM KẾT HỢP VỚI KHO SKILL .AGENTS

StoryFlow tích hợp trực tiếp các thế mạnh kỹ thuật từ kho `.agents` vào luồng sáng tác:

1. **Bộ lọc khử văn mẫu AI & Chuẩn hóa dấu câu (Quality Gate):**
   - Tích hợp trực tiếp `scripts/normalize-punctuation.js` và `scripts/check-ai-patterns.js`.
   - Lệnh kiểm tra trước khi lưu: `python manage_story.py check`.
2. **Dashboard Trực Quan (Web UI):**
   - Tích hợp `scripts/dashboard-server.mjs` và thư mục `assets/`.
   - Lệnh mở giao diện Web quản lý truyện: `python manage_story.py dashboard`.
3. **Kho công thức thể loại (Genre Formulas):**
   - Tích hợp toàn bộ thư mục `references/genre-styles/` (Huyền huyễn, Đô thị, Trinh thám, Kinh dị...).
4. **Hệ sinh thái vệ tinh kế thừa:**
   - Hỗ trợ tương tác với các skill vệ tinh: `story-review` (thẩm định đa vai), `story-cover` (tạo bìa truyện), `story-scan` (quét đề tài hot), `story-import` (nhập truyện cũ).

---

## 🚀 CÀI ĐẶT BẰNG NPX SKILLS

Sau khi đưa repository này lên GitHub, bạn có thể cài đặt skill này vào bất kỳ dự án nào bằng lệnh:

```bash
npx skills add 7binh/svb-story
```

Hệ thống sẽ tự động nhận diện skill `story-flow` (kích hoạt bằng `/story-flow` hoặc `/story-write`).

---

## 📂 CẤU TRÚC HỆ THỐNG

```text
story-flow/
├── manage_story.py            # CLI điều phối trung tâm (context, save, check, dashboard...)
├── SKILL.md                   # Định nghĩa Skill chính cho AI Agent
├── README.md                  # Tài liệu hướng dẫn
├── .gitignore                 # Chặn commit rác, cache, active_story.json
├── skills/
│   └── story-flow/
│       └── SKILL.md           # Bản sao tương thích với npx skills add
├── scripts/                   # Bộ công cụ kế thừa từ .agents
│   ├── check-ai-patterns.js   # Quét văn mẫu AI & câu cú lặp
│   ├── normalize-punctuation.js # Chuẩn hóa dấu câu, đối thoại
│   └── dashboard-server.mjs   # Server Web Dashboard cục bộ
├── assets/                    # Giao diện Web Dashboard (HTML/CSS/JS)
├── references/                # Tài liệu tham chiếu văn phong chuyên sâu
│   ├── show-dont-tell.md      # Kỹ thuật hữu hình hóa cảm xúc, đối thoại đa tầng
│   ├── plot-branching.md      # Quy trình gợi ý 3 nhánh rẽ cốt truyện
│   ├── anti-slop.md           # Danh sách đen loại bỏ văn mẫu AI
│   └── genre-styles/          # Công thức các thể loại đặc thù (từ .agents)
└── stories/                   # Thư mục chứa các tác phẩm
    └── <story_id>/
        ├── story_config.json  # Metadata truyện
        ├── story.json         # Danh sách chương & tóm tắt ngắn (Brief)
        ├── chapters/
        │   ├── draft.md       # File nháp đa năng (dùng Annotation Routing)
        │   └── chapter_*.md   # Các chương hoàn chỉnh
        └── summaries/
            ├── rolling_summary.txt  # Tóm tắt cuốn chiếu mỗi 10 chương
            ├── outline.md           # Đề cương mục tiêu phân đoạn & các chương
            ├── foreshadow.json      # Sổ theo dõi phục bút / manh mối
            ├── character_bible.json # Hồ sơ & diễn biến nhân vật
            └── lorebook.json        # Thiết lập thế giới & bối cảnh
```
