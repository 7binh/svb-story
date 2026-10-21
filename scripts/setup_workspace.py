#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
setup_workspace.py — Bootstraps StoryFlow runtime into a new project workspace.
Copies manage_story.py, scripts/, references/, assets/, and style_library/
from GitHub repository or local cache without touching .agents/ or existing drafts.
"""

import os
import sys
import shutil
import tempfile
import subprocess

# Ensure UTF-8 output on Windows consoles
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
if sys.stderr.encoding and sys.stderr.encoding.lower() != 'utf-8':
    try:
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass


REPO_URL = "https://github.com/7binh/svb-story.git"


def setup_workspace(target_dir=None):
    target = os.path.abspath(target_dir or os.getcwd())
    print(f"=== STORYFLOW WORKSPACE BOOTSTRAP ===")
    print(f"Mục tiêu cài đặt: {target}\n")

    # Check if manage_story.py already exists
    manage_py = os.path.join(target, "manage_story.py")
    if os.path.exists(manage_py):
        print(f"[INFO] manage_story.py đã tồn tại tại: {manage_py}")
        print("[INFO] Đang tiến hành kiểm tra tính toàn vẹn...")
        res = subprocess.run([sys.executable, manage_py, "--help"], capture_output=True, encoding="utf-8", errors="replace")
        if res.returncode == 0:
            print("✅ Hệ thống StoryFlow đã sẵn sàng hoạt động trong workspace này!")
            return True

    # Clone source to temp folder
    temp_dir = tempfile.mkdtemp(prefix="svb_setup_")
    print(f"[1/4] Đang kéo mã nguồn từ {REPO_URL}...")
    try:
        clone_res = subprocess.run(
            ["git", "clone", "--depth", "1", REPO_URL, temp_dir],
            capture_output=True,
            encoding="utf-8",
            errors="replace"
        )
        if clone_res.returncode != 0:
            print(f"[ERROR] Không thể clone repository từ GitHub: {clone_res.stderr}")
            shutil.rmtree(temp_dir, ignore_errors=True)
            return False

        print("[2/4] Đang sao chép các thành phần thực thi vào workspace...")
        items_to_copy = [
            ("manage_story.py", False),
            ("scripts", True),
            ("references", True),
            ("assets", True),
            ("style_library", True),
        ]

        for item_name, is_dir in items_to_copy:
            src = os.path.join(temp_dir, item_name)
            dst = os.path.join(target, item_name)
            if not os.path.exists(src):
                continue
            if is_dir:
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
            print(f"  + Đã sao chép: {item_name}")

        stories_dir = os.path.join(target, "stories")
        os.makedirs(stories_dir, exist_ok=True)
        print("  + Đảm bảo thư mục stories/ đã sẵn sàng.")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

    print("[3/4] Kiểm tra vận hành công cụ...")
    verify_res = subprocess.run([sys.executable, manage_py, "--help"], capture_output=True, encoding="utf-8", errors="replace")
    if verify_res.returncode == 0:
        print("[4/4] ✅ Cài đặt hoàn tất thành công 100%!")
        print("\n👉 Bạn có thể bắt đầu sử dụng ngay:")
        print("  - Xem danh mục truyện   : python manage_story.py stories")
        print("  - Khởi tạo truyện đầu   : python manage_story.py init --title \"Tên Truyện\" --author \"Tác Giả\" --genre \"Thể Loại\"")
        print("  - Viết chương tương tác: /story-write hoặc python manage_story.py context")
        return True
    else:
        print(f"[ERROR] Kiểm tra manage_story.py thất bại: {verify_res.stderr}")
        return False


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else None
    success = setup_workspace(target)
    sys.exit(0 if success else 1)
