# Blackfin

Blackfin is a small, provider-independent engineering protocol for coding agents. Orca owns execution; Blackfin preserves acceptance criteria, evidence, independent evaluation, and bounded repairs.

| Work | Route |
| --- | --- |
| Exact typo/comment/static rename | Current agent -> diff and applicable checks |
| Clear, bounded behavior | Coordinator-authored contract -> Forge -> gates -> fresh Vigil |
| Unclear scope/root cause | Atlas -> bounded investigation -> Forge -> gates -> fresh Vigil |
| Auth, payment, migration, destructive data, shared-state concurrency, security, production infrastructure | Atlas -> Forge -> gates -> fresh Vigil -> human approval |

Atlas plans WHAT/WHY, Forge implements HOW, and Vigil evaluates without editing. Clear normal work does not need a separate planner session. Reuse an existing task worktree unless writes conflict. Roles never imply a particular model provider.

## Install

Node.js/npm is required for the installer and the documented JSON Schema validator. Git and Python 3 are required for revision checkpoints.

Install the stable release globally:

```bash
npx --yes skills@latest add https://github.com/HC-kang/blackfin/tree/v0.2.1 \
  --skill blackfin-atlas --skill blackfin-forge \
  --skill blackfin-vigil --skill blackfin-orchestrator \
  --agent codex claude-code --global --yes
npx --yes skills@latest list --global
```

The example targets Codex and Claude Code; replace `--agent` with your intended clients that support global installation. Project-only clients such as PromptScript cannot use `--global`.

Use the repository URL without `/tree/v0.2.1` only to follow development on `main`. Each role ships its own required schemas and checkpoint resources; install all four for coordinated runs.

## Use

```text
Use Blackfin to fix this input-boundary bug.
Use Blackfin / Vigil to evaluate <revision> against <contract-path>.
```

Non-trivial work passes three validated JSON artifacts: Acceptance Contract, Forge handoff, and Vigil evaluation. The human or designated planner/coordinator owns the contract; Forge cannot weaken it. Store artifacts in `.blackfin/` or outside the implementation tree and pass absolute paths between worktrees.

Before Forge, fix the mandatory gate commands. The coordinator verifies their actual execution evidence at the handoff revision, executing them if only an agent summary is available. Vigil probes contract behavior independently; passing suites need not be repeated without cause. Optional diagnostics remain visible even when failed or unrun.

Every failed-gate or Vigil-FAIL transition back to implementation consumes a repair cycle. Default: two after the initial attempt. Missing prerequisites mean BLOCKED; PASS stops automation and leaves required human approval pending against that revision.

Choose models and effort at runtime for the work. Stronger models do not require more ceremony or waive independent evaluation. Provider startup/trust and lifecycle permissions must work before substantive dispatch.

See [task classification](references/task-classification.md), [evidence](references/evidence-policy.md), [handoffs](references/handoff-protocol.md), and [the Orca example](references/orca-integration.md). Repository-local architecture, commands, conventions, and domain rules remain authoritative. Other runners may be used if they preserve artifacts, retry counts, and fresh evaluation contexts.

## Versioning and validation

Skill changes are behavioral releases: record them in [CHANGELOG.md](CHANGELOG.md), update `VERSION`, merge reviewed changes to `main`, then tag the tested merge commit. Never move a published tag.

v0.2 artifacts use `schemaVersion: "0.2.0"`. Finish active v0.1 runs with v0.1 assets or start an explicit replacement contract; do not relabel old evidence. The checkpoint format remains `blackfin-checkpoint-v1`.

```bash
python3 -m unittest discover -s tests -v
```

`skills/` contains installable instructions; `references/` contains policy; `schemas/` and `scripts/` are canonical sources mirrored into the relevant role packages. Tests check schema semantics, checkpoint behavior, and package drift.
