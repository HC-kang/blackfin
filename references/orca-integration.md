# Orca integration

Orca owns execution, worktrees, terminals, and tracked orchestration. Blackfin owns role boundaries, artifact contracts, task routing, and acceptance policy.

Orca commands change over time. Resolve the correct executable for the current environment, then load its version-matched guides before operating:

```text
ORCA skills get orca-cli
ORCA skills get orchestration
```

`ORCA` is a documentation placeholder, not a shell variable. Use `ORCA_CLI_COMMAND` when supplied, `orca-dev` in a matching development checkout, `orca-ide` on Linux outside Orca-managed terminals, and `orca` otherwise. Continue with the same executable for the whole run.

The orchestrator reads these full guides once per run and injects the minimal current worker-lifecycle commands into each task. Atlas, Forge, and Vigil do not reload both guides merely to send heartbeat, completion, question, or escalation messages. They load a full guide only when directly operating additional Orca state.

## Worktree and permission policy

Use one isolated worktree for substantive Forge implementation. Atlas may inspect the source read-only. Vigil evaluates the resulting Forge state, preferably with write permissions removed, rather than creating a divergent implementation copy.

Pass cross-worktree artifacts by absolute shared path or artifact ID. Relative uncommitted files do not follow a newly created worktree. Pass absolute paths to the installed role schema and Forge/Vigil checkpoint tool in the same task specification.

A Git worktree is not a security sandbox. It does not isolate filesystem credentials, SSH keys, cloud credentials, Docker or Kubernetes access, or the network. Configure those permissions separately.

## Example supervised normal flow

The following is illustrative. Replace role-agent placeholders at run time and follow the loaded Orca guides when they differ.

```bash
orca status --json
orca orchestration run-create --objective "<objective>" --json

orca orchestration task-create \
  --spec "Use Blackfin / Atlas. Inspect the repository and write a validated Acceptance Contract to <absolute-contract-path-or-artifact-id>." \
  --json
orca orchestration worker-start \
  --task <atlas-task-id> --worktree current --agent <atlas-agent> --json
orca orchestration check \
  --wait --types worker_done,escalation,question --timeout-ms 900000 --json
orca orchestration worker-release --dispatch <atlas-dispatch-id> --json
orca orchestration check --ack <atlas-delivery-id> --json

orca orchestration task-create \
  --spec "Use Blackfin / Forge. Implement <absolute-contract-path-or-artifact-id>, run deterministic gates, and write <absolute-forge-handoff-path-or-artifact-id>." \
  --json
orca orchestration worker-start \
  --task <forge-task-id> --worktree new-child --name <worktree-name> \
  --agent <forge-agent> --setup run --json
orca orchestration check \
  --wait --types worker_done,escalation,question --timeout-ms 900000 --json
orca orchestration worker-release --dispatch <forge-dispatch-id> --json
orca orchestration check --ack <forge-delivery-id> --json

# Only after the Forge handoff records passing mandatory deterministic gates:
orca orchestration task-create \
  --spec "Use Blackfin / Vigil. Evaluate <forge-revision> against <absolute-contract-path-or-artifact-id>; write <absolute-evaluation-path-or-artifact-id>; do not modify implementation." \
  --json
orca orchestration worker-start \
  --task <vigil-task-id> --worktree id:<repo-id>::<forge-worktree-path> \
  --agent <vigil-agent> --json
orca orchestration check \
  --wait --types worker_done,escalation,question --timeout-ms 900000 --json
orca orchestration worker-release --dispatch <vigil-dispatch-id> --json
orca orchestration check --ack <vigil-delivery-id> --json
```

Process every message in a returned delivery before acknowledging it. A timeout is a liveness checkpoint, not proof of failure. Use the exact worker and delivery lifecycle described by the current Orca guide.

On Vigil FAIL, consume one repair cycle, create or resume Forge repair in the same feature worktree, and pass the contract plus evaluation artifact. Repeat deterministic gates and use a fresh Vigil context. A failed mandatory gate consumes a cycle before implementation resumes. Stop at the configured limit. On PASS, independently verify CLEAN or DIRTY state as defined by the checkpoint protocol, stop automated iteration, and set the worktree to review when configured.

## Checkpoints

Use short, evidence-oriented worktree comments at meaningful transitions:

```bash
orca worktree set --worktree active --comment "planning complete; contract validated" --json
orca worktree set --worktree active --comment "deterministic gates passed; ready for Vigil" --json
orca worktree set --worktree active --comment "Vigil PASS; ready for human review" --json
```

Useful lifecycle names are `investigation-started`, `root-cause-confirmed`, `planning-complete`, `implementation-started`, `implementation-complete`, `deterministic-checks-passed`, `ready-for-evaluation`, `evaluation-failed`, `repair-started`, `evaluation-passed`, and `blocked`.
