import os
import re
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_DIR = os.path.join(REPO_ROOT, "skills")
REFERENCES_DIR = os.path.join(REPO_ROOT, "references")


class TestSkillsIntegrity(unittest.TestCase):

    def test_all_skills_have_valid_frontmatter_and_exist(self):
        expected_skills = [
            "story",
            "story-write",
            "story-study",
            "story-outline",
            "story-deslop",
            "story-review",
            "story-cover",
            "story-import",
            "story-flow",
            "story-setup"
        ]

        for skill_name in expected_skills:
            skill_path = os.path.join(SKILLS_DIR, skill_name, "SKILL.md")
            self.assertTrue(os.path.exists(skill_path), f"Missing skill file: {skill_path}")

            with open(skill_path, "r", encoding="utf-8") as f:
                content = f.read()

            self.assertTrue(content.startswith("---"), f"{skill_name} does not start with YAML frontmatter")
            parts = content.split("---", 2)
            self.assertGreaterEqual(len(parts), 3, f"{skill_name} YAML frontmatter not closed properly")

            frontmatter = parts[1]
            self.assertIn(f"name: {skill_name}", frontmatter)
            self.assertIn("description:", frontmatter)

    def test_distinct_triggers_between_story_write_and_story_flow(self):
        """Ensure /story-write and /story-flow have separated, non-conflicting primary triggers."""
        write_path = os.path.join(SKILLS_DIR, "story-write", "SKILL.md")
        flow_path = os.path.join(SKILLS_DIR, "story-flow", "SKILL.md")

        with open(write_path, "r", encoding="utf-8") as f:
            write_content = f.read()
        with open(flow_path, "r", encoding="utf-8") as f:
            flow_content = f.read()

        # story-write owns /story-write
        self.assertIn("/story-write", write_content)

        # story-flow must NOT register /story-write as its main trigger in frontmatter
        flow_fm = flow_content.split("---")[1]
        self.assertNotIn("/story-write", flow_fm, "story-flow frontmatter should not claim /story-write trigger")

    def test_no_ghost_commands_in_skills(self):
        """Verify that ghost command /story-scan does not appear in any skill file."""
        for root, _, files in os.walk(SKILLS_DIR):
            for file in files:
                if file.endswith(".md"):
                    fp = os.path.join(root, file)
                    with open(fp, "r", encoding="utf-8") as f:
                        text = f.read()
                    self.assertNotIn("/story-scan", text, f"Found ghost command /story-scan in {fp}")


if __name__ == "__main__":
    unittest.main()
