# Handoff protocol

Blackfin handoffs are standalone artifacts tied to exact repository state. Conversation history is optional and must not be required for correctness.

The contract reference in each handoff contains its location or artifact ID plus a SHA-256 digest. Recompute the digest before use; a mismatch blocks the run instead of silently changing acceptance criteria.

## Artifact flow

```text
Acceptance Contract
        |
        v
Forge + repository instructions
        |
        v
revision + Forge handoff
        |
        v
Vigil + diff + runtime
        |
   FAIL | PASS
        |   `-> stop automation; human review if configured
        `----> Forge repair
```

The runner chooses storage. A useful run-directory convention is:

```text
<run-directory>/acceptance-contract.json
<run-directory>/forge-handoff.<attempt>.json
<run-directory>/evaluation.<attempt>.json
```

Do not require this path layout when an orchestrator provides equivalent artifact IDs.
When roles run in different worktrees, use absolute shared paths or artifact IDs. An uncommitted relative file does not appear in a newly created worktree.

## Atlas to Forge

Pass the validated Acceptance Contract and repository state. Do not require Atlas's hidden reasoning. Forge may report a blocking contradiction but cannot rewrite the contract.

## Forge to Vigil

This structured handoff is required for every non-trivial route. `TRIVIAL` instead returns changed files and frozen gate results directly to the orchestrator; any behavioral interpretation upgrades the route to `NORMAL`.

Pass:

- the unchanged Acceptance Contract;
- the exact revision, including relevant uncommitted worktree state;
- the complete diff;
- the Forge handoff validated by [`../schemas/generator-handoff.schema.json`](../schemas/generator-handoff.schema.json);
- access to the relevant runtime or test environment.

`READY_FOR_EVALUATION` requires mandatory deterministic gates to pass. Otherwise return to Forge or emit `BLOCKED`.

For a clean worktree, `checkpoint` must be absent; Forge and Vigil run the checkpoint tool and require matching `HEAD` plus empty `changedFiles`. For a dirty worktree, use the canonical [`checkpoint`](checkpoint.md), which covers tracked and non-ignored untracked state outside reserved `.blackfin/`. Vigil confirms it before and after evaluation.

## Vigil to Forge or human

Validate Vigil output with [`../schemas/evaluation.schema.json`](../schemas/evaluation.schema.json).

- `FAIL`: return criterion-level evidence and the smallest reliable reproduction to Forge. Keep the contract unchanged.
- `PASS`: terminate automated iteration and request human review when the contract or run configuration requires it.
- `BLOCKED`: escalate the missing prerequisite or contract defect.

The orchestrator must enforce its repair-cycle limit. The default is two cycles after the initial Forge implementation; limit exhaustion escalates rather than silently accepting or looping forever.

Every transition from a failed mandatory gate or Vigil `FAIL` back to implementation consumes one repair cycle, even when the same Forge session continues. Persist artifacts and the consumed count so an interrupted run resumes from the last validated transition rather than resetting its limit.

Gate-failure repair input is the unchanged contract plus failed command and observed output; do not fabricate a Vigil evaluation. Vigil-failure repair input is the unchanged contract plus evaluation artifact.

If a human rejects a PASS without changing the contract, route the evidence to a counted Forge repair. If the requested behavior changes, return to Atlas for an explicit replacement contract and invalidate the prior evaluation.
