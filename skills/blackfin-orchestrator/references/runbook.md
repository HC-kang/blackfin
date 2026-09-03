# Orchestrator runbook

## Classification

| Class | Typical signals | Route |
| --- | --- | --- |
| `TRIVIAL` | Typo, comment, obvious static rename | Forge -> gates -> orchestrator completion |
| `NORMAL` | Business logic, endpoint, or UI behavior | Atlas -> Forge -> gates -> Vigil |
| `HIGH_UNCERTAINTY` | Unknown root cause, performance, concurrency | Atlas + bounded investigation -> Forge -> gates -> Vigil |
| `HIGH_RISK` | Auth, payment, migration, destructive data, security, production infrastructure | Atlas -> optional investigation -> Forge -> gates -> Vigil -> human |

Choose the highest applicable class. Keep investigations bounded and use independent workers only when distinct hypotheses justify them.

`TRIVIAL` is limited to wording, comment-only changes, and obvious static renames with no runtime, interface, data, dependency, configuration, generated-output, or security effect. Any uncertainty is at least `NORMAL`. Every class except `TRIVIAL` uses an Acceptance Contract and Forge handoff.

The orchestrator owns the route. Atlas may return evidence that requires reclassification. For an investigation, the orchestrator names the distinct hypotheses, caps the worker count or time, and asks Atlas to synthesize evidence before Forge starts.

## Artifact boundary

- Atlas -> Acceptance Contract
- Forge -> exact repository revision plus Forge handoff
- Vigil -> evaluation with criterion-level evidence
- FAIL -> evaluation artifact back to Forge
- Gate failure -> failed command and observed output back to Forge; no evaluation artifact is fabricated

Do not silently revise the contract during a repair. Contract changes return to Atlas or the human and must be explicit.

Across worktrees, pass artifacts by absolute shared path or artifact ID; relative uncommitted files do not follow a newly created worktree.

Persist contract and handoff digests plus the consumed repair count so an interrupted run can resume without resetting its limits.

Before Forge dispatch, persist the mandatory gate command set from repository instructions plus deterministic checks required by the contract. Forge may add checks but cannot remove this set. The orchestrator, not Forge, executes the frozen set before Vigil or trivial completion.

Every transition from a failed mandatory gate or Vigil `FAIL` back to implementation consumes one repair cycle, whether Forge is reused or newly dispatched. The default permits two repair cycles after the initial implementation. Persist and check the count before authorizing more edits.

A gate-failure repair receives the unchanged contract plus failed command and output. A Vigil-failure repair receives the unchanged contract plus evaluation artifact.

A Vigil `PASS` ends agent iteration. If the contract or route requires approval, record `PENDING_HUMAN_APPROVAL` with the contract digest, evaluation digest, HEAD, and checkpoint when dirty. Reverify that exact state immediately before recording the approving actor and time; stale approval cannot complete a changed revision. If no durable approval record is available, do not mark the run complete.

For `TRIVIAL`, record the starting HEAD and checkpoint before Forge. Completion requires the orchestrator to inspect the baseline-to-result diff and independently rerun the frozen gates; Forge's report alone is not acceptance evidence.

## Orca boundary

Use Orca orchestration only for supervised coordination. The orchestrator resolves the executable, loads `orca skills get orca-cli` and `orca skills get orchestration`, and follows their current task/worker lifecycle. It includes the minimal current heartbeat, completion, question, and escalation commands in each dispatch. Role workers must not load both full guides solely to complete that lifecycle; they load them only if they must operate additional Orca state directly.

Resolve all role assets from one Blackfin release, reject unsupported artifact `schemaVersion` values, and pass absolute installed paths for each role's schema and Forge/Vigil checkpoint tool. After Vigil settles, independently verify the handoff: DIRTY requires matching `HEAD` and checkpoint; CLEAN requires matching `HEAD` and empty tool `changedFiles`.

The orchestrator specifies material runtime prerequisites in each dispatch. Forge records the environment it actually used in check evidence; Vigil establishes its environment independently and does the same. Missing material environment evidence is `BLOCKED`.

Use a fresh agent context for Vigil. Release or explicitly retain every settled worker as directed by the current Orca guide.

Without Orca, a runner may execute the same route only if it can create separate role contexts and persist the same artifacts and attempt count. If it cannot provide a fresh independent Vigil context, a route requiring Vigil is `BLOCKED`; do not replace independence with hidden conversation.

Checkpoint worktree comments at meaningful state changes: planning complete, implementation complete, deterministic gates passed, evaluation failed or passed, and blocked. Keep comments evidence-oriented.

Do not treat worktree isolation as a security sandbox. Configure filesystem, network, cloud, Docker, and other credentials independently.
