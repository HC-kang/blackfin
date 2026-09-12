# Runbook

## Route and ownership

Use `TRIVIAL` only for exact wording, comments, or static renames with no runtime, interface, data, dependency, configuration, generated-output, or security effect. The current agent may complete it directly; inspect the diff and run applicable checks. No separate acceptance role, JSON, or checkpoint tool is required.

For clear, low-impact `NORMAL` work, the human request supplies acceptance. The current agent implements, runs meaningful checks, inspects the diff, and records the outcome without mandatory JSON or workers. Missing mandatory evidence is a blocker, not permission to call the task trivial. Add fresh Vigil when review is requested/required, regression exposure is broad, acceptance is subjective, or verification is weak. Escalate material uncertainty rather than guessing. Model strength alone never lowers risk.

`HIGH_UNCERTAINTY` requires Atlas and bounded diagnosis; `HIGH_RISK` (auth, payment, migration, destructive data, shared-state concurrency, security, production infrastructure) requires Atlas and human approval. Both use the structured path below and fresh Vigil. Highest applicable class wins. Use the same structured path if the user or an automation consumer requires schema-validated artifacts; choose it before implementation, not as a fallback around a failed prerequisite.

Routine review needs only standalone acceptance, exact source state/diff, observed check evidence, and a fresh reviewer. A clean commit identifies state; for uncommitted work include tracked and untracked content identity, or use the existing checkpoint tool. Recheck state after review and before delivery; drift invalidates acceptance. No particular serialization is required. Forge claims remain hints, not proof.

Structured runs use a validated contract, revision-bound Forge handoff, and Vigil evaluation. Use role assets from one release and pass absolute paths or artifact IDs. Each criterion ID must occur once in the contract, verification mapping, and evaluation, with unchanged mandatory flags. Only the human or designated contract owner can issue an explicit replacement; it invalidates prior evaluation. Do not convert an active structured run to routine work to evade its gates.

## Gates, repairs, acceptance

Preserve user/repository-required checks on every route. For structured runs, freeze mandatory gate commands before Forge. Forge may add optional diagnostics but cannot omit or demote a frozen gate. Record command, exit result, relevant environment, and revision. Before independent review, the coordinator inspects runner-observed output at that state, or executes required gates if only Forge's summary is available. Reusing trustworthy execution evidence avoids a duplicate suite; trusting an agent's PASS label does not.

Broaden or repeat passing checks only for changes, stale/missing/suspect evidence, failures, or unresolved concerns. Vigil independently probes accepted behavior rather than mechanically running the full suite again. Optional failed/unrun diagnostics stay visible; a diagnostic contradicting mandatory acceptance blocks completion regardless of its label.

Persist the consumed repair count. Every failed mandatory gate or Vigil FAIL sent back to implementation consumes one cycle, even with session reuse; default two after the initial attempt. Return the unchanged contract and failure evidence. Missing environment/authority or contradictory requirements are BLOCKED, not an automatic repair loop. Cap investigations by time or worker count before starting them.

For structured handoffs, verify state again after Vigil: CLEAN requires matching HEAD and empty checkpoint-tool `changedFiles`; DIRTY requires matching HEAD and canonical checkpoint. PASS stops repairs; continue authorized delivery. If approval is required, record `PENDING_HUMAN_APPROVAL` bound to contract/evaluation digests and revision. Before shipping, reverify that state and record the approving actor/time; an older approval cannot approve a changed result. Do not add another confirmation when the user has already authorized the same delivery and no separate approval requirement applies.

## Execution

Reuse the existing task worktree; create another only for conflicting writes or requested isolation. Evaluate Forge's resulting state, not a divergent copy. Worktrees do not isolate host credentials or network permissions.

When supervising workers through Orca, load its current `orchestration` guide once in the coordinator. Load `orca-cli` only for additional Orca operations. Workers use injected lifecycle commands without loading whole guides. Verify task/dispatch provenance and release settled workers under that guide.

Before substantive dispatch, check model/effort selection, workspace trust, and access to required artifacts, commands, runtime, and lifecycle reporting. Inspect launch receipts; do not infer progress from a started process or bypass permission prompts. If a worker cannot report completion, inspect its evidence and record explicit coordinator recovery, never impersonate a worker result.

Keep roles provider-independent and honor configured model/effort choices. Report effective selection or fallback when observable. Without Orca, another runner must preserve the chosen route's evidence, repair count, and required fresh evaluation context; do not build a second orchestration runtime.
