import os
import json
import unittest
from tests.helpers import isolated_workspace
import scripts.style_analyzer as sa


class TestStyleEngine(unittest.TestCase):

    def test_analyzer_five_axes_and_schema_version(self):
        """Analyze text and verify schema 2.0.0, 5 axes, and metrics labeling."""
        sample_text = (
            "Trời vừa chập tối, ngọn gió lạnh rít qua từng khe cửa gỗ mục nát.\n"
            "— Ngươi thực sự muốn đi sao? — Nàng hỏi khẽ, đồng tử co rút lại vì sợ hãi.\n"
            "— Phải đi. Không thể ở lại nơi này thêm một khắc nào nữa.\n"
            "Hắn siết chặt chuôi kiếm trong tay, gân xanh nổi cộm trên mu bàn tay thô ráp. "
            "Trong lòng hắn thầm nhủ: phen này nếu không thành công thì chỉ có con đường chết. "
            "Bóng đêm mênh mông như nuốt chửng cả ngọn núi hoang vu."
        )

        res = sa.analyze_texts(["sample.txt"], [sample_text], profile_id="test_prof", scope="story")

        # Verify schema version
        self.assertEqual(res.get("schema_version"), "2.0.0")
        self.assertEqual(res.get("profile_id"), "test_prof")
        self.assertEqual(res.get("scope"), "story")

        # Axis 1: Syntax & Rhythm
        stats = res["fingerprint"]["stats"]
        self.assertIn("whitespace_syllables_count", stats)
        self.assertIn("avg_syllables_per_sentence", stats)

        # Axis 2: Sensory Immersion
        sensory = res["fingerprint"]["sensory_profile"]
        self.assertIn("primary_sense", sensory)
        self.assertIn("density_per_1000", sensory)

        # Axis 3: Content Ratios
        ratios = res["fingerprint"]["content_ratios"]
        self.assertIn("dialogue_ratio", ratios)
        self.assertIn("narrative_action_ratio", ratios)

        # Axis 4: Tone & Voice
        tone = res["fingerprint"]["tone_and_voice"]
        self.assertIn("descriptor", tone)
        self.assertIn("tone_confidence", tone)

        # Axis 5: Rhetoric & Lexicon
        rhetoric = res["fingerprint"]["rhetoric_and_lexicon"]
        self.assertIn("sample_reduplicatives", rhetoric)

        # Check scene variants and limitations
        self.assertIn("scene_variants", res)
        self.assertIn("confidence_and_limitations", res)

    def test_style_learn_single_file_and_folder(self):
        """Test learning from a single file and a directory via manage_story.py."""
        with isolated_workspace() as (ws, run_cli):
            run_cli("init", "--title", "Test Story", "--id", "test-story")

            # Create sample files in a directory
            samples_dir = os.path.join(ws, "samples")
            os.makedirs(samples_dir, exist_ok=True)
            f1 = os.path.join(samples_dir, "sample1.txt")
            with open(f1, "w", encoding="utf-8") as f:
                f.write("Tiếng mưa rơi lộp bộp trên mái hiên. Đêm nay lạnh buốt thấu xương. Hắn khẽ thở dài.")

            f2 = os.path.join(samples_dir, "sample2.md")
            with open(f2, "w", encoding="utf-8") as f:
                f.write("— Đứng lại! — Giọng quát vang lên như sấm sét giữa đêm vắng.")

            # Learn from folder
            res_learn = run_cli("style", "--learn", samples_dir, "--profile", "rain-style", "--scope", "story")
            self.assertEqual(res_learn.returncode, 0, f"Learn failed: {res_learn.stderr or res_learn.stdout}")

            # Verify profile files exist
            prof_dir = os.path.join(ws, "stories", "test-story", "summaries", "style_profiles", "rain-style")
            json_path = os.path.join(prof_dir, "style_profile.json")
            md_path = os.path.join(prof_dir, "STYLE_PROFILE.md")
            self.assertTrue(os.path.exists(json_path), "style_profile.json not found")
            self.assertTrue(os.path.exists(md_path), "STYLE_PROFILE.md not found")

            # Verify active profile pointer
            active_json = os.path.join(ws, "stories", "test-story", "summaries", "active_style_profile.json")
            with open(active_json, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertEqual(data.get("active_profile"), "rain-style")
            self.assertEqual(data.get("scope"), "story")

    def test_style_global_and_local_scope(self):
        """Test creating and listing global profiles vs story profiles."""
        with isolated_workspace() as (ws, run_cli):
            run_cli("init", "--title", "Test Story", "--id", "test-story")

            sample_file = os.path.join(ws, "global_sample.txt")
            with open(sample_file, "w", encoding="utf-8") as f:
                f.write("Gió thổi ào ào trên đỉnh núi tuyết. Ánh trăng rọi xuống mờ mờ ảo ảo.")

            # Learn as global
            res = run_cli("style", "--learn", sample_file, "--profile", "global-martial", "--scope", "global")
            self.assertEqual(res.returncode, 0, f"Global learn failed: {res.stderr or res.stdout}")

            global_dir = os.path.join(ws, "style_library", "global-martial")
            self.assertTrue(os.path.exists(os.path.join(global_dir, "style_profile.json")))

            # List profiles
            res_list = run_cli("style", "--list")
            self.assertIn("global-martial", res_list.stdout)


if __name__ == "__main__":
    unittest.main()
