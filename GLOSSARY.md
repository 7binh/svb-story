# StoryFlow Narrative Domain

The ubiquitous language and domain model for long-form novel creation, narrative continuity, and agentic story systems in StoryFlow.

## Language

### Core Entities

**Story**:
An independent fictional work consisting of chapters, characters, world rules, and narrative memory.
_Avoid_: Book, project, novel (when referring to the system entity)

**Chapter**:
A numbered, atomic narrative installment containing prose, a title, and a brief synopsis.
_Avoid_: Episode, section, installment

**Story Canon**:
The immutable collection of facts, world rules, and historical events that have been officially confirmed in saved chapters.
_Avoid_: Lore, worldbuilding (when referring specifically to confirmed truth)

**Provenance**:
The explicit origin metadata of a fact or event, including source chapter number, verbatim quote, and extraction timestamp.
_Avoid_: Citation, reference (when referring to proof of truth)

### Narrative Memory States

**World Truth**:
An objective, factual reality within the story world, independent of character awareness.
_Avoid_: Objective fact, reality

**Character Belief**:
A subjective conviction held by a character, which may be true, mistaken, or outright false.
_Avoid_: Assumption, perspective, delusion

**Secret**:
A piece of confidential story information tagged with authorized knowers, reader visibility, and narrative reveal conditions.
_Avoid_: Hidden plot, twist (when referring to information access control)

**Dispute**:
An unresolved contradiction between two chapter sources, recorded with dual provenance rather than silently overwritten.
_Avoid_: Conflict, plot hole (when referring to evidentiary contradiction)

### Slices of State

**Dynamic Character State**:
The time-varying status of a character at a given chapter, including physical injuries, held inventory, active goals, and shifting beliefs.
_Avoid_: Character sheet, profile (when referring to state over time)

**Causal Event Chain**:
The dependency-ordered sequence of events where past actions cause subsequent lasting changes.
_Avoid_: Timeline, plot points (when referring to causality)

**5-Layer Context**:
The structured briefing assembled before writing, containing Core Intent, Relevant Memory, Evidentiary Proof, Style Rules, and Recent Cadence.
_Avoid_: Prompt context, context dump

### Writing & Quality Control

**Style Fingerprint**:
The quantitative 5-axis signature of a story (sentence cadence, sensory density, dialogue ratio, character vocabulary, rhetorical devices).
_Avoid_: Tone, vibe

**Quality Gate**:
The mandatory pre-commit verification ensuring zero AI-slop, closed quotation pairs, and continuity invariant compliance.
_Avoid_: Linter, test run (when referring to prose validation)
