# 0001. Native Markdown-First Architecture with Execution Tools

## Context
StoryFlow was originally designed around a terminal CLI workflow (`draft.md` with annotation headers like `/story-title`, followed by running `python manage_story.py save` which parsed the draft and copied prose to `chapters/chapter_XXXX.md`). In modern agent environments like Google Antigravity and Claude Code, agents have native tools (`read_file`, `write_file`, `edit_file`). Forcing the agent to route prose through `draft.md` creates unnecessary indirection, while writing directly to Markdown allows seamless human-AI collaboration. However, pure LLM prompting cannot reliably compute mathematical style statistics (Style Engine 2.0) or execute instant regex-based AI-slop checks (`vn_checker.py`).

## Decision
We adopt a **Hybrid Native Markdown-First Architecture**:
1. **Primary Interface**: All core creative artifacts are first-class Markdown files (`chapters/chapter_XXXX.md`, `outline.md`, `characters.md`, `STYLE_PROFILE.md`) directly readable and editable by both human authors and AI agents using native file tools.
2. **Execution Tools**: Python scripts (`scripts/narrative_memory.py`, `scripts/style_analyzer.py`, `scripts/vn_checker.py`, `manage_story.py`) remain available as deterministic execution tools for quantitative analysis, invariant auditing, regex slop filtering, and Web Dashboard serving.
3. **Dual Writing Paths**:
   - **Native Agent Path**: AI directly inspects context `.md` files and authors `chapters/chapter_XXXX.md`, running automated audits before finalization.
   - **CLI / Backward Compatibility Path**: `manage_story.py save`, `context`, `check`, and `memory` remain fully functional for terminal users and legacy workflows.
4. **Narrative Rules Invariance**: The 5-axis style decomposition, Show-Don't-Tell rules, 4-tier audit rubric, and Narrative Memory invariants remain strictly enforced across both paths.
