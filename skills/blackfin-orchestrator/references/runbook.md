# Runbook

## Route and ownership

Use `TRIVIAL` only for exact wording, comments, or static renames with no runtime, interface, data, dependency, configuration, generated-output, or security effect. The current agent may complete it directly; inspect the diff and run applicable checks. No separate acceptance role, JSON, or checkpoint tool is required.

For clear `NORMAL` work, the human or coordinator owns the contract; author it with the Atlas skill's schema/card without starting a planner worker. Forge and Vigil still use separate contexts. Add Atlas when scope or verification needs investigation. `HIGH_UNCERTAINTY` requires Atlas and bounded diagnosis; `HIGH_RISK` (auth, payment, migration, destructive data, shared-state concurrency, security, production infrastructure) requires Atlas and human approval. Highest applicable class wins.

All non-trivial routes use a validated contract, revision-bound Forge handoff, and Vigil evaluation. Use all role assets from one release and pass absolute paths or artifact IDs. Each criterion ID must occur once in the contract, verification mapping, and evaluation, with unchanged mandatory flags. Only the human or designated contract owner can issue an explicit replacement; it invalidates prior evaluation.

## Gates, repairs, acceptance

Freeze mandatory gate commands before Forge. Forge may add optional diagnostics but cannot omit or demote a frozen gate. Record command, exit result, relevant environment, and revision. The coordinator must inspect runner-observed output at that exact state, or execute the frozen gates itself if only Forge's summary is available. Reusing trustworthy execution evidence avoids a duplicate suite; trusting an agent's PASS label does not.

Do not broaden passing checks without new evidence. Vigil independently probes contract behavior rather than mechanically running the full suite again. Optional failed/unrun diagnostics stay visible; a diagnostic that contradicts a mandatory criterion blocks READY regardless of its label.

Persist the consumed repair count. Every failed mandatory gate or Vigil FAIL sent back to implementation consumes one cycle, even with session reuse; default two after the initial attempt. Return the unchanged contract and failure evidence. Missing environment/authority or contradictory requirements are BLOCKED, not an automatic repair loop. Cap investigations by time or worker count before starting them.

Verify the handoff state again after Vigil: CLEAN requires matching HEAD and empty checkpoint-tool `changedFiles`; DIRTY requires matching HEAD and canonical checkpoint. PASS stops iteration. If approval is required, record `PENDING_HUMAN_APPROVAL` bound to contract/evaluation digests and revision. Before shipping, reverify that state and record the approving actor/time; an older approval cannot approve a changed result.

## Execution

Reuse the existing task worktree; create another only for conflicting writes or requested isolation. Evaluate Forge's resulting state, not a divergent copy. Worktrees do not isolate host credentials or network permissions.

When supervising workers through Orca, load its current `orchestration` guide once in the coordinator. Load `orca-cli` only for additional Orca operations. Workers use injected lifecycle commands without loading whole guides. Verify task/dispatch provenance and release settled workers under that guide.

Before substantive dispatch, check model/effort selection, workspace trust, and access to required artifacts, commands, runtime, and lifecycle reporting. Inspect launch receipts; do not infer progress from a started process or bypass permission prompts. If a worker cannot report completion, inspect its evidence and record explicit coordinator recovery, never impersonate a worker result.

Use provider-independent roles and the lowest sufficient effort; frontier models need not fill every role. A stronger model does not waive independent evaluation. Report effective model selection or fallback when observable. Without Orca, use another runner only if it preserves artifacts, attempt counts, and a fresh Vigil context.
