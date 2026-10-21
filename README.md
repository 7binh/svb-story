# StoryFlow — Hệ Thống Sáng Tác & Quản Trị Tiểu Thuyết Đa Tác Phẩm (Author-Led Story Engine)

> **StoryFlow** kết hợp triết lý kiểm soát của tác giả (từ `agent_story_writer`) với bộ công cụ kiểm duyệt chất lượng, đề cương thích ứng và giao diện trực quan (từ `.agents`).

---

## 🧭 DANH SÁCH 8 SKILL CON TÍCH HỢP TRONG HỆ SINH THÁI

Khi bạn cài đặt repository này qua `npx skills add 7binh/svb-story`, bạn sẽ sở hữu trọn bộ 8 skill con tương ứng với 8 lệnh slash command chuyên biệt:

| Lệnh Slash Command | Tên Skill | Chức Năng Chính |
|---|---|---|
| `/story` | `story` | **Trạm điều phối trung tâm (Router)**: Điều hướng yêu cầu, chuyển đổi tác phẩm, khởi chạy Web Dashboard. |
| `/story-write` | `story-write` | **Quy trình viết chính**: Vòng lặp 5 bước (context -> nháp draft.md -> check -> save). |
| `/story-outline` | `story-outline` | **Đề cương & Phục bút**: Hoạch định Arc, gợi ý 3 nhánh rẽ cốt truyện khi bí ý, theo dõi manh mối. |
| `/story-deslop` | `story-deslop` | **Khử văn mẫu AI**: Loại bỏ câu từ sáo rỗng, áp dụng Show-Don't-Tell và chiều sâu giác quan. |
| `/story-review` | `story-review` | **Thẩm định phản biện đa góc nhìn**: 3 vai độc giả khó tính soát lỗi Logic, Nhịp điệu, Nhân vật. |
| `/story-cover` | `story-cover` | **Thiết kế ảnh bìa AI**: Tự động tạo prompt sinh ảnh bìa chuyên nghiệp từ thông số truyện. |
| `/story-import` | `story-import` | **Nhập bản thảo cũ**: Tự động phân rã file truyện cũ nhiều chương vào cấu trúc chuẩn đa tác phẩm. |
| `/story-flow` | `story-flow` | **Toàn trình hợp nhất**: Vòng lặp sáng tác tổng quát kết hợp cả quản lý và viết. |

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
