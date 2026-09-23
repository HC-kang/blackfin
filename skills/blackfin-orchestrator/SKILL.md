---
name: blackfin-orchestrator
description: Route a coding task by consequence and verification strength, then drive it to verified completion. Use when the user invokes Blackfin or asks how much review or evidence a change needs. Not for unrelated Orca operations.
---

# Blackfin / Orchestrator

Blackfin keeps three things outside the implementer's hands: acceptance, evidence, and review. Everything else is judgment. The user's instructions and repository rules outrank this skill; if a Blackfin rule makes you pause or stop short, name the skill file, quote the line, and say whether it is an explicit rule or your interpretation.

## Route

Ask two questions: what breaks if this is wrong, and how strong is the available verification? Take the highest row that applies. Model strength lowers no row; effort rises with the row.

| Situation | Route |
| --- | --- |
| Local and reversible, and a focused check proves it (exact wording, comments, static renames included) | Direct: implement, show observed evidence, done. No workers, JSON, or checkpoint tool. |
| Review requested or required, broad regression exposure, subjective acceptance, or weak verification | Direct, then a fresh Vigil before delivery. |
| Root cause or scope unclear | Structured (`HIGH_UNCERTAINTY`): Atlas contract → Forge → frozen gates → fresh Vigil. |
| Irreversible or shared: auth, payment, migration, data deletion, shared-state concurrency, security, production infrastructure | Structured (`HIGH_RISK`) plus human approval of the evaluated result. |

## Invariants

- Acceptance is owned by the user, Atlas, or the coordinator. Forge implements it and never edits it; replacement is explicit and invalidates prior evaluation. A mid-run change from the user is folded into Direct work and is an explicit replacement in a structured run.
- Evidence is observed output at the evaluated state. A summary or PASS label opens no gate; when only a summary exists, run the gate yourself.
- Every write has one owner. Child agents may investigate or implement in parallel when their scopes do not overlap: each task spec names what that agent may edit, and parallel implementers take separate worktrees when they would conflict or should land as separate PRs. Accept each result only after checking its evidence.
- Vigil is fresh and read-only. It receives acceptance, the exact diff or state, and check evidence, not the implementer's transcript. Without Vigil, report checks and gaps, never an independent PASS. A review result authorizes synthesis, not coordinator edits; fixes return to the owning Forge unless the user assigned them to the coordinator.
- Repairs are bounded: default two after the first attempt, counted across sessions. Each failed mandatory gate or Vigil FAIL consumes one. A missing prerequisite is BLOCKED, not a repair.
- A structured run finishes structured. Passing checks and review end repair, not already-authorized delivery.
- Required approval is of a concrete, evaluated result: prepare everything, then stop once, bound to that revision.

## Finish line

Name what done means before work starts. While a step needs no input, keep going and put status in the same message as the next action; a summary, an offer to continue, or non-blocking choices are not stops. Stop only when you cannot continue without the user, when approval is required, or before a destructive or out-of-scope action: deleting data, force-pushing, or changing anything outside the task. A long run keeps its task list in a file and resumes from it, not from summarized context.

The final report leads with what needs the user, then what changed, then the observed evidence and remaining gaps.

## Under Orca

Read the existing worktree note on start or resume. Update it at meaningful transitions (cause confirmed, implemented, verified, blocked, handed off) and before completion, trivial tasks included: current state, observed evidence, next action; keep unresolved items. Chat and repository memory are not the note. Verify the write; report a failed write instead of claiming it. In supervised runs the coordinator consolidates shared notes.

A handoff moves ownership: put the acceptance, route, and consumed repairs in the brief, stop once the send is accepted, and do not monitor. Supervise with a Run only when the user asks for supervision or a structured run dispatches role workers. A dispatched worker asks its coordinator through the preamble instead of stopping for the user, and reports in the `worker_done` format; the Run's task list serves as its task file.

For structured runs read [the runbook](references/runbook.md). For supervised workers, only the coordinator loads the current Orca `orchestration` guide.

Example: an off-by-one at an input boundary is Direct: fix it, run the neighboring values, report the output. A refresh-token race is `HIGH_RISK`: Atlas, frozen gates, fresh Vigil, then one approval.
