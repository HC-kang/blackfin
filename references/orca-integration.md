# Orca integration

Orca owns execution and lifecycle. Blackfin owns acceptance and evidence. For supervised work, resolve the CLI through the installed `orchestration` skill and read its version-matched guide once. Read `orca-cli` only for additional workspace or browser operations. Workers use the injected lifecycle preamble.

Before dispatch, confirm model/effort, workspace trust, required artifact/runtime access, and lifecycle permissions. Inspect launch receipts; a terminal existing is not proof that an agent accepted the task. Do not bypass provider trust prompts. Failed lifecycle reporting requires an explicit coordinator recovery record after inspecting evidence, not a forged worker completion.

## Clear normal flow

The coordinator uses the Atlas authoring card/schema to create the contract and freezes mandatory gates, without a separate planner worker. The example assumes an existing task worktree; create another only when conflicting writes or requested isolation require it. Substitute discovered IDs and absolute artifact paths.

```bash
orca orchestration run-create --objective "<bounded objective>" --json
orca orchestration task-create \
  --spec "Use Blackfin / Forge. Implement <absolute-contract-path>, run <frozen-gates>, and write <absolute-handoff-path>. Role assets: <absolute-skill-path>." --json
orca orchestration worker-start \
  --task <forge-task-id> --worktree current --agent <agent> --json
orca orchestration check \
  --wait --types worker_done,escalation,question --timeout-ms 60000 --json
# Process the whole delivery. Release a settled worker, not a timed-out active worker.
orca orchestration worker-release --dispatch <forge-dispatch-id> --json
orca orchestration check --ack <forge-delivery-id> --json

# Verify contract/revision identity and actual runner-observed frozen-gate output.
# If only Forge's summary is available, execute those commands in Forge's worktree.
# Failure returns to a counted Forge repair. Only observed passing gates open Vigil.
orca orchestration task-create \
  --spec "Use Blackfin / Vigil. Evaluate <handoff-revision> against <absolute-contract-path>, inspect <absolute-handoff-path>, and write <absolute-evaluation-path>. Do not edit implementation. Role assets: <absolute-skill-path>." --json
orca orchestration worker-start \
  --task <vigil-task-id> --worktree current --agent <agent> --json
orca orchestration check \
  --wait --types worker_done,escalation,question --timeout-ms 60000 --json
orca orchestration worker-release --dispatch <vigil-dispatch-id> --json
orca orchestration check --ack <vigil-delivery-id> --json
```

Continue rolling waits until expected dispatches settle; timeouts are liveness checkpoints. Follow the loaded guide for questions, failed starts, retries, and cleanup. Verify task/dispatch provenance before claiming orchestration.

For uncertainty/high risk, add Atlas before Forge and cap any investigation. High risk requires human approval. Trivial edits need no Run or workers.

Return gate failures as commands/output, Vigil failures as evaluation artifacts, and preserve the contract and consumed repair count. Default two repairs after the initial attempt. Reverify the exact revision after Vigil; PASS stops automation and leaves configured human approval pending.

Use one resulting implementation state for evaluation and absolute paths across worktrees. Never treat worktrees as credential or network sandboxes. Keep concise, evidence-oriented worktree comments at meaningful transitions; ordinary file edits do not require loading Orca guides.
