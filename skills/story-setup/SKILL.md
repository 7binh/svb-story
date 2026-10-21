---
name: story-setup
description: "Khởi tạo và cài đặt toàn bộ công cụ thực thi StoryFlow (manage_story.py, scripts, references, assets) cho dự án mới sau khi chạy 'skills add'. Kích hoạt: /story-setup, 'cài đặt môi trường', 'setup project', 'chuẩn bị viết truyện', 'tải manage_story.py'."
---

# /story-setup: Cài Đặt & Đồng Bộ Hạ Tầng Sáng Tác StoryFlow

Khi người dùng cài đặt bộ kỹ năng qua lệnh `npx skills add 7binh/svb-story`, trình quản lý kỹ năng chỉ tải về các file hướng dẫn tư duy (`SKILL.md`) vào thư mục `.agents/skills/` mà không tải các file mã nguồn thực thi ở thư mục gốc của repository.

Skill `/story-setup` chịu trách nhiệm trang bị đầy đủ công cụ thực thi gồm:
1. `manage_story.py` (CLI điều phối trung tâm).
2. `scripts/` (Narrative Memory Engine, Style Engine 2.0, vn_checker, dashboard server).
3. `references/` (Tài liệu tham chiếu Show-Don't-Tell, rubric văn học, thể loại).
4. `assets/` (Web Dashboard UI).
5. `style_library/` (Thư viện phong cách toàn cục).
6. Khởi tạo thư mục `stories/`.

---

## 🔍 BƯỚC 1: KIỂM TRA MÔI TRƯỜNG HIỆN TẠI (DIAGNOSTICS)

Trước khi thực thi, kiểm tra xem workspace hiện tại đã có `manage_story.py` chưa:
- Nếu `manage_story.py` **đã tồn tại**:
  Chạy lệnh kiểm tra phiên bản:
  ```powershell
  python manage_story.py status
  ```
  Báo cáo hệ sinh thái đã sẵn sàng, hiển thị tác phẩm đang chọn và mời tác giả bắt đầu bằng `/story-write` hoặc `/story-flow`.
- Nếu `manage_story.py` **chưa tồn tại**: Tiến hành Bước 2 để tự động kéo mã nguồn về.

---

## 🚀 BƯỚC 2: TỰ ĐỘNG ĐỒNG BỘ CÔNG CỤ (BOOTSTRAPPING PIPELINE)

AI Agent tự động thực hiện lệnh tải mã nguồn từ kho lưu trữ `https://github.com/7binh/svb-story.git`:

```powershell
# 1. Tạo thư mục tạm và clone bản mới nhất
git clone --depth 1 https://github.com/7binh/svb-story.git .svb_setup_tmp

# 2. Sao chép các thành phần thực thi vào thư mục dự án hiện tại (không ghi đè .agents)
Copy-Item -Path .svb_setup_tmp\manage_story.py -Destination .\ -Force
Copy-Item -Path .svb_setup_tmp\scripts -Destination .\ -Recurse -Force
Copy-Item -Path .svb_setup_tmp\references -Destination .\ -Recurse -Force
Copy-Item -Path .svb_setup_tmp\assets -Destination .\ -Recurse -Force
Copy-Item -Path .svb_setup_tmp\style_library -Destination .\ -Recurse -Force
if (-not (Test-Path .\stories)) { New-Item -ItemType Directory -Path .\stories }

# 3. Dọn dẹp thư mục tạm
Remove-Item -Path .svb_setup_tmp -Recurse -Force
```

*(Hoặc chạy script đồng bộ bằng Python nếu môi trường ưu tiên Python: `python -c "import subprocess, shutil, os, tempfile; td=tempfile.mkdtemp(); subprocess.run(['git', 'clone', '--depth', '1', 'https://github.com/7binh/svb-story.git', td]); ..."`)*

---

## ✅ BƯỚC 3: XÁC THỰC TÍNH TOÀN VẸN (VERIFICATION)

Chạy lệnh kiểm tra tính sẵn sàng của công cụ:
```powershell
python manage_story.py --help
```
Yêu cầu: Lệnh trả về mã 0 và hiển thị đầy đủ các subcommand: `init`, `select`, `stories`, `save`, `context`, `check`, `style`, `memory`, `dashboard`.

---

## 📖 BƯỚC 4: KHỞI TẠO TÁC PHẨM ĐẦU TIÊN (FIRST STORY ONBOARDING)

1. Kiểm tra danh mục tác phẩm:
   ```powershell
   python manage_story.py stories
   ```
2. Nếu chưa có tác phẩm nào, gợi ý tác giả đặt tên và thể loại để khởi tạo:
   ```text
   Hạ tầng StoryFlow đã sẵn sàng! Bạn muốn đặt tên tác phẩm đầu tiên là gì?
   - Tiêu đề truyện: ...
   - Bút danh tác giả: ...
   - Thể loại: (Tiên hiệp, Đô thị, Trinh thám, Huyền bí...)
   ```
   Sau khi tác giả cung cấp thông tin, chạy lệnh:
   ```powershell
   python manage_story.py init --title "<Tên Truyện>" --author "<Tác Giả>" --genre "<Thể Loại>"
   ```
3. Sau khi khởi tạo xong, hướng dẫn tác giả chuyển sang `/story-write` để bắt đầu viết chương 1!
