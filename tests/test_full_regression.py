import os
import json
import unittest
from tests.helpers import isolated_workspace
import scripts.style_analyzer as sa


class TestFullRegression(unittest.TestCase):

    def test_legacy_profile_migration(self):
        """Test migrating legacy 1.0.0 profile to schema 2.0.0."""
        legacy_data = {
            "profile_id": "old_style",
            "version": "1.0.0",
            "fingerprint": {"stats": {"total_words": 100}},
            "style_rules": {"rule1": "test"}
        }

        migrated = sa.migrate_legacy_profile(legacy_data)
        self.assertEqual(migrated["schema_version"], "2.0.0")
        self.assertEqual(migrated["analysis_version"], "2.0.0")
        self.assertIn("scene_variants", migrated)
        self.assertIn("confidence_and_limitations", migrated)
        # Original fields preserved
        self.assertEqual(migrated["profile_id"], "old_style")

    def test_empty_draft_rejection(self):
        """Empty draft is cleanly rejected with non-zero exit code."""
        with isolated_workspace() as (ws, run_cli):
            run_cli("init", "--title", "Test Story", "--id", "test-story")
            draft_path = os.path.join(ws, "stories", "test-story", "chapters", "draft.md")

            # Write empty content
            with open(draft_path, "w", encoding="utf-8") as f:
                f.write("   \n\n   ")

            res = run_cli("save")
            self.assertNotEqual(res.returncode, 0)
            self.assertIn("File nháp trống", res.stdout + res.stderr)

    def test_invalid_cli_command_rejection(self):
        """Unknown command is cleanly rejected by argparse with non-zero exit code."""
        with isolated_workspace() as (ws, run_cli):
            res = run_cli("invalid-command")
            self.assertNotEqual(res.returncode, 0)

    def test_context_when_no_active_style_profile(self):
        """Context command outputs 'No active style profile' cleanly when no profile is set."""
        with isolated_workspace() as (ws, run_cli):
            run_cli("init", "--title", "Test Story", "--id", "test-story")

            res = run_cli("context")
            self.assertEqual(res.returncode, 0)
            self.assertIn("No active style profile", res.stdout)

    def test_story_study_draft_preserves_sample_source(self):
        """When /story-study is used in draft, draft text is preserved and backed up to profile."""
        with isolated_workspace() as (ws, run_cli):
            run_cli("init", "--title", "Test Story", "--id", "test-story")
            draft_path = os.path.join(ws, "stories", "test-story", "chapters", "draft.md")

            sample_text = (
                "/story-study --profile excerpt-prof\n"
                "Ánh trăng tà rọi xuống mặt hồ tĩnh lặng. Nàng khẽ nghiêng đầu lắng nghe tiếng gió rít."
            )
            with open(draft_path, "w", encoding="utf-8") as f:
                f.write(sample_text)

            res = run_cli("save")
            self.assertEqual(res.returncode, 0, f"Save study failed: {res.stderr or res.stdout}")

            # Verify draft still contains the sample text (not silently wiped)
            with open(draft_path, "r", encoding="utf-8") as f:
                current_draft = f.read()
            self.assertIn("Ánh trăng tà rọi xuống", current_draft)

            # Verify backup in profile dir
            prof_dir = os.path.join(ws, "stories", "test-story", "summaries", "style_profiles", "excerpt-prof")
            self.assertTrue(os.path.exists(os.path.join(prof_dir, "source_sample.txt")))


if __name__ == "__main__":
    unittest.main()
