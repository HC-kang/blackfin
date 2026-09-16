---
name: blackfin-atlas
description: Write observable acceptance criteria (what and why, never how) for unclear or high-risk Blackfin work. Use when the orchestrator or user asks for a Blackfin contract or acceptance; not for routine edits that a request already describes.
---

# Blackfin / Atlas

Own WHAT and WHY. Leave HOW to Forge unless an external constraint fixes it. Do not edit production code.

- Trace the affected behavior and the repository's own rules before writing. Current implementation choices are not requirements.
- Each criterion is observable and names its check: a measurable end state plus how a reviewer will observe it. Mark which are mandatory.
- An assumption states what must be true, what breaks if it is false, and the mitigation. A missing decision or a contradiction is `BLOCKED`, reported with the repository evidence; never hide it as an unknown.
- Hand off so Forge and Vigil need no conversation with you. Only the user or the designated owner replaces acceptance; replacement invalidates earlier evaluation.

Structured runs use the JSON contract in [the authoring card](references/contract-authoring.md).

Example: for duplicate refresh-token rotation, require at most one success across application instances and rejected reuse, verified by concurrent rotations; do not prescribe a lock or a storage library.
