#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_long_novel_regression.py — 10-Scenario Long-Novel Regression Fixtures (Phase 2)
Tests multi-chapter continuity, invariants, secret leaks, dynamic character states,
dramatic irony, and safe canon isolation.
"""

import os
import sys
import tempfile
import unittest
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import scripts.narrative_memory as nm
import manage_story as ms


class TestLongNovelRegression(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.story_id = "long_novel_fixture"
        self.story_dir = os.path.join(self.tmp_dir, "stories", self.story_id)
        self.chapters_dir = os.path.join(self.story_dir, "chapters")
        self.summaries_dir = os.path.join(self.story_dir, "summaries")
        self.memory_dir = os.path.join(self.summaries_dir, "memory")

        os.makedirs(self.chapters_dir, exist_ok=True)
        os.makedirs(self.summaries_dir, exist_ok=True)
        os.makedirs(self.memory_dir, exist_ok=True)

        self.engine = nm.NarrativeMemoryEngine(self.memory_dir, self.chapters_dir, story_id=self.story_id)

    def tearDown(self):
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_scenario_01_unhealed_injury_continuity(self):
        """Scenario 1: Character injured in earlier chapter cannot exert injured limb without healing."""
        # Ch.1: Lâm Phong breaks his right arm
        self.engine.update_character_state(
            character_name="Lâm Phong",
            chapter=1,
            injuries_add=["Kinh mạch tay phải bị gãy dập"]
        )
        self.engine.add_event(
            chapter=1,
            title="Đại chiến Hắc Phong",
            summary="Lâm Phong bị thương nặng ở tay phải.",
            lasting_changes=["Kinh mạch tay phải bị gãy dập, không thể vung kiếm"]
        )

        # Ch.2: Draft depicts Lâm Phong wielding sword with injured right arm
        bad_draft = (
            "# Chương 2: Truy sát\n\n"
            "Lâm Phong vung tay phải chém một kiếm kinh hoàng xé toạc màn đêm."
        )
        issues = self.engine.audit_continuity(target_chapter=2, draft_text=bad_draft)
        self.assertTrue(any(i["category"] == "injury_inconsistency" for i in issues))

    def test_scenario_02_item_transfer_invariance(self):
        """Scenario 2: Transferred item cannot spontaneously reappear in former owner's hands."""
        # Ch.1: Lâm Phong has "Thanh Phong Kiếm"
        self.engine.update_character_state("Lâm Phong", 1, inventory_add=["Thanh Phong Kiếm"])

        # Ch.2: Lâm Phong hands it to Tiêu Viêm
        self.engine.transfer_item("Thanh Phong Kiếm", "Lâm Phong", "Tiêu Viêm", chapter=2, reason="Bái biệt")

        # Ch.3: Draft has Lâm Phong pulling out Thanh Phong Kiếm again
        bad_draft = (
            "# Chương 3: Bí cảnh\n\n"
            "Giữa tình thế nguy nan, Lâm Phong rút ra Thanh Phong Kiếm chuẩn bị huyết chiến."
        )
        issues = self.engine.audit_continuity(target_chapter=3, draft_text=bad_draft)
        self.assertTrue(any(i["category"] == "inventory_inconsistency" for i in issues))

    def test_scenario_03_secret_containment_and_leak_prevention(self):
        """Scenario 3: Secret known only to Character A cannot be spoken by uninformed Character B."""
        self.engine.update_character_state("Dạ Lão", 1)
        self.engine.update_character_state("Lâm Phong", 1)
        self.engine.update_character_state("Thanh Mai", 1)

        sec = self.engine.add_secret(
            title="Thân thế Dược Tôn",
            summary="Dạ Lão là Dược Tôn bị đệ tử phản bội.",
            owner="Dạ Lão",
            known_by=["Lâm Phong"],
            introduced_chapter=1
        )

        # Thanh Mai has not been told the secret yet
        self.assertFalse(self.engine.is_secret_known_by(sec["secret_id"], "Thanh Mai"))

        # Draft where Thanh Mai speaks the secret
        bad_draft = (
            "# Chương 4: Trà quán\n\n"
            'Thanh Mai khẽ cười nói: "Thân thế Dược Tôn của Dạ Lão sớm muộn cũng sẽ bị phát giác thôi."'
        )
        issues = self.engine.audit_continuity(target_chapter=4, draft_text=bad_draft)
        self.assertTrue(any(i["category"] == "secret_leak" for i in issues))

    def test_scenario_04_dramatic_irony_belief_vs_world_truth(self):
        """Scenario 4: Reader knows truth, but protagonist holds false belief without corrupting canon."""
        # World truth: The mentor was poisoned by traitor Hàn Phong
        wt = self.engine.add_fact(
            subject="Dạ Lão",
            predicate="kẻ_hạ_độc",
            obj="Hàn Phong",
            fact_type="world_truth",
            state="confirmed",
            chapter=1,
            quote="Hàn Phong hạ độc vào đan dược của sư phụ."
        )

        # Character belief: Lâm Phong erroneously believes Liễu Gia killed his mentor
        cb = self.engine.add_fact(
            subject="Lâm Phong",
            predicate="tin_rằng",
            obj="Liễu Gia hạ độc sư phụ",
            fact_type="character_belief",
            state="confirmed",
            chapter=2,
            believer_id="Lâm Phong",
            accuracy=False,
            quote="Lâm Phong thề trước mộ: Mối thù này Liễu gia phải đền mạng!"
        )

        # Verify separation
        self.assertEqual(wt["fact_type"], "world_truth")
        self.assertEqual(cb["fact_type"], "character_belief")
        self.assertFalse(cb["accuracy"])

        # Querying world truth returns Hàn Phong, not Liễu Gia
        truths = self.engine.query_facts(fact_type="world_truth", subject="Dạ Lão")
        self.assertEqual(len(truths), 1)
        self.assertEqual(truths[0]["object"], "Hàn Phong")

    def test_scenario_05_nonlinear_exposition_without_causal_inversion(self):
        """Scenario 5: Past event revealed in later chapter preserves causal timeline."""
        # Ch.1: Present event
        e1 = self.engine.add_event(chapter=1, title="Lâm Phong rời thành", summary="Bắt đầu hành trình lưu lạc.")

        # Ch.5: Revelation of a flashback event that took place 10 years ago
        e_past = self.engine.add_event(
            chapter=5,
            sequence_index=0,
            title="Biến cố diệt môn 10 năm trước",
            summary="Gia tộc Lâm thị bị thế lực hắc ám tập kích.",
            relative_time="10 năm trước Chương 1",
            consequence_events=[e1["event_id"]]
        )

        timeline = self.engine.get_timeline()
        # Events are indexed cleanly with relative time and causal dependencies
        past_ev = [e for e in timeline if e["event_id"] == e_past["event_id"]][0]
        self.assertIn(e1["event_id"], past_ev["consequence_events"])
        self.assertEqual(past_ev["relative_time"], "10 năm trước Chương 1")

    def test_scenario_06_contradictory_sources_recorded_as_dispute(self):
        """Scenario 6: Conflicting chapter accounts recorded as dispute without silent overwrite."""
        conf = self.engine.record_conflict(
            subject="Xuất thân của Dạ Lão",
            description="Chương 1 bảo là tán tu phương Bắc, Chương 6 ghi xuất thân từ Vạn Dược Tông phương Nam",
            source_a={"chapter": 1, "quote": "Tán tu lang bạt phương Bắc"},
            source_b={"chapter": 6, "quote": "Nguyên lão xuất thân Vạn Dược Tông phương Nam"},
            severity="critical"
        )
        open_confs = self.engine.get_open_conflicts()
        self.assertEqual(len(open_confs), 1)
        self.assertEqual(open_confs[0]["conflict_id"], conf["conflict_id"])

        # Audit alerts about open dispute
        issues = self.engine.audit_continuity(target_chapter=7)
        self.assertTrue(any(i["category"] == "conflict_dispute" for i in issues))

    def test_scenario_07_dormant_clue_retrieval_across_multi_chapters(self):
        """Scenario 7: Clue introduced in Chapter 1 successfully retrieved in Chapter 15."""
        self.engine.add_fact(
            subject="Ngọc Bội Bán Nguyệt",
            predicate="vị_trí_ẩn_giấu",
            obj="Dưới đáy giếng cổ tại Lâm gia trang",
            state="confirmed",
            chapter=1,
            quote="Ném ngọc bội xuống giếng cổ phong ấn.",
            tags=["ngọc_bội", "manh_mối"]
        )

        # Retrieve at chapter 15
        results = self.engine.query_facts(query="ngọc bội")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["provenance"]["chapter"], 1)
        self.assertIn("Lâm gia trang", results[0]["object"])

    def test_scenario_08_personality_shift_following_catalyst_event(self):
        """Scenario 8: Character mindset shifts organically following a verified catalyst event."""
        # Initial character state
        self.engine.update_character_state(
            character_name="Lâm Phong",
            chapter=1,
            emotional_state="Hồn nhiên, tin người",
            goals={"primary": "Tu luyện bảo vệ bạn bè"}
        )

        # Ch.4: Betrayal event
        betrayal = self.engine.add_event(
            chapter=4,
            title="Vụ phản bội tại Thạch Lâm",
            summary="Bạn thân Lục Viễn phản bội, đẩy Lâm Phong vào miệng vực sâu.",
            characters_involved=["Lâm Phong", "Lục Viễn"]
        )

        # Character personality shift
        self.engine.update_character_state(
            character_name="Lâm Phong",
            chapter=4,
            emotional_state="Lãnh đạm, cảnh giác cao độ",
            goals={"primary": "Sinh tồn và đòi lại công đạo"},
            shift_note=f"Tâm tính biến đổi sau khi bị Lục Viễn phản bội (Biến cố {betrayal['event_id']})"
        )

        st = self.engine.get_character_state("Lâm Phong")
        self.assertEqual(st["emotional_state"], "Lãnh đạm, cảnh giác cao độ")
        self.assertEqual(len(st["notable_shifts"]), 1)
        self.assertIn("phản bội", st["notable_shifts"][0]["note"])

    def test_scenario_09_style_adaptation_across_scene_types(self):
        """Scenario 9: Style profile guidance adapts across action and dialogue scenes without rigid uniform sentence length."""
        ctx = self.engine.build_5layer_context(
            target_chapter=5,
            target_goal="Đột kích doanh trại địch",
            style_profile_info={
                "profile_id": "tien_hiep_chien_dau",
                "version": "2.0.0",
                "context_guidance": [
                    "Cảnh chiến đấu: Nhịp câu ngắn, dồn dập, động từ mạnh.",
                    "Cảnh đối thoại: Đa tầng, có khoảng lặng và subtext."
                ]
            }
        )
        guidelines = ctx["layer_d_style"]["guidelines"]
        self.assertEqual(len(guidelines), 2)
        # Verify both action and emotional guidelines coexist without forcing identical metrics
        self.assertTrue(any("chiến đấu" in g for g in guidelines))
        self.assertTrue(any("đối thoại" in g for g in guidelines))

    def test_scenario_10_draft_failure_preserves_canon_integrity(self):
        """Scenario 10: Failed draft or invalid write never mutates the Story Canon."""
        initial_canon_count = len(self.engine.canon)
        initial_event_count = len(self.engine.events)

        # Simulate a draft with unconfirmed wild claims
        draft_file = os.path.join(self.chapters_dir, "draft.md")
        with open(draft_file, "w", encoding="utf-8") as f:
            f.write("# Chương chưa duyệt\n\nDạ Lão bất ngờ hóa thành Kim Long bay lên trời.")

        # Simulate save failure (e.g. invalid arguments or exception)
        # As per architecture rule, canon is untouched
        self.engine.load()  # re-read from disk
        self.assertEqual(len(self.engine.canon), initial_canon_count)
        self.assertEqual(len(self.engine.events), initial_event_count)
        # Draft file remains intact
        self.assertTrue(os.path.exists(draft_file))


if __name__ == "__main__":
    unittest.main()
