---
name: blackfin-orchestrator
description: Choose the smallest Blackfin workflow, preserve externally owned acceptance, and coordinate independent evaluation and bounded repairs.
---

# Blackfin / Orchestrator

Keep acceptance independent of implementation. Roles are responsibilities, not mandatory extra sessions or fixed model providers.

1. Inspect the task and choose its route:
   - `TRIVIAL`: exact wording/comment/static rename with no behavioral effect. Complete directly with a diff check and relevant repository checks; no role workers or JSON artifacts required.
   - `NORMAL`: clear, bounded behavior. Author or reuse a validated contract in the coordinator context, then Forge -> gates -> fresh Vigil. Use Atlas only when planning would resolve a material ambiguity.
   - `HIGH_UNCERTAINTY` or `HIGH_RISK`: Atlas -> bounded investigation if needed -> Forge -> gates -> fresh Vigil. High risk also requires human approval.
2. Fix the acceptance criteria and mandatory gate commands before Forge starts. Forge cannot weaken either. Pass artifacts, not conversational reasoning.
3. Use the existing task worktree when safe; isolate conflicting implementations. Choose provider and effort per task, not by role name.
4. Confirm gate results from actual execution at the handoff revision before dispatching Vigil. Stop failed gates at Forge; do not spend evaluator work on them.
5. Return reproducible failures to Forge. Default to two repair cycles after the initial attempt, counting failed gates and Vigil failures together; stop on exhaustion or missing prerequisites.
6. PASS stops automated iteration. Honor any required human approval against the evaluated revision before accepting or shipping it.

Before a multi-role run, read [the runbook](references/runbook.md). Use the current Orca `orchestration` guide for supervised workers; only the coordinator loads that guide for lifecycle operations.

Example: a known input-boundary bug needs a short coordinator-authored contract, Forge, and fresh Vigil. An authentication race needs Atlas and human review as well.
