#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_narrative_memory.py — Unit tests for Narrative Memory Engine (Phase 2)
"""

import os
import sys
import tempfile
import unittest
import shutil

# Add parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import scripts.narrative_memory as nm


class TestNarrativeMemoryEngine(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.memory_dir = os.path.join(self.tmp_dir, "summaries", "memory")
        self.chapters_dir = os.path.join(self.tmp_dir, "chapters")
        os.makedirs(self.memory_dir, exist_ok=True)
        os.makedirs(self.chapters_dir, exist_ok=True)
        self.engine = nm.NarrativeMemoryEngine(self.memory_dir, self.chapters_dir, story_id="test_story")

    def tearDown(self):
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_fact_creation_and_provenance(self):
        """Test G1: Fact creation with provenance, state, and idempotency."""
        fact = self.engine.add_fact(
            subject="Dạ Lão",
            predicate="trạng_thái",
            obj="bị phong ấn trong Cổ Giới Chỉ",
            fact_type="world_truth",
            state="confirmed",
            chapter=1,
            quote="Linh hồn Dạ Lão thức tỉnh từ chiếc nhẫn đen.",
            confidence=0.98,
            tags=["dạ_lão", "nhẫn"]
        )
        self.assertEqual(fact["subject"], "Dạ Lão")
        self.assertEqual(fact["state"], "confirmed")
        self.assertEqual(fact["provenance"]["chapter"], 1)
        self.assertEqual(fact["provenance"]["quote"], "Linh hồn Dạ Lão thức tỉnh từ chiếc nhẫn đen.")

        # Idempotency: adding same subject-predicate-object updates existing fact without duplicate
        self.engine.add_fact(
            subject="Dạ Lão",
            predicate="trạng_thái",
            obj="bị phong ấn trong Cổ Giới Chỉ",
            confidence=1.0
        )
        self.assertEqual(len(self.engine.canon), 1)
        self.assertEqual(self.engine.canon[0]["provenance"]["confidence"], 1.0)

    def test_world_truth_vs_character_belief(self):
        """Test G1: Distinguish between objective world truth and subjective belief."""
        # Objective world truth: Liễu Thanh was killed by a beast, not by Lâm Phong
        self.engine.add_fact(
            subject="Liễu Thanh",
            predicate="nguyên_nhân_chết",
            obj="Bị Hắc Hổ giết",
            fact_type="world_truth",
            state="confirmed",
            chapter=3
        )
        # Subjective character belief: Liễu Tông chủ falsely believes Lâm Phong killed his son
        self.engine.add_fact(
            subject="Liễu Tông Chủ",
            predicate="tin_rằng",
            obj="Lâm Phong giết Liễu Thanh",
            fact_type="character_belief",
            state="confirmed",
            chapter=4,
            believer_id="Liễu Tông Chủ",
            accuracy=False
        )
        wt = self.engine.query_facts(fact_type="world_truth")
        cb = self.engine.query_facts(fact_type="character_belief")
        self.assertEqual(len(wt), 1)
        self.assertEqual(len(cb), 1)
        self.assertFalse(cb[0]["accuracy"])
        self.assertEqual(cb[0]["believer_id"], "Liễu Tông Chủ")

    def test_event_timeline_and_causality(self):
        """Test G2: Events chain and timeline ordering."""
        e1 = self.engine.add_event(
            chapter=1,
            title="Nhận được nhẫn",
            summary="Lâm Phong tìm thấy nhẫn đen ở đáy vách núi.",
            characters_involved=["Lâm Phong"]
        )
        e2 = self.engine.add_event(
            chapter=2,
            title="Thức tỉnh Dạ Lão",
            summary="Dạ Lão hiện hình và nhận Lâm Phong làm đệ tử.",
            characters_involved=["Lâm Phong", "Dạ Lão"],
            cause_events=[e1["event_id"]]
        )
        tl = self.engine.get_timeline()
        self.assertEqual(len(tl), 2)
        self.assertEqual(tl[0]["chapter"], 1)
        self.assertEqual(tl[1]["cause_events"], [e1["event_id"]])

    def test_dynamic_character_state_and_injury(self):
        """Test G2: Track injuries and inventory across chapters."""
        self.engine.update_character_state(
            character_name="Lâm Phong",
            chapter=2,
            goals={"primary": "Báo thù gia tộc"},
            emotional_state="Phẫn nộ",
            injuries_add=["Kinh mạch tay phải bị tổn thương"]
        )
        state = self.engine.get_character_state("Lâm Phong")
        self.assertIn("Kinh mạch tay phải bị tổn thương", state["physical_state"]["injuries"])

        # Healing injury
        self.engine.update_character_state(
            character_name="Lâm Phong",
            chapter=5,
            injuries_remove=["Kinh mạch tay phải"]
        )
        state2 = self.engine.get_character_state("Lâm Phong")
        self.assertEqual(len(state2["physical_state"]["injuries"]), 0)

    def test_item_transfer_invariance(self):
        """Test G2: Item transfer invariant between characters."""
        self.engine.update_character_state("Lâm Phong", 1, inventory_add=["Cổ Giới Chỉ", "Thanh Phong Kiếm"])
        self.engine.update_character_state("Tiêu Viêm", 1, inventory_add=["Dược Đỉnh"])

        # Lâm Phong transfers Thanh Phong Kiếm to Tiêu Viêm
        self.engine.transfer_item("Thanh Phong Kiếm", "Lâm Phong", "Tiêu Viêm", chapter=2, reason="Quà kết nghĩa")

        lp_state = self.engine.get_character_state("Lâm Phong")
        tv_state = self.engine.get_character_state("Tiêu Viêm")

        self.assertNotIn("Thanh Phong Kiếm", lp_state["physical_state"]["inventory"])
        self.assertIn("Thanh Phong Kiếm", tv_state["physical_state"]["inventory"])

    def test_knowledge_and_secret_containment(self):
        """Test G3: Secrets awareness and reveal controls."""
        sec = self.engine.add_secret(
            title="Thân thế Dạ Lão",
            summary="Dạ Lão là Bát Phẩm Luyện Dược Sư.",
            owner="Dạ Lão",
            known_by=["Lâm Phong"],
            introduced_chapter=1
        )
        self.assertTrue(self.engine.is_secret_known_by(sec["secret_id"], "Dạ Lão"))
        self.assertTrue(self.engine.is_secret_known_by(sec["secret_id"], "Lâm Phong"))
        self.assertFalse(self.engine.is_secret_known_by(sec["secret_id"], "Thanh Mai"))

        # Reveal secret to Thanh Mai at chapter 4
        self.engine.reveal_secret_to(sec["secret_id"], "Thanh Mai", chapter=4, method="Lâm Phong tiết lộ khi nguy cấp")
        self.assertTrue(self.engine.is_secret_known_by(sec["secret_id"], "Thanh Mai"))

    def test_conflict_recording_without_silent_overwrite(self):
        """Test G3: Conflict recorded as dispute rather than overwritten."""
        c = self.engine.record_conflict(
            subject="Ngày sinh của Lâm Phong",
            description="Chương 1 ghi mùa đông, Chương 5 ghi mùa hè",
            source_a={"chapter": 1, "quote": "Sinh ra giữa trời tuyết rơi trắng xóa"},
            source_b={"chapter": 5, "quote": "Ngày sinh nhật ve kêu râm ran mùa hạ"},
            severity="significant"
        )
        self.assertEqual(len(self.engine.get_open_conflicts()), 1)
        self.assertEqual(c["status"], "open")

        # Resolve conflict
        self.engine.resolve_conflict(c["conflict_id"], "Đính chính: Lâm Phong sinh mùa đông, mùa hạ là ngày được nhận nuôi.")
        self.assertEqual(len(self.engine.get_open_conflicts()), 0)

    def test_audit_continuity_invariants(self):
        """Test invariant audit for secret leaks and injuries."""
        self.engine.update_character_state(
            character_name="Lâm Phong",
            chapter=2,
            injuries_add=["Rạn nứt xương tay phải"]
        )
        self.engine.add_secret(
            title="Vạn Hóa Thần Quyết",
            summary="Bí kíp thượng cổ giấu dưới chân tượng Phật",
            owner="Dạ Lão",
            known_by=["Dạ Lão"]
        )

        # Draft where Lâm Phong uses injured right arm and speaks about secret he doesn't know
        bad_draft = (
            "Lâm Phong vung tay phải chém một kiếm kinh hoàng.\n"
            'Lâm Phong cười bảo: "Vạn Hóa Thần Quyết này quả nhiên lợi hại!"'
        )

        issues = self.engine.audit_continuity(target_chapter=3, draft_text=bad_draft)
        self.assertTrue(any(i["category"] == "injury_inconsistency" for i in issues))
        self.assertTrue(any(i["category"] == "secret_leak" for i in issues))

    def test_build_5layer_context(self):
        """Test G4: Layered context assembly."""
        self.engine.update_character_state("Lâm Phong", 1, goals={"primary": "Luyện kiếm"})
        self.engine.add_event(1, "Luyện kiếm thành công", "Đạt tầng thứ nhất.")

        ctx = self.engine.build_5layer_context(
            target_chapter=2,
            target_goal="Đột phá cảnh giới",
            active_characters=["Lâm Phong"],
            style_profile_info={"profile_id": "tien_hiep_co_dien", "version": "2.0.0", "context_guidance": ["Văn phong trang trọng"]}
        )
        self.assertIn("layer_a_core", ctx)
        self.assertIn("layer_b_memory", ctx)
        self.assertIn("layer_c_evidence", ctx)
        self.assertIn("layer_d_style", ctx)
        self.assertIn("layer_e_recent", ctx)
        self.assertEqual(ctx["layer_a_core"]["target_chapter"], 2)
        self.assertIn("Lâm Phong", ctx["layer_b_memory"]["character_dynamic_states"])


if __name__ == "__main__":
    unittest.main()
