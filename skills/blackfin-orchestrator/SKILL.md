---
name: blackfin-orchestrator
description: Classify and coordinate a complete Blackfin engineering run across Atlas, Forge, deterministic gates, and Vigil using Orca when available. Use for supervised multi-role workflows, bounded repair loops, and evidence-based handoffs; skip full ceremony for trivial tasks.
---

# Blackfin / Orchestrator

Route work; do not collapse role ownership. Orca supplies execution and tracked coordination. Blackfin supplies policy.

## Invariants

- Classify before routing. Multi-agent work is a risk control, not a default ceremony.
- Keep role selection independent from provider selection.
- Pass artifacts and repository state between roles, not hidden conversational reasoning.
- Atlas owns the Acceptance Contract. Forge implements it. Vigil evaluates without editing.
- Run deterministic gates before Vigil; failed gates return directly to Forge.
- Stop automated repair after the configured limit. Default: two repair cycles after the initial Forge attempt; every failed-gate or Vigil-FAIL transition back to implementation consumes one, regardless of session reuse.
- PASS terminates agent iteration. High-risk or configured work transitions to `PENDING_HUMAN_APPROVAL`, not final acceptance.

## Workflow

1. Classify the task and choose the smallest valid route.
2. For substantive implementation, use an isolated Orca worktree. Treat permissions and credentials separately; a worktree is not a sandbox.
3. Dispatch Atlas when required and preserve its contract as a standalone artifact. Enforce unique criterion IDs and one verification mapping per required behavior.
4. Before Forge starts, persist the mandatory deterministic gate commands derived from repository instructions and the contract where present. Forge may add checks but cannot omit this set.
5. Dispatch Forge with the contract or exact trivial task plus repository instructions.
6. Independently execute the frozen deterministic gates; Forge's check claims are not sufficient. For non-trivial work, also require a revision-bound Forge handoff.
7. Dispatch a fresh Vigil context with the contract, handoff, revision, diff, runtime access, and absolute paths to the installed schemas and checkpoint tool.
8. On reproducible Vigil `FAIL`, return its evaluation artifact to Forge. On a failed mandatory gate, return that command and observed output instead. Consume one repair cycle, then repeat gates and Vigil within the remaining limit.
9. On PASS, stop; request configured human review. On limit exhaustion or BLOCKED, escalate with evidence.

For `TRIVIAL`, record the starting HEAD/checkpoint, then pass Forge the exact human task with no Acceptance Contract or non-trivial handoff. The orchestrator independently confirms the resulting diff is limited to that mechanical request and reruns the frozen gates. Forge still does not accept its own work. Any interpretation or missing meaningful check upgrades the task to `NORMAL`.

Load [references/runbook.md](references/runbook.md) before starting a run. When Orca is available, the orchestrator loads the installed `orca-cli` and `orchestration` skills and supplies workers with the minimal version-matched lifecycle commands they need.
