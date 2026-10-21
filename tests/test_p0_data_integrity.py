import os
import unittest
from tests.helpers import isolated_workspace


class TestP0DataIntegrity(unittest.TestCase):

    def test_check_fails_or_warns_when_script_crashes(self):
        """Proof that check command does NOT falsely report pass when checker crashes."""
        with isolated_workspace() as (ws, run_cli):
            # Init a story
            res = run_cli("init", "--title", "Test Truyện", "--id", "test-story")
            self.assertEqual(res.returncode, 0)

            # Write a draft
            draft_path = os.path.join(ws, "stories", "test-story", "chapters", "draft.md")
            with open(draft_path, "w", encoding="utf-8") as f:
                f.write("/story-title Chương 1: Khởi Đầu\n/story-brief Tóm tắt\nNội dung chương một...")

            # Run check
            res_check = run_cli("check")
            # If scripts crash (which they do currently because style-whitelist is missing),
            # check MUST NOT report pass or silent success
            output = res_check.stdout + res_check.stderr
            # Must NOT claim false positive pass:
            if "Cannot find module" in output or res_check.returncode != 0:
                self.assertNotIn("✓ Không phát hiện văn mẫu AI nghiêm trọng.", res_check.stdout,
                                 "False positive detected: reported clean slop while checker crashed!")

    def test_save_handles_leading_blank_lines_and_bom(self):
        """Save must handle leading blank lines and UTF-8 BOM without rejecting valid annotation."""
        with isolated_workspace() as (ws, run_cli):
            run_cli("init", "--title", "Test Truyện", "--id", "test-story")
            draft_path = os.path.join(ws, "stories", "test-story", "chapters", "draft.md")

            # Write draft with BOM and 2 leading blank lines
            content = "\ufeff\n\n/story-title Chương 1: Bước Ngoặt\n/story-brief Gặp gỡ nhân vật mới\nNội dung chương 1 đầy đủ."
            with open(draft_path, "w", encoding="utf-8") as f:
                f.write(content)

            res_save = run_cli("save")
            self.assertEqual(res_save.returncode, 0, f"Save failed with leading newlines: {res_save.stderr or res_save.stdout}")

            ch1_path = os.path.join(ws, "stories", "test-story", "chapters", "chapter_0001.md")
            self.assertTrue(os.path.exists(ch1_path), "chapter_0001.md was not created!")
            with open(ch1_path, "r", encoding="utf-8") as f:
                saved_text = f.read()
            self.assertIn("Nội dung chương 1 đầy đủ", saved_text)

    def test_save_preserves_draft_when_annotation_invalid(self):
        """When draft has invalid annotation, it must NOT be reset or deleted."""
        with isolated_workspace() as (ws, run_cli):
            run_cli("init", "--title", "Test Truyện", "--id", "test-story")
            draft_path = os.path.join(ws, "stories", "test-story", "chapters", "draft.md")

            invalid_content = "Đây là văn bản không có annotation dòng đầu hợp lệ..."
            with open(draft_path, "w", encoding="utf-8") as f:
                f.write(invalid_content)

            res_save = run_cli("save")
            self.assertNotEqual(res_save.returncode, 0, "Save should fail for invalid annotation")

            with open(draft_path, "r", encoding="utf-8") as f:
                preserved_content = f.read()
            self.assertEqual(preserved_content, invalid_content, "Draft content was modified or reset on failure!")

    def test_save_creates_backup_before_reset(self):
        """When draft is saved, a backup copy of the draft is safely archived before reset."""
        with isolated_workspace() as (ws, run_cli):
            run_cli("init", "--title", "Test Truyện", "--id", "test-story")
            draft_path = os.path.join(ws, "stories", "test-story", "chapters", "draft.md")

            content = "/story-title Chương 1\n/story-brief Brief 1\nNội dung cần lưu..."
            with open(draft_path, "w", encoding="utf-8") as f:
                f.write(content)

            res_save = run_cli("save")
            self.assertEqual(res_save.returncode, 0)

            backup_dir = os.path.join(ws, "stories", "test-story", "chapters", ".draft_backups")
            self.assertTrue(os.path.exists(backup_dir), ".draft_backups directory was not created!")
            backups = os.listdir(backup_dir)
            self.assertGreaterEqual(len(backups), 1, "No backup file found in .draft_backups!")

    def test_append_summary_subcommand_registered_and_working(self):
        """python manage_story.py append-summary must be a registered CLI command and append correctly."""
        with isolated_workspace() as (ws, run_cli):
            run_cli("init", "--title", "Test Truyện", "--id", "test-story")

            res = run_cli("append-summary", "--from", "1", "--to", "10", "--text", "Tóm tắt từ chương 1 đến 10.")
            self.assertEqual(res.returncode, 0, f"append-summary failed: {res.stderr or res.stdout}")

            summary_file = os.path.join(ws, "stories", "test-story", "summaries", "rolling_summary.txt")
            with open(summary_file, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn("CHƯƠNG 1–10", content)
            self.assertIn("Tóm tắt từ chương 1 đến 10.", content)

    def test_native_vietnamese_checker_and_whitelist(self):
        """Native vn_checker correctly detects slop and respects .deslop-whitelist."""
        with isolated_workspace() as (ws, run_cli):
            run_cli("init", "--title", "Test Truyện", "--id", "test-story")
            draft_path = os.path.join(ws, "stories", "test-story", "chapters", "draft.md")

            # Write slop into draft
            with open(draft_path, "w", encoding="utf-8") as f:
                f.write("/story-title Chương 1\n/story-brief Brief 1\nKhông thể phủ nhận rằng bầu không khí bỗng ngưng đọng lại.")

            # Check without whitelist should fail
            res1 = run_cli("check")
            self.assertNotEqual(res1.returncode, 0)
            self.assertIn("Phát hiện", res1.stdout)

            # Create .deslop-whitelist
            wl_path = os.path.join(ws, "stories", "test-story", ".deslop-whitelist")
            with open(wl_path, "w", encoding="utf-8") as f:
                f.write("Không thể phủ nhận rằng\nbầu không khí bỗng ngưng đọng lại\n")

            # Check with whitelist should pass
            res2 = run_cli("check")
            self.assertEqual(res2.returncode, 0, f"Check failed despite whitelist: {res2.stderr or res2.stdout}")
            self.assertIn("BẢN NHÁP ĐẠT TIÊU CHUẨN CHẤT LƯỢNG", res2.stdout)


if __name__ == "__main__":
    unittest.main()
