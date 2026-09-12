# Blackfin

Blackfin is a small, provider-independent engineering protocol for coding agents. Orca owns execution; Blackfin preserves the user's acceptance criteria, observed evidence, and review where it earns its cost.

| Work | Route |
| --- | --- |
| Exact typo/comment/static rename | Current agent -> diff and applicable checks |
| Clear, low-impact behavior with meaningful verification | Current agent -> focused checks -> outcome |
| Requested review, broad regression exposure, subjective acceptance, weak verification | Implementation -> required checks -> fresh Vigil |
| Unclear scope/root cause | Atlas -> bounded investigation -> Forge -> gates -> fresh Vigil |
| Auth, payment, migration, destructive data, shared-state concurrency, security, production infrastructure | Atlas -> Forge -> gates -> fresh Vigil -> human approval |

Atlas plans WHAT/WHY, Forge implements HOW, and Vigil evaluates without editing. Roles are responsibilities, not mandatory sessions. Reuse the task worktree unless writes conflict. Model strength alone never lowers risk or bypasses required review.

## Install

Node.js/npm is required for the installer. Structured runs additionally use the documented JSON Schema validator, Git, and Python 3 checkpoints; routine work does not require these artifact tools.

Install the stable release globally:

```bash
npx --yes skills@latest add https://github.com/HC-kang/blackfin/tree/v0.3.0 \
  --skill blackfin-atlas --skill blackfin-forge \
  --skill blackfin-vigil --skill blackfin-orchestrator \
  --agent codex claude-code --global --yes
npx --yes skills@latest list --global
```

The example targets Codex and Claude Code; replace `--agent` with your intended clients that support global installation. Project-only clients such as PromptScript cannot use `--global`.

Rerun the command to update to this release. Use the repository URL without `/tree/v0.3.0` only to follow development on `main`. Each role ships its required schemas and checkpoint resources; install all four for coordinated runs.

## Use

```text
Use Blackfin to fix this input-boundary bug.
Use Blackfin / Vigil to evaluate <revision> against <contract-path>.
```

Routine work uses the human request as acceptance. Report what changed, observed checks, and remaining gaps; no JSON, checkpoint tool, or workers are mandatory. Add independent review for the signals above. Plain-text review is sufficient when acceptance and exact source state/diff are available; check state before/after review and before delivery. Without Vigil, do not label self-checks an independent PASS.

High-risk, high-uncertainty, and explicitly structured runs pass three validated JSON artifacts: Acceptance Contract, Forge handoff, and Vigil evaluation. The human or designated planner/coordinator owns acceptance; Forge cannot weaken it. Freeze mandatory gates before Forge, and bind evidence to the contract and actual source revision. Store artifacts in `.blackfin/` or outside the implementation tree; pass absolute paths between worktrees. An active structured run cannot be downgraded to evade a blocker.

Preserve required checks on every route. Before Vigil, inspect actual runner-observed execution evidence; run gates if only an agent summary is available. Vigil probes behavior independently; repeat passing suites only for changed/stale evidence, failures, or unresolved concerns. Optional failures remain visible and cannot conceal mandatory failures.

Every failed-gate or Vigil-FAIL transition back to implementation consumes a repair cycle. Default: two after the initial attempt, persisted across sessions. Missing mandatory prerequisites mean BLOCKED. Passing required checks/review stops repairs; continue authorized delivery without inventing another approval stop. High-risk or otherwise required human approval still binds the evaluated revision.

Under Orca, read the existing worktree note on start/resume, update at meaningful transitions and completion, and verify it saved. Include current state, evidence, and unresolved next action. Chat and project memory do not replace the worktree note.

See [task classification](references/task-classification.md), [evidence](references/evidence-policy.md), [handoffs](references/handoff-protocol.md), and [the Orca example](references/orca-integration.md) when relevant. Repository-local commands, conventions, and domain rules remain authoritative. Other runners must preserve the chosen route's evidence, retry count, and required independent review.

## Versioning and validation

Skill changes are behavioral releases: record them in [CHANGELOG.md](CHANGELOG.md), update `VERSION`, merge reviewed changes to `main`, then tag the tested merge commit. Never move a published tag.

v0.3 changes default routing, not artifact formats: structured artifacts still use `schemaVersion: "0.2.0"`; checkpoints remain `blackfin-checkpoint-v1`. Finish active runs with their selected rules or explicitly replace the contract; do not relabel evidence or reset repair budgets. The three JSON schemas remain available for strict consumers.

The [September harness review](references/harness-review-2026-09.md) explains the evidence and limits behind this change. This release does not claim a measured speed or quality gain on Blackfin tasks.

```bash
python3 -m unittest discover -s tests -v
```

`skills/` contains installable instructions; `references/` contains policy; `schemas/` and `scripts/` are canonical sources mirrored into the relevant role packages. Tests check schema semantics, checkpoint behavior, and package drift.
