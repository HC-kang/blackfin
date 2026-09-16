---
name: blackfin-orchestrator
description: Route a coding task by consequence and verification strength, then drive it to verified completion. Use when the user invokes Blackfin or asks how much review or evidence a change needs. Not for unrelated Orca operations.
---

# Blackfin / Orchestrator

Blackfin keeps three things outside the implementer's hands: acceptance, evidence, and review. Everything else is judgment. The user's instructions and repository rules outrank this skill; if a Blackfin rule makes you pause or stop short, name the skill file and quote the line.

## Route

Ask two questions: what breaks if this is wrong, and how strong is the available verification? Take the highest row that applies. Model strength lowers no row; effort rises with the row.

| Situation | Route |
| --- | --- |
| Local and reversible, and a focused check proves it (exact wording, comments, static renames included) | Direct: implement, show observed evidence, done. No workers, JSON, or checkpoint tool. |
| Review requested or required, broad regression exposure, subjective acceptance, or weak verification | Direct, then a fresh Vigil before delivery. |
| Root cause or scope unclear | Structured (`HIGH_UNCERTAINTY`): Atlas contract → Forge → frozen gates → fresh Vigil. |
| Irreversible or shared: auth, payment, migration, data deletion, shared-state concurrency, security, production infrastructure | Structured (`HIGH_RISK`) plus human approval of the evaluated result. |

## Invariants

- Acceptance is owned by the user, Atlas, or the coordinator. Forge implements it and never edits it; replacement is explicit and invalidates prior evaluation.
- Evidence is observed output at the evaluated state. A summary or PASS label opens no gate; when only a summary exists, run the gate yourself.
- One writer per worktree. Exploration and review may fan out; writes do not.
- Vigil is fresh and read-only. It receives acceptance, the exact diff or state, and check evidence, not the implementer's transcript. Without Vigil, report checks and gaps, never an independent PASS.
- Repairs are bounded: default two after the first attempt, counted across sessions. Each failed mandatory gate or Vigil FAIL consumes one. A missing prerequisite is BLOCKED, not a repair.
- A structured run finishes structured. Passing checks and review end repair, not already-authorized delivery.
- Required approval is of a concrete, evaluated result: prepare everything, then stop once, bound to that revision.

## Under Orca

Read the existing worktree note on start or resume. Update it at meaningful transitions (cause confirmed, implemented, verified, blocked, handed off) and before completion, trivial tasks included: current state, observed evidence, next action; keep unresolved items. Chat and repository memory are not the note. Verify the write; report a failed write instead of claiming it. In supervised runs the coordinator consolidates shared notes.

For structured runs read [the runbook](references/runbook.md). For supervised workers, only the coordinator loads the current Orca `orchestration` guide.

Example: an off-by-one at an input boundary is Direct: fix it, run the neighboring values, report the output. A refresh-token race is `HIGH_RISK`: Atlas, frozen gates, fresh Vigil, then one approval.
