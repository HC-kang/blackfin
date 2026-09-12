---
name: blackfin-orchestrator
description: Route Blackfin work by risk and verification needs; coordinate review when needed.
---

# Blackfin / Orchestrator

Keep acceptance externally owned. Roles are responsibilities, not mandatory sessions or fixed model providers. Follow the user's scope and repository requirements; do not add approval stops to already-authorized work.

1. Inspect the task and choose its route:
   - `TRIVIAL`: exact wording/comment/static rename with no behavioral effect. Complete directly with a diff check and relevant repository checks; no role workers or JSON artifacts required.
   - `NORMAL`: clear, low-impact behavior with understood scope and meaningful verification. Complete in the current session using the human request, focused checks, and a short outcome record; no workers, JSON, or checkpoint tool required by default. Add fresh Vigil for requested review, broad regression exposure, subjective acceptance, or weak verification. Never use this route to bypass a required gate or approval.
   - `HIGH_UNCERTAINTY` or `HIGH_RISK`: Atlas -> bounded investigation if needed -> Forge -> gates -> fresh Vigil. High risk also requires human approval.
2. Establish expected behavior and required checks before implementation. Do not weaken either to fit the result. For structured runs, freeze the contract and mandatory gate commands before Forge.
3. Use the existing task worktree when safe; isolate conflicting implementations. Choose provider and effort per task, not by role name.
4. Confirm gate results from actual execution at the handoff revision before dispatching Vigil. Stop failed gates at Forge; do not spend evaluator work on them.
5. Return reproducible failures for repair. Default to two repair cycles after the initial attempt, counting failed gates and Vigil failures together; stop on exhaustion or missing mandatory prerequisites. Do not relabel work to evade a blocker.
6. Stop repair iteration when required checks and any required review pass; continue the user's authorized delivery steps. Without Vigil, report checks and remaining gaps, not an independent PASS. Approval is required only where the user, repository, or high-risk route requires it; bind it to the evaluated state.

Under Orca, the task owner must read the existing worktree comment on start/resume and update it at meaningful transitions (confirmed cause, implementation or verification result, blocker, handoff) and before task completion, including trivial tasks. Record current state, observed evidence, and blockers/next action in the user's language; preserve unresolved items. Chat replies and repository memory do not replace this note. The coordinator consolidates shared-worktree notes in supervised runs. Verify the saved comment; if writing fails, report the error and pending note rather than claiming it was saved.

For independent review or a structured run, read [the runbook](references/runbook.md). Use the current Orca `orchestration` guide for supervised workers; only the coordinator loads that guide for lifecycle operations.

Example: fix a local input-boundary bug and verify neighboring values directly. An authentication race needs Atlas, structured evidence, fresh Vigil, and human approval.
