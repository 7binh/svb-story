#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
narrative_memory.py — Narrative Memory Engine for svb-story (Phase 2)
Provides deep continuity, canon provenance, dynamic character states,
knowledge & secret tracking, conflict detection, and layered context generation.
"""

import os
import sys
import json
import re
import datetime
from typing import Dict, List, Any, Optional, Tuple


# ─── ENUMS & CONSTANTS ────────────────────────────────────────────────────────

FACT_STATES = ["confirmed", "draft", "inferred", "disputed", "unresolved", "retracted"]
FACT_TYPES = ["world_truth", "character_belief", "character_deception"]
SECRET_STATUSES = ["concealed", "partially_revealed", "exposed"]
AUDIT_SEVERITIES = ["critical", "significant", "soft", "artistic_choice"]


def get_iso_timestamp() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")


def atomic_save_json(filepath: str, data: Any):
    """Safely saves data to JSON using temporary file and atomic replace."""
    os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
    tmp_path = f"{filepath}.tmp.{os.getpid()}_{int(datetime.datetime.now().timestamp()*1000)}"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    if os.path.exists(filepath):
        try:
            os.replace(tmp_path, filepath)
        except OSError:
            os.remove(filepath)
            os.replace(tmp_path, filepath)
    else:
        os.replace(tmp_path, filepath)


# ─── NARRATIVE MEMORY ENGINE ──────────────────────────────────────────────────

class NarrativeMemoryEngine:
    def __init__(self, memory_dir: str, chapters_dir: Optional[str] = None, story_id: Optional[str] = None):
        self.memory_dir = os.path.abspath(memory_dir)
        self.chapters_dir = os.path.abspath(chapters_dir) if chapters_dir else None
        self.story_id = story_id or "unknown_story"

        # File paths
        self.canon_file = os.path.join(self.memory_dir, "canon.json")
        self.events_file = os.path.join(self.memory_dir, "events.json")
        self.chars_file = os.path.join(self.memory_dir, "characters_state.json")
        self.knowledge_file = os.path.join(self.memory_dir, "knowledge.json")
        self.conflicts_file = os.path.join(self.memory_dir, "conflicts.json")

        self.canon: List[Dict[str, Any]] = []
        self.events: List[Dict[str, Any]] = []
        self.characters: Dict[str, Dict[str, Any]] = {}
        self.knowledge: Dict[str, Any] = {"secrets": [], "character_knowledge": {}}
        self.conflicts: List[Dict[str, Any]] = []

        self._ensure_initialized()
        self.load()

    def _ensure_initialized(self):
        """Creates directory and default files if not present."""
        os.makedirs(self.memory_dir, exist_ok=True)
        defaults = [
            (self.canon_file, []),
            (self.events_file, []),
            (self.chars_file, {}),
            (self.knowledge_file, {"secrets": [], "character_knowledge": {}}),
            (self.conflicts_file, [])
        ]
        for fpath, default_data in defaults:
            if not os.path.exists(fpath):
                atomic_save_json(fpath, default_data)

    def load(self):
        """Loads all memory databases."""
        try:
            with open(self.canon_file, "r", encoding="utf-8") as f:
                self.canon = json.load(f)
        except Exception:
            self.canon = []

        try:
            with open(self.events_file, "r", encoding="utf-8") as f:
                self.events = json.load(f)
        except Exception:
            self.events = []

        try:
            with open(self.chars_file, "r", encoding="utf-8") as f:
                self.characters = json.load(f)
        except Exception:
            self.characters = {}

        try:
            with open(self.knowledge_file, "r", encoding="utf-8") as f:
                self.knowledge = json.load(f)
        except Exception:
            self.knowledge = {"secrets": [], "character_knowledge": {}}

        try:
            with open(self.conflicts_file, "r", encoding="utf-8") as f:
                self.conflicts = json.load(f)
        except Exception:
            self.conflicts = []

    def save_all(self):
        """Persists all memory stores atomically and updates Markdown projections."""
        atomic_save_json(self.canon_file, self.canon)
        atomic_save_json(self.events_file, self.events)
        atomic_save_json(self.chars_file, self.characters)
        atomic_save_json(self.knowledge_file, self.knowledge)
        atomic_save_json(self.conflicts_file, self.conflicts)
        self.export_markdown_projections()

    def export_markdown_projections(self):
        """Generates clean, human-and-agent-readable Markdown summaries in summaries/ directory."""
        summaries_dir = os.path.dirname(self.memory_dir)
        os.makedirs(summaries_dir, exist_ok=True)

        # 1. characters.md
        chars_lines = ["# HỒ SƠ & TIẾN TRÌNH NHÂN VẬT (DYNAMIC CHARACTER STATES)\n"]
        if not self.characters:
            chars_lines.append("_Chưa có nhân vật nào được ghi nhận._\n")
        else:
            for c_name, c_state in sorted(self.characters.items()):
                curr_ch = c_state.get("current_chapter", 0)
                chars_lines.append(f"## {c_name} (Tiến trình: Chương {curr_ch})\n")
                goals = c_state.get("goals", {})
                if goals.get("primary"):
                    chars_lines.append(f"- **Mục tiêu chính**: {goals['primary']}")
                if goals.get("secondary"):
                    chars_lines.append(f"- **Mục tiêu phụ**: {goals['secondary']}")
                chars_lines.append(f"- **Tâm trạng hiện thời**: {c_state.get('emotional_state', 'Bình thường')}")

                phys = c_state.get("physical_state", {})
                injs = phys.get("injuries", [])
                inv = phys.get("inventory", [])
                loc = phys.get("location", "Chưa rõ")
                chars_lines.append(f"- **Vị trí**: {loc}")
                chars_lines.append(f"- **Chấn thương**: {', '.join(injs) if injs else 'Không có (khỏe mạnh)'}")
                chars_lines.append(f"- **Hành trang / Vật phẩm**: {', '.join(inv) if inv else 'Không có'}")

                rels = c_state.get("relationships", {})
                if rels:
                    chars_lines.append("- **Mối quan hệ**:")
                    for target, rel in rels.items():
                        chars_lines.append(f"  - Với `{target}`: {rel}")

                beliefs = c_state.get("beliefs", {})
                if beliefs:
                    chars_lines.append("- **Niềm tin & Nhận thức**:")
                    for b_title, b_data in beliefs.items():
                        is_wt = isinstance(b_data, dict) and b_data.get("is_world_truth")
                        tag = "Sự thật khách quan" if is_wt else "Chủ quan / Hiểu lầm"
                        chars_lines.append(f"  - {b_title} _[{tag}]_")

                shifts = c_state.get("notable_shifts", [])
                if shifts:
                    chars_lines.append("- **Biến chuyển tâm lý đáng chú ý**:")
                    for s in shifts:
                        chars_lines.append(f"  - [Ch.{s.get('chapter', '?')}]: {s.get('note', '')}")
                chars_lines.append("")

        chars_md_path = os.path.join(summaries_dir, "characters.md")
        with open(chars_md_path, "w", encoding="utf-8") as f:
            f.write("\n".join(chars_lines).strip() + "\n")

        # 2. timeline.md
        tl_lines = ["# TRỤC THỜI GIAN SỰ KIỆN NHÂN QUẢ (CAUSAL TIMELINE)\n"]
        if not self.events:
            tl_lines.append("_Chưa có sự kiện nào trong timeline._\n")
        else:
            for e in self.events:
                status_str = e.get("status", "confirmed").upper()
                tl_lines.append(f"### [Chương {e.get('chapter', 0)}] {e.get('title')} `[{status_str}]`")
                tl_lines.append(f"- **Tóm lược**: {e.get('summary')}")
                if e.get("relative_time"):
                    tl_lines.append(f"- **Mốc thời gian**: {e['relative_time']}")
                if e.get("characters_involved"):
                    tl_lines.append(f"- **Nhân vật tham gia**: {', '.join(e['characters_involved'])}")
                if e.get("lasting_changes"):
                    tl_lines.append("- **Hệ quả / Di chứng kéo dài**:")
                    for chg in e["lasting_changes"]:
                        tl_lines.append(f"  - {chg}")
                tl_lines.append("")

        tl_md_path = os.path.join(summaries_dir, "timeline.md")
        with open(tl_md_path, "w", encoding="utf-8") as f:
            f.write("\n".join(tl_lines).strip() + "\n")

        # 3. canon.md
        canon_lines = ["# CHÂN LÝ THẾ GIỚI & QUY TẮC BẤT BIẾN (STORY CANON)\n"]
        if not self.canon:
            canon_lines.append("_Chưa có dữ kiện Canon nào được ghi nhận._\n")
        else:
            for f_item in self.canon:
                prov = f_item.get("provenance", {})
                ch_str = f"Chương {prov.get('chapter')}" if prov.get("chapter") else "Khởi tạo"
                q_str = f' — _"{prov.get("quote")}"_' if prov.get("quote") else ""
                state_tag = f_item.get("state", "confirmed").upper()
                type_tag = f_item.get("fact_type", "world_truth")
                canon_lines.append(f"- **[{state_tag} | {type_tag}]** `{f_item.get('subject')}` {f_item.get('predicate')} **{f_item.get('object')}** ({ch_str}){q_str}")

        secrets = self.knowledge.get("secrets", [])
        if secrets:
            canon_lines.append("\n## DANH SÁCH BÍ MẬT & MA TRẬN NHẬN THỨC (SECRETS MATRIX)\n")
            for s in secrets:
                known_str = ", ".join(s.get("known_by", []))
                canon_lines.append(f"- **{s.get('title')}** `[{s.get('status', 'concealed').upper()}]`")
                canon_lines.append(f"  - Chủ sở hữu: `{s.get('owner')}` | Người biết: `{known_str}`")
                canon_lines.append(f"  - Tóm tắt: {s.get('summary')}")

        open_conflicts = self.get_open_conflicts()
        if open_conflicts:
            canon_lines.append("\n## TRANH CHẤP & MÂU THUẪN ĐANG MỞ (OPEN CONFLICTS)\n")
            for c in open_conflicts:
                canon_lines.append(f"- ⚠️ **{c.get('subject')}** `[{c.get('severity', 'critical').upper()}]`: {c.get('description')}")
                canon_lines.append(f"  - Nguồn A: Ch.{c.get('source_a', {}).get('chapter')} | Nguồn B: Ch.{c.get('source_b', {}).get('chapter')}")

        canon_md_path = os.path.join(summaries_dir, "canon.md")
        with open(canon_md_path, "w", encoding="utf-8") as f:
            f.write("\n".join(canon_lines).strip() + "\n")

    # ─── G1: CANON & PROVENANCE ───────────────────────────────────────────────

    def add_fact(
        self,
        subject: str,
        predicate: str,
        obj: str,
        fact_type: str = "world_truth",
        state: str = "confirmed",
        chapter: Optional[int] = None,
        quote: str = "",
        confidence: float = 1.0,
        believer_id: Optional[str] = None,
        accuracy: Optional[bool] = None,
        tags: Optional[List[str]] = None,
        fact_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Adds a fact with provenance and state. Ensures idempotency by updating matching facts."""
        if state not in FACT_STATES:
            state = "confirmed"
        if fact_type not in FACT_TYPES:
            fact_type = "world_truth"

        subject = subject.strip()
        predicate = predicate.strip()
        obj = obj.strip()

        # Idempotency check: see if exact subject-predicate-object exists
        existing = None
        for f in self.canon:
            if (f.get("subject", "").lower() == subject.lower() and
                f.get("predicate", "").lower() == predicate.lower() and
                f.get("object", "").lower() == obj.lower()):
                existing = f
                break

        now_str = get_iso_timestamp()
        if existing:
            existing["state"] = state
            existing["fact_type"] = fact_type
            if chapter is not None:
                existing["provenance"]["chapter"] = chapter
            if quote:
                existing["provenance"]["quote"] = quote
            existing["provenance"]["confidence"] = confidence
            existing["provenance"]["timestamp"] = now_str
            if believer_id:
                existing["believer_id"] = believer_id
            if accuracy is not None:
                existing["accuracy"] = accuracy
            if tags:
                existing["tags"] = list(set(existing.get("tags", []) + tags))
            atomic_save_json(self.canon_file, self.canon)
            self.export_markdown_projections()
            return existing

        fid = fact_id or f"fact_{len(self.canon) + 1:04d}"
        new_fact = {
            "fact_id": fid,
            "subject": subject,
            "predicate": predicate,
            "object": obj,
            "fact_type": fact_type,
            "state": state,
            "provenance": {
                "chapter": chapter,
                "quote": quote.strip(),
                "confidence": confidence,
                "timestamp": now_str
            },
            "believer_id": believer_id,
            "accuracy": accuracy,
            "tags": tags or []
        }
        self.canon.append(new_fact)
        atomic_save_json(self.canon_file, self.canon)
        self.export_markdown_projections()
        return new_fact

    def update_fact_state(self, fact_id: str, new_state: str, note: str = "") -> bool:
        if new_state not in FACT_STATES:
            return False
        for f in self.canon:
            if f.get("fact_id") == fact_id:
                f["state"] = new_state
                f["provenance"]["updated_at"] = get_iso_timestamp()
                if note:
                    f["state_note"] = note
                atomic_save_json(self.canon_file, self.canon)
                return True
        return False

    def query_facts(
        self,
        query: Optional[str] = None,
        subject: Optional[str] = None,
        state: Optional[str] = None,
        fact_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Queries facts matching criteria."""
        results = []
        q_lower = query.lower() if query else None
        s_lower = subject.lower() if subject else None

        for f in self.canon:
            if state and f.get("state") != state:
                continue
            if fact_type and f.get("fact_type") != fact_type:
                continue
            if s_lower and s_lower not in f.get("subject", "").lower():
                continue
            if q_lower:
                text_blob = f"{f.get('subject','')} {f.get('predicate','')} {f.get('object','')} {f.get('provenance',{}).get('quote','')}".lower()
                if q_lower not in text_blob:
                    continue
            results.append(f)
        return results

    # ─── G2: EVENT, TIMELINE & CHARACTER STATE ───────────────────────────────

    def add_event(
        self,
        chapter: int,
        title: str,
        summary: str,
        sequence_index: int = 1,
        relative_time: str = "",
        characters_involved: Optional[List[str]] = None,
        witnesses: Optional[List[str]] = None,
        cause_events: Optional[List[str]] = None,
        consequence_events: Optional[List[str]] = None,
        lasting_changes: Optional[List[str]] = None,
        status: str = "confirmed",
        event_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Adds an event to the causal event chain. Idempotent on chapter + title."""
        title = title.strip()
        summary = summary.strip()

        for e in self.events:
            if e.get("chapter") == chapter and e.get("title", "").lower() == title.lower():
                e["summary"] = summary
                e["relative_time"] = relative_time or e.get("relative_time", "")
                if characters_involved:
                    e["characters_involved"] = list(set(e.get("characters_involved", []) + characters_involved))
                if witnesses:
                    e["witnesses"] = list(set(e.get("witnesses", []) + witnesses))
                if cause_events:
                    e["cause_events"] = list(set(e.get("cause_events", []) + cause_events))
                if consequence_events:
                    e["consequence_events"] = list(set(e.get("consequence_events", []) + consequence_events))
                if lasting_changes:
                    e["lasting_changes"] = list(set(e.get("lasting_changes", []) + lasting_changes))
                e["status"] = status
                atomic_save_json(self.events_file, self.events)
                self.export_markdown_projections()
                return e

        eid = event_id or f"evt_ch{chapter:03d}_{len(self.events) + 1:02d}"
        new_event = {
            "event_id": eid,
            "chapter": chapter,
            "sequence_index": sequence_index,
            "title": title,
            "summary": summary,
            "relative_time": relative_time,
            "characters_involved": characters_involved or [],
            "witnesses": witnesses or [],
            "cause_events": cause_events or [],
            "consequence_events": consequence_events or [],
            "lasting_changes": lasting_changes or [],
            "status": status,
            "created_at": get_iso_timestamp()
        }
        self.events.append(new_event)
        # Sort events by chapter and sequence
        self.events.sort(key=lambda x: (x.get("chapter", 0), x.get("sequence_index", 0)))
        atomic_save_json(self.events_file, self.events)
        self.export_markdown_projections()
        return new_event

    def get_timeline(self, up_to_chapter: Optional[int] = None) -> List[Dict[str, Any]]:
        """Returns chronological event stream up to target chapter."""
        evs = self.events
        if up_to_chapter is not None:
            evs = [e for e in evs if e.get("chapter", 0) <= up_to_chapter]
        return sorted(evs, key=lambda x: (x.get("chapter", 0), x.get("sequence_index", 0)))

    def get_character_state(self, character_name: str) -> Dict[str, Any]:
        """Returns current dynamic character state or creates an empty one."""
        char_key = character_name.strip()
        if char_key not in self.characters:
            self.characters[char_key] = {
                "character_name": char_key,
                "current_chapter": 0,
                "goals": {"primary": "", "secondary": ""},
                "emotional_state": "Bình thường",
                "physical_state": {
                    "injuries": [],
                    "location": "Chưa xác định",
                    "inventory": []
                },
                "beliefs": {},
                "relationships": {},
                "notable_shifts": []
            }
        return self.characters[char_key]

    def update_character_state(
        self,
        character_name: str,
        chapter: int,
        goals: Optional[Dict[str, str]] = None,
        emotional_state: Optional[str] = None,
        injuries_add: Optional[List[str]] = None,
        injuries_remove: Optional[List[str]] = None,
        inventory_add: Optional[List[str]] = None,
        inventory_remove: Optional[List[str]] = None,
        location: Optional[str] = None,
        beliefs: Optional[Dict[str, Any]] = None,
        relationships: Optional[Dict[str, str]] = None,
        shift_note: Optional[str] = None
    ) -> Dict[str, Any]:
        """Updates a character's state dynamically."""
        state = self.get_character_state(character_name)
        state["current_chapter"] = max(state.get("current_chapter", 0), chapter)

        if goals:
            if "primary" in goals:
                state["goals"]["primary"] = goals["primary"]
            if "secondary" in goals:
                state["goals"]["secondary"] = goals["secondary"]

        if emotional_state:
            state["emotional_state"] = emotional_state

        phys = state.setdefault("physical_state", {"injuries": [], "location": "", "inventory": []})
        if injuries_add:
            for inj in injuries_add:
                inj_str = inj.strip()
                if inj_str and inj_str not in phys["injuries"]:
                    phys["injuries"].append(inj_str)
        if injuries_remove:
            for inj in injuries_remove:
                inj_str = inj.strip().lower()
                phys["injuries"] = [i for i in phys["injuries"] if inj_str not in i.lower()]

        if inventory_add:
            for item in inventory_add:
                item_str = item.strip()
                if item_str and item_str not in phys["inventory"]:
                    phys["inventory"].append(item_str)
        if inventory_remove:
            for item in inventory_remove:
                item_str = item.strip().lower()
                phys["inventory"] = [i for i in phys["inventory"] if item_str not in i.lower()]

        if location:
            phys["location"] = location

        if beliefs:
            state.setdefault("beliefs", {}).update(beliefs)

        if relationships:
            state.setdefault("relationships", {}).update(relationships)

        if shift_note:
            state.setdefault("notable_shifts", []).append({
                "chapter": chapter,
                "note": shift_note,
                "timestamp": get_iso_timestamp()
            })

        self.characters[character_name.strip()] = state
        atomic_save_json(self.chars_file, self.characters)
        self.export_markdown_projections()
        return state

    def transfer_item(self, item_name: str, from_char: str, to_char: str, chapter: int, reason: str = ""):
        """Transfers an item from one character to another, keeping inventory invariant."""
        item_clean = item_name.strip()
        self.update_character_state(from_char, chapter, inventory_remove=[item_clean])
        self.update_character_state(to_char, chapter, inventory_add=[item_clean])
        self.add_event(
            chapter=chapter,
            title=f"Chuyển giao vật phẩm: {item_clean}",
            summary=f"{from_char} đã trao/mất {item_clean} cho {to_char}. Lý do: {reason or 'Sự kiện cốt truyện'}",
            characters_involved=[from_char, to_char],
            lasting_changes=[f"{from_char} không còn giữ {item_clean}", f"{to_char} hiện đang sở hữu {item_clean}"]
        )

    # ─── G3: KNOWLEDGE, SECRETS & CONFLICTS ────────────────────────────────────

    def add_secret(
        self,
        title: str,
        summary: str,
        owner: str,
        known_by: Optional[List[str]] = None,
        reader_aware: bool = True,
        reveal_conditions: str = "",
        introduced_chapter: int = 1,
        secret_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Registers a secret and who is aware of it."""
        title = title.strip()
        summary = summary.strip()
        owner = owner.strip()
        known = [owner]
        if known_by:
            for k in known_by:
                k_clean = k.strip()
                if k_clean and k_clean not in known:
                    known.append(k_clean)

        secrets = self.knowledge.setdefault("secrets", [])
        for s in secrets:
            if s.get("title", "").lower() == title.lower():
                s["summary"] = summary
                s["owner"] = owner
                s["known_by"] = list(set(s.get("known_by", []) + known))
                s["reader_aware"] = reader_aware
                if reveal_conditions:
                    s["reveal_conditions"] = reveal_conditions
                atomic_save_json(self.knowledge_file, self.knowledge)
                self.export_markdown_projections()
                return s

        sid = secret_id or f"sec_{len(secrets) + 1:03d}"
        new_secret = {
            "secret_id": sid,
            "title": title,
            "summary": summary,
            "owner": owner,
            "known_by": known,
            "reader_aware": reader_aware,
            "reveal_conditions": reveal_conditions,
            "status": "concealed",
            "introduced_chapter": introduced_chapter,
            "created_at": get_iso_timestamp()
        }
        secrets.append(new_secret)
        atomic_save_json(self.knowledge_file, self.knowledge)
        self.export_markdown_projections()
        return new_secret

    def is_secret_known_by(self, secret_id_or_title: str, character_name: str) -> bool:
        """Checks if a character has knowledge of a secret."""
        c_name = character_name.strip().lower()
        for s in self.knowledge.get("secrets", []):
            if s.get("secret_id") == secret_id_or_title or s.get("title", "").lower() == secret_id_or_title.lower():
                known = [k.lower() for k in s.get("known_by", [])]
                return c_name in known
        return False

    def reveal_secret_to(self, secret_id_or_title: str, character_name: str, chapter: int, method: str = "direct"):
        """Reveals a secret to an additional character."""
        c_clean = character_name.strip()
        for s in self.knowledge.get("secrets", []):
            if s.get("secret_id") == secret_id_or_title or s.get("title", "").lower() == secret_id_or_title.lower():
                if c_clean not in s.get("known_by", []):
                    s.setdefault("known_by", []).append(c_clean)
                s["status"] = "partially_revealed"
                atomic_save_json(self.knowledge_file, self.knowledge)
                self.add_event(
                    chapter=chapter,
                    title=f"Tiết lộ bí mật: {s.get('title')}",
                    summary=f"{c_clean} đã biết được bí mật '{s.get('title')}' qua phương thức: {method}.",
                    characters_involved=[c_clean, s.get("owner", "")],
                    lasting_changes=[f"{c_clean} hiện đã biết bí mật '{s.get('title')}'"]
                )
                return True
        return False

    def record_conflict(
        self,
        subject: str,
        description: str,
        source_a: Dict[str, Any],
        source_b: Dict[str, Any],
        severity: str = "critical"
    ) -> Dict[str, Any]:
        """Records an explicit dispute/conflict between two sources without silent overwrite."""
        cid = f"conf_{len(self.conflicts) + 1:03d}"
        conflict = {
            "conflict_id": cid,
            "subject": subject.strip(),
            "description": description.strip(),
            "source_a": source_a,  # {'chapter': X, 'quote': '...'}
            "source_b": source_b,  # {'chapter': Y, 'quote': '...'}
            "severity": severity if severity in AUDIT_SEVERITIES else "critical",
            "status": "open",
            "created_at": get_iso_timestamp()
        }
        self.conflicts.append(conflict)
        atomic_save_json(self.conflicts_file, self.conflicts)
        self.export_markdown_projections()
        return conflict

    def get_open_conflicts(self) -> List[Dict[str, Any]]:
        return [c for c in self.conflicts if c.get("status") == "open"]

    def resolve_conflict(self, conflict_id: str, resolution_note: str) -> bool:
        for c in self.conflicts:
            if c.get("conflict_id") == conflict_id:
                c["status"] = "resolved"
                c["resolution_note"] = resolution_note
                c["resolved_at"] = get_iso_timestamp()
                atomic_save_json(self.conflicts_file, self.conflicts)
                self.export_markdown_projections()
                return True
        return False

    # ─── AUDIT INVARIANTS ─────────────────────────────────────────────────────

    def audit_continuity(self, target_chapter: int, draft_text: Optional[str] = None) -> List[Dict[str, Any]]:
        """Audits continuity invariants. Returns list of detected issues."""
        issues = []

        # 1. Open critical conflicts
        for conf in self.get_open_conflicts():
            issues.append({
                "severity": conf.get("severity", "critical"),
                "category": "conflict_dispute",
                "message": f"Mâu thuẫn chưa giải quyết: {conf.get('subject')} — {conf.get('description')}",
                "evidence": f"Chương {conf.get('source_a',{}).get('chapter')} vs Chương {conf.get('source_b',{}).get('chapter')}",
                "suggestion": "Xác minh lại chương gốc hoặc ghi chú giải thích trong diễn biến truyện."
            })

        # 2. Check draft text against secrets and injuries if text is provided
        if draft_text:
            # Check secrets: characters who don't know the secret shouldn't talk about it
            for s in self.knowledge.get("secrets", []):
                s_title = s.get("title", "")
                words = [re.escape(w) for w in re.findall(r"\w+", s_title) if len(w) >= 3]
                if not words:
                    continue
                match_terms = [re.escape(s_title)] + words
                term_pat = "|".join(match_terms)

                # Check if an uninformed character speaks of the secret
                # Uninformed characters are any known characters not in known_by
                uninformed = [c for c in self.characters.keys() if not self.is_secret_known_by(s.get("secret_id"), c)]
                for c in uninformed:
                    # Look for dialogue attributed to character containing secret terms
                    pat = rf'(?:{re.escape(c)}[^:\n"“]{{0,35}}[:,\s]+["“][^"”]*?(?:{term_pat})[^"”]*?["”])'
                    if re.search(pat, draft_text, re.IGNORECASE):
                        issues.append({
                            "severity": "critical",
                            "category": "secret_leak",
                            "message": f"Nhân vật '{c}' chưa biết bí mật '{s_title}' nhưng thoại nhắc tới chi tiết này!",
                            "evidence": f"Bí mật {s.get('secret_id')} chỉ dành cho: {', '.join(s.get('known_by', []))}",
                            "suggestion": f"Bỏ câu thoại nhắc đến bí mật hoặc bổ sung tình tiết {c} biết được bí mật trước."
                        })

            # Check unhealed injuries: character with injury in physical_state
            for c_name, c_state in self.characters.items():
                injuries = c_state.get("physical_state", {}).get("injuries", [])
                if injuries and c_name in draft_text:
                    # Check if character is performing actions inconsistent with injury
                    for inj in injuries:
                        if "tay phải" in inj.lower():
                            if re.search(rf'{c_name}\s+[^.\n]*\b(vung tay phải|cầm kiếm tay phải|đấm tay phải)\b', draft_text, re.IGNORECASE):
                                issues.append({
                                    "severity": "critical",
                                    "category": "injury_inconsistency",
                                    "message": f"Nhân vật '{c_name}' đang có chấn thương: '{inj}' nhưng văn bản miêu tả dùng tay phải bình thường!",
                                    "evidence": f"Chấn thương ghi nhận: {inj}",
                                    "suggestion": f"Miêu tả cơn đau nhói hoặc đổi sang dùng tay trái/cần người hỗ trợ."
                                })

            # Check item inventory: former owner using item after transfer
            for e in self.events:
                for change in e.get("lasting_changes", []):
                    m = re.match(r"(.+?)\s+không còn giữ\s+(.+)", change)
                    if m:
                        former_owner, item = m.group(1).strip(), m.group(2).strip()
                        pat = rf'(?:{re.escape(former_owner)}[^.\n]{{0,40}}?(?:rút ra|cầm|dùng|kích hoạt|vung|mang theo)\s+{re.escape(item)})'
                        if re.search(pat, draft_text, re.IGNORECASE):
                            issues.append({
                                "severity": "critical",
                                "category": "inventory_inconsistency",
                                "message": f"Nhân vật '{former_owner}' đã mất/chuyển giao '{item}' nhưng vẫn sử dụng trong bản thảo!",
                                "evidence": f"Biến cố tại Chương {e.get('chapter')}: {e.get('summary')}",
                                "suggestion": f"Kiểm tra lại người đang giữ '{item}' hoặc giải thích cách lấy lại vật phẩm."
                            })

        return issues

    # ─── G4: 5-LAYER CONTEXT BUILDER ──────────────────────────────────────────

    def build_5layer_context(
        self,
        target_chapter: int,
        target_goal: str = "",
        active_characters: Optional[List[str]] = None,
        style_profile_info: Optional[Dict[str, Any]] = None,
        recent_chapters_to_check: int = 1
    ) -> Dict[str, Any]:
        """Assembles the complete 5-Layer Context for writing a chapter."""
        chars = active_characters or []

        # Layer A — Core Context
        layer_a = {
            "target_chapter": target_chapter,
            "target_goal": target_goal or f"Phát triển cốt truyện Chương {target_chapter}",
            "story_id": self.story_id,
            "world_rules": [
                f["object"] for f in self.canon
                if f.get("fact_type") == "world_truth" and f.get("state") == "confirmed" and "luật" in f.get("tags", [])
            ][:5]
        }

        # Layer B — Relevant Story Memory
        relevant_events = [e for e in self.events if e.get("chapter", 0) < target_chapter][-5:]
        char_states = {}
        for c in chars:
            c_state = self.get_character_state(c)
            char_states[c] = {
                "goals": c_state.get("goals", {}),
                "emotional_state": c_state.get("emotional_state", ""),
                "injuries": c_state.get("physical_state", {}).get("injuries", []),
                "inventory": c_state.get("physical_state", {}).get("inventory", []),
                "location": c_state.get("physical_state", {}).get("location", ""),
                "beliefs": c_state.get("beliefs", {})
            }

        relevant_secrets = []
        for s in self.knowledge.get("secrets", []):
            # Include secret if any active character knows it OR if it's concealed
            known_in_scene = [c for c in chars if self.is_secret_known_by(s.get("secret_id"), c)]
            unaware_in_scene = [c for c in chars if not self.is_secret_known_by(s.get("secret_id"), c)]
            relevant_secrets.append({
                "secret_id": s.get("secret_id"),
                "title": s.get("title"),
                "summary": s.get("summary"),
                "known_by_in_scene": known_in_scene,
                "unaware_in_scene": unaware_in_scene,
                "status": s.get("status")
            })

        layer_b = {
            "relevant_events": relevant_events,
            "character_dynamic_states": char_states,
            "secrets_matrix": relevant_secrets
        }

        # Layer C — Source Evidence & Open Conflicts
        open_conflicts = self.get_open_conflicts()
        disputed_facts = [f for f in self.canon if f.get("state") == "disputed"]
        layer_c = {
            "open_conflicts": open_conflicts,
            "disputed_facts": disputed_facts
        }

        # Layer D — Style Context
        layer_d = {
            "active_profile": style_profile_info.get("profile_id") if style_profile_info else "none",
            "version": style_profile_info.get("version") if style_profile_info else "2.0.0",
            "guidelines": style_profile_info.get("context_guidance", []) if style_profile_info else [],
            "constraints": [
                "Ưu tiên giữ đúng tính cách và chấn thương của nhân vật.",
                "Không để nhân vật chưa biết bí mật nói ra chi tiết bí mật.",
                "Không đồng nhất nhịp câu giữa cảnh hành động và cảnh tâm lý."
            ]
        }

        # Layer E — Recent Context
        recent_meta = []
        prev_ch = target_chapter - 1
        if prev_ch > 0 and self.chapters_dir:
            prev_file = os.path.join(self.chapters_dir, f"chapter_{prev_ch:04d}.md")
            if os.path.exists(prev_file):
                try:
                    with open(prev_file, "r", encoding="utf-8") as pf:
                        p_lines = pf.readlines()
                    last_paragraphs = [l.strip() for l in p_lines[-15:] if l.strip()]
                    recent_meta.append({
                        "chapter": prev_ch,
                        "file": prev_file,
                        "ending_snip": "\n".join(last_paragraphs[-3:]) if last_paragraphs else ""
                    })
                except Exception:
                    pass

        layer_e = {
            "previous_chapter": prev_ch,
            "recent_snippets": recent_meta
        }

        return {
            "layer_a_core": layer_a,
            "layer_b_memory": layer_b,
            "layer_c_evidence": layer_c,
            "layer_d_style": layer_d,
            "layer_e_recent": layer_e
        }
