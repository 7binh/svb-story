# SPEC: NATIVE MARKDOWN-FIRST NARRATIVE ARCHITECTURE
*Generated via `/matt-to-spec` for `svb-story` / `story-flow`*

## Problem Statement

Authors and modern AI agents operating in rich IDEs like Google Antigravity face friction when forced to interact exclusively through legacy command-line indirection. Specifically, drafting novel chapters required staging prose into a temporary `draft.md` with rigid annotation syntax (`/story-title`, `/story-brief`), then invoking shell scripts (`python manage_story.py save`) to extract, copy, and reset the file. This indirection breaks the natural conversational flow, limits direct human editing of Markdown files, and introduces failure points if shell environments differ. However, abandoning all scripts in favor of pure LLM prompting would sacrifice mathematical style metrics, zero-token regex slop detection, and atomic safety guarantees.

## Solution

Re-architect StoryFlow into a **Hybrid Native Markdown-First System**:
1. Human authors and AI agents can directly read and write first-class Markdown documents (`chapters/chapter_XXXX.md`, `outline.md`, `characters.md`, `STYLE_PROFILE.md`) using standard editor and agent file tools.
2. The 7-step narrative pipeline (`Understand` -> `Plan` -> `Retrieve 5-Layer Context` -> `Write Prose` -> `Audit 4-Tier` -> `Repair` -> `Finalize`) operates directly on the target Markdown files without mandatory `draft.md` indirection.
3. Python engines (`scripts/narrative_memory.py`, `scripts/vn_checker.py`, `scripts/style_analyzer.py`, `manage_story.py`) remain embedded as deterministic verification and analysis tools, callable on demand for rapid invariant audits and style enforcement.
4. Complete backward compatibility is maintained: `manage_story.py` CLI commands continue to work for users who prefer terminal shell scripting.
5. All deep analytical rules (5-axis style decomposition, Show-Don't-Tell sensorial depth, 4-tier audit rubric, Story Canon provenance, and dynamic character tracking) remain 100% active and uncompromised.

## User Stories

1. As a novelist in Antigravity, I want to open `chapters/chapter_0001.md` and edit my prose directly, so that I don't have to navigate a temporary draft staging buffer.
2. As an AI writing agent, I want to read `outline.md` and `characters.md` directly using `read_file`, so that I can inspect story background without shell command overhead.
3. As an AI writing agent, I want to write completed chapters directly to `chapters/chapter_XXXX.md` using `write_file`, so that the chapter is immediately available in the user's workspace.
4. As a novelist, I want an automatic draft backup to be created before any chapter is updated or overwritten, so that I never lose previously written text.
5. As an AI writing agent, I want to run `python manage_story.py check` to verify Vietnamese typography and detect AI-slop in milliseconds, so that I don't waste LLM tokens on repetitive string scanning.
6. As an AI writing agent, I want to execute `python manage_story.py memory --audit` on a freshly written chapter, so that I catch continuity invariants (unhealed injuries, item disappearance, secret leaks) before presenting the chapter to the user.
7. As a novelist, I want character dynamic states (injuries, inventory, emotional shifts) to be readable in plain Markdown (`summaries/characters.md`), so that I can inspect my cast at a glance without reading raw JSON.
8. As a novelist, I want to update character profiles or world lore by simply editing Markdown files, so that I don't have to remember CLI command flags.
9. As an AI writing agent, I want `manage_story.py` to synchronize between Markdown views (`characters.md`, `canon.md`) and JSON indices (`characters_state.json`, `canon.json`), so that human legibility and machine query speed coexist seamlessly.
10. As a novelist, I want the 5-axis style engine to analyze sample texts and generate a clear, human-readable `STYLE_PROFILE.md`, so that both the AI and I know the exact cadence and sensory targets.
11. As an AI writing agent, I want the Style Enforcement Pipeline to adjust sentence cadence based on scene type (action vs dialogue) without flattening prose into rigid uniformity.
12. As a novelist, I want the 4-tier audit rubric to categorize feedback into Critical, Significant, Soft, and Artistic Choice, so that my intentional stylistic choices are never ruined by mechanical over-correction.
13. As an author who prefers CLI scripting, I want `manage_story.py save`, `context`, `outline`, and `foreshadow` to remain fully supported, so that my existing habits and scripts don't break.
14. As a novelist, I want `manage_story.py status` and `manage_story.py list` to accurately reflect all chapters created whether by direct Markdown writing or by CLI commands.
15. As an AI writing agent, I want `story-write` instructions to guide me through scene planning (POV, conflict, secrets, pacing) before drafting prose, so that chapter quality remains consistently high.
16. As an AI writing agent, I want `story-flow` to autonomously execute the 7-step pipeline from goal to final chapter while pausing for human input on critical plot divergences.
17. As a novelist, I want secrets and spoilers to remain strictly contained to characters who have witnessed or been told the information, so that dramatic tension is preserved.
18. As a novelist, I want the Web Dashboard to display the chapter tree and narrative timeline regardless of how chapters were authored.
19. As a novelist, I want `GLOSSARY.md` and architectural ADRs to define the canonical terms of the codebase, so that future agents and collaborators use consistent vocabulary.
20. As a novelist, I want zero data loss guarantees: any interrupted save or syntax error must leave the manuscript untouched.

## Implementation Decisions

### Architectural Seams
- **Human-Agent Seam (Markdown-First)**:
  - All creative inputs and outputs reside in standard Markdown: `chapters/chapter_XXXX.md`, `summaries/outline.md`, `summaries/characters.md`, `summaries/lorebook.md`, `summaries/foreshadow.md`, and `style_library/<id>/STYLE_PROFILE.md`.
  - The agent interacts with these files using native tools (`read_file`, `write_file`, `edit_file`).
- **Verification & Analysis Seam (Execution Tools)**:
  - Python scripts (`scripts/narrative_memory.py`, `scripts/vn_checker.py`, `scripts/style_analyzer.py`) act as fast, deterministic subprocess tools invoked via `run_command` (prefixed with `rtk`).
  - `manage_story.py` exposes these verification capabilities through `manage_story.py check`, `manage_story.py memory --audit`, and `manage_story.py style`.
- **Synchronization Seam**:
  - `manage_story.py` provides bidirectional bridging: when `manage_story.py memory` or `save` runs, it updates both the machine-fast JSON database (`summaries/memory/*.json`) and generates human-friendly Markdown projections (`summaries/characters.md`, `summaries/timeline.md`).

### Schema & Invariant Contracts
- All 10 regression scenarios defined in Phase 2 remain strict invariants:
  1. Unhealed injury continuity.
  2. Item transfer conservation.
  3. Secret access containment.
  4. World truth vs character belief separation.
  5. Causal timeline precedence.
  6. Evidentiary dispute preservation.
  7. Long-range dormant clue retrieval.
  8. Catalyst-driven attitude shifts.
  9. Adaptive style across scene types.
  10. Canon isolation upon save failure.

## Testing Decisions

### What Makes a Good Test
- Tests must verify external observable behavior (file contents, exit codes, invariant violation detection), not private scratch variables.
- All tests must run in isolated temporary directories (`tempfile.mkdtemp`) without network access or mutating user stories.
- Both direct Markdown authoring and legacy CLI paths must be verified.

### Modules Tested
1. `tests/test_p0_data_integrity.py`: Atomic write safety, check command error reporting.
2. `tests/test_style_engine.py`: 5-axis style decomposition, multi-profile scoping.
3. `tests/test_skills_integrity.py`: 10 skills frontmatter, triggers, and absence of ghost commands.
4. `tests/test_narrative_memory.py`: Canon provenance, knowledge matrix, dynamic character states.
5. `tests/test_long_novel_regression.py`: 10-scenario multi-chapter novel regression suite.
6. `tests/test_full_regression.py`: End-to-end CLI regression baseline.

## Out of Scope
- Eliminating Python altogether: quantitative metric analysis (syllable frequency, standard deviation) and fast regex slop scanning require Python.
- Replacing the Web Dashboard server: Node.js/Python server remains necessary for local HTTP browser rendering.

## Further Notes
- This architecture bridges the gap between terminal CLI conventions and modern AI-first workspace environments.
