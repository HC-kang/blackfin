# Structured run

Use this for `HIGH_UNCERTAINTY`, `HIGH_RISK`, or when the user or an automation consumer requires schema-validated artifacts. Choose it before implementation; it is not a fallback around a failed prerequisite, and an active structured run is never converted to Direct work.

## Contract and gates

1. Atlas (or the coordinator for clear scope) writes the Acceptance Contract; the human owns it. Bound any investigation by time or worker count before it starts.
2. Freeze the mandatory gate commands before Forge starts. Forge may add optional diagnostics but cannot omit, demote, or weaken a frozen gate.
3. Forge hands off a revision-bound artifact: contract reference with digest, exact revision (`CLEAN` head, or `DIRTY` head plus canonical checkpoint), changed files, and each check with its command, result, and observed output.

## Before Vigil

Inspect runner-observed gate output at the handoff revision. If only Forge's summary exists, run the gates yourself. A failed gate returns to Forge with its output and consumes a repair; no evaluator time is spent on it.

Give Vigil the contract, the source state or diff, the handoff, and runtime access, in a fresh context. Vigil verifies the contract digest and revision before and after evaluating.

## After Vigil

- `FAIL`: return the evaluation and unchanged contract to Forge within the persisted repair budget (default two after the first attempt; failed gates and Vigil failures share it).
- `BLOCKED`: resolve the named prerequisite, environment, authority, or contradiction; this is not a repair.
- `PASS`: verify state again (`CLEAN` requires matching head and no changed files; `DIRTY` requires the same checkpoint). Repairs stop. If approval is required, record `PENDING_HUMAN_APPROVAL` bound to the contract and evaluation digests and the revision; before shipping, recheck that state and record the approving actor and time. An earlier approval cannot approve a changed result.

Only the human or designated owner replaces a contract; replacement invalidates prior evaluation and does not reset the repair budget.

## Execution

Reuse the task worktree; create another only for conflicting writes or requested isolation. Evaluate Forge's resulting state, not a copy. Pass absolute artifact paths across worktrees; keep run artifacts under `.blackfin/` or outside the implementation tree. Worktrees do not isolate credentials or network access.

Under Orca, the coordinator loads the current `orchestration` guide once; workers use their injected lifecycle commands. Before dispatch, confirm model and effort, workspace trust, and access to artifacts, commands, and lifecycle reporting. Inspect launch receipts. If a worker cannot report completion, inspect its evidence and record an explicit coordinator recovery; never report on a worker's behalf. Without Orca, another runner must preserve the route's evidence, repair count, and fresh evaluation context.
