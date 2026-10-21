# SPEC: NARRATIVE MEMORY ENGINE & LONG-FORM FICTION ARCHITECTURE
*Generated via `/matt-to-spec` for `svb-story` / `story-flow`*

## Problem Statement

When writing multi-chapter long-form novels, AI language models suffer from rapid contextual amnesia, timeline drift, character trait flattening, and secret leaks. Currently, `svb-story` relies primarily on static files (`character_bible.json`, `lorebook.json`, `rolling_summary.txt`) and short-term window history. This leads to critical continuity failures:
1. Characters act upon secrets they have no logical means of knowing (omniscient leakage).
2. Physical injuries or item transfers established in earlier chapters vanish without narrative cause in subsequent chapters.
3. Subjective character beliefs or outright lies are accidentally canonized into objective world truths.
4. Draft iterations or failed saves risk polluting or mutating official narrative memory.
5. Summaries drift away from actual chapter prose, losing verifiable evidence (provenance).

## Solution

Build the **Narrative Memory Engine**, a multi-tiered, verifiable memory and continuity system for `svb-story`. The engine provides:
- A definitive **Story Canon** with explicit states (`confirmed`, `draft`, `inferred`, `disputed`, `unresolved`, `retracted`) and textual provenance (chapter, quote, confidence).
- Clear separation between **World Truth** and **Character Belief**.
- **Dynamic Character State Tracking** (tracking physical injuries, held inventory, active goals, shifting emotional states, and relationships over time).
- A **Knowledge & Secret Tracking Matrix** preventing premature information disclosure and omniscient character behavior.
- A **5-Layer Context Builder** (`Core Context`, `Relevant Story Memory`, `Source Evidence`, `Style Context`, `Recent Context`) powering `manage_story.py context`.
- Pre-save narrative continuity audit preventing logical contradictions before chapters are canonized.
- CLI inspection tooling (`python manage_story.py memory`) allowing authors and agents to query facts, timeline, secrets, and audit report.

## User Stories

1. As a novelist, I want each recorded story fact to track its source chapter and quote, so that I can always verify where a detail originated.
2. As a novelist, I want the system to distinguish between objective world truth and a character's mistaken belief, so that misunderstandings and dramatic irony do not break the world's continuity.
3. As a novelist, I want to track physical injuries sustained by characters across chapters, so that characters do not miraculously recover in the next scene without medical care or time lapse.
4. As a novelist, I want to track items and weapons held by characters, so that an item given away or lost does not spontaneously reappear in the original owner's hands.
5. As an AI writing agent, I want to know who is aware of a specific secret before drafting a scene, so that I do not accidentally make an uninformed character reveal or react to that secret.
6. As a novelist, I want to define release conditions or milestones for plot secrets, so that the AI holds back critical reveals until the intended chapter or narrative arc.
7. As an AI writing agent, I want the system to supply relevant past events based on the characters and themes in the current chapter, so that I do not rely solely on the immediate previous chapter.
8. As a novelist, I want unconfirmed draft ideas to remain in a `draft` or `inferred` state, so that unapproved text never silently mutates the story canon.
9. As an AI writing agent, I want a multi-chapter timeline that preserves causal dependencies, so that future plot developments do not contradict earlier chronological milestones.
10. As a novelist, I want conflicts between two chapter sources to be flagged as `disputed` rather than silently overwritten, so that I can deliberately decide which version is true.
11. As a novelist, I want to audit a draft against canon invariants before saving, so that logical blunders are caught and highlighted before they become permanent.
12. As a novelist, I want character emotional states and motivations to update in response to specific catalyst events, so that character arcs feel organic rather than frozen or arbitrary.
13. As an AI writing agent, I want `manage_story.py context` to output a structured 5-layer briefing, so that I have complete situational, stylistic, and continuity awareness before writing prose.
14. As an author running CLI commands, I want `python manage_story.py memory --query <keyword>` to search for all canon facts and quotes related to that keyword, so that I can quickly recall past details without opening every chapter file.
15. As an author running CLI commands, I want `python manage_story.py memory --audit` to output any open disputes, broken dependencies, or unrecovered injuries, so that I can keep my manuscript clean.
16. As an author running CLI commands, I want `python manage_story.py memory --timeline` to display the chronological progression of major events, so that I maintain clear pacing.
17. As an author running CLI commands, I want `python manage_story.py memory --character <name>` to view a character's dynamic status at the current chapter, so that I write them with accurate physical and emotional constraints.
18. As a novelist, I want memory files to be safely saved using atomic writes and JSON validation, so that partial writes or unexpected crashes never corrupt the narrative database.
19. As a novelist, I want backward compatibility with existing `character_bible.json`, `lorebook.json`, and `foreshadow.json`, so that existing projects continue to function without data migration loss.
20. As an AI writing agent, I want the system to categorize audit feedback into Critical, Significant, Soft, and Artistic Choice, so that creative prose is not stripped away by mechanical over-correction.

## Implementation Decisions

### Architectural Seams
- **Core Memory Module**: A standalone Python standard library module `scripts/narrative_memory.py` encapsulating state models, persistence, provenance validation, query execution, conflict detection, and context assembly.
- **CLI Seam**: `manage_story.py` integrates `narrative_memory.py` by:
  - Extending `get_paths()` with memory directory and file locations (`summaries/memory/`).
  - Upgrading `action_context()` to assemble the 5-layer briefing.
  - Adding `action_memory(args)` for inspection, querying, auditing, and maintenance.
  - Hooking into `save_chapter_data()` to trigger idempotent memory updates upon successful chapter save.
- **Skill Seams**:
  - `skills/story/SKILL.md`: Routes memory commands.
  - `skills/story-write/SKILL.md` & `skills/story-flow/SKILL.md`: Standardize on the 7-step Plan → Retrieve → Write → Audit → Repair → Save → Update pipeline.
  - `skills/story-review/SKILL.md`: Incorporates the 4-tier audit rubric.
  - `skills/story-outline/SKILL.md`: Connects plot branches and foreshadowing to event memory.

### Schemas & State Enums
- `FactState`: `confirmed`, `draft`, `inferred`, `disputed`, `unresolved`, `retracted`.
- `FactType`: `world_truth`, `character_belief`, `character_deception`.
- `SecretStatus`: `concealed`, `partially_revealed`, `exposed`.
- Memory storage layout under `stories/<story_id>/summaries/memory/`:
  - `canon.json`: Array of Facts with provenance (`chapter`, `quote`, `confidence`, `timestamp`).
  - `events.json`: Array of Events with causality (`cause_events`, `consequence_events`, `lasting_changes`, `witnesses`).
  - `characters_state.json`: Dynamic character state mapped by character name.
  - `knowledge.json`: Secrets and character-knowledge associations.
  - `conflicts.json`: Log of open disputes with dual citations.

## Testing Decisions

### What Makes a Good Test
- Tests must verify external behavior and invariants, not internal scratch variables.
- Tests must run offline without external dependencies or network access.
- Tests must use isolated temporary workspaces (`tempfile.TemporaryDirectory`) and never mutate real user stories.
- Tests must verify that failures preserve drafts and do not promote unverified drafts to canon.

### Modules Tested
1. `tests/test_narrative_memory.py`:
   - Fact lifecycle (creation, state transition, provenance validation).
   - Dynamic character state tracking (injury persistence, inventory transfer).
   - Knowledge & Secret verification (preventing uninformed characters from knowing secrets).
   - World truth vs character belief separation.
   - Idempotent memory update (running update multiple times produces no duplicate entities).
   - Conflict detection and dispute recording.
2. `tests/test_long_novel_regression.py`:
   - 10-case long-form narrative regression fixture testing:
     1. Unhealed injury continuity across chapters.
     2. Item transfer invariant (A gives item to B; item stays with B).
     3. Secret containment (A knows, B does not know; B cannot reference it).
     4. Dramatic irony (reader knows truth, protagonist holds false belief).
     5. Nonlinear exposition without causal inversion.
     6. Contradictory chapter evidence leading to `disputed` status.
     7. Early clue retrieval after dormancy across many chapters.
     8. Emotion/attitude shift following a verified catalyst event.
     9. Style profile adaptation without uniform sentence flattening across scene types.
     10. Draft rejection preserving canon integrity upon save failure.

## Out of Scope
- External vector databases, embedding APIs, or third-party graph databases (standard Python JSON indexing is used).
- Full automated literary text generation without human/agent interaction (the engine provides memory and bounds, not autonomous creative writing without oversight).
- Overwriting or censoring creative metaphors as "falsehoods" (distinction between literal facts and figurative prose is respected).

## Further Notes
- All memory operations must maintain atomic safety guarantees introduced in Phase 1.
- CLI output is in Vietnamese, consistent with existing `svb-story` conventions.
