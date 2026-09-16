# Blackfin

Blackfin is a small, provider-independent engineering protocol for coding agents. Orca owns execution; Blackfin keeps three things outside the implementer's hands: acceptance, evidence, and review. Everything else is the model's judgment.

Route by two questions: what breaks if the change is wrong, and how strong is the available verification?

| Situation | Route |
| --- | --- |
| Local and reversible, and a focused check proves it (exact wording and static edits included) | Direct: implement, show observed evidence, done |
| Review requested or required, broad regression exposure, subjective acceptance, weak verification | Direct, then a fresh Vigil |
| Root cause or scope unclear | Structured: Atlas -> Forge -> frozen gates -> fresh Vigil |
| Irreversible or shared: auth, payment, migration, data deletion, shared-state concurrency, security, production infrastructure | Structured plus one human approval of the evaluated result |

Atlas owns WHAT and WHY, Forge is the single writer, and Vigil reviews in a fresh read-only context. Roles are responsibilities, not mandatory sessions. Model strength lowers no row. The user's instructions outrank Blackfin, and a Blackfin-caused pause names the skill and line.

## Install

Node.js/npm is required for the installer. Structured runs additionally use the documented JSON Schema validator, Git, and Python 3 checkpoints; routine work does not require these artifact tools.

Install the stable release globally:

```bash
npx --yes skills@latest add https://github.com/HC-kang/blackfin/tree/v0.4.0 \
  --skill blackfin-atlas --skill blackfin-forge \
  --skill blackfin-vigil --skill blackfin-orchestrator \
  --agent codex claude-code --global --yes
npx --yes skills@latest list --global
```

The example targets Codex and Claude Code; replace `--agent` with your intended clients that support global installation. Project-only clients such as PromptScript cannot use `--global`.

Rerun the command to update to this release. Use the repository URL without `/tree/v0.4.0` only to follow development on `main`. Each role ships its required schemas and checkpoint resources; install all four for coordinated runs.

## Use

```text
Use Blackfin to fix this input-boundary bug.
Use Blackfin / Vigil to evaluate <revision> against <contract-path>.
```

Direct work uses the human request as acceptance and ends with the change, the observed commands and output, and remaining gaps; no JSON, checkpoint tool, or workers. Forge audits each claim against a tool result before reporting. Add a fresh Vigil for the signals above; without one, self-checks are never an independent PASS.

Structured runs pass three validated JSON artifacts: Acceptance Contract, Forge handoff, and Vigil evaluation. Mandatory gates are frozen before Forge; evidence is bound to the contract and the exact source revision; every failed gate or Vigil FAIL consumes one of two default repair cycles; a structured run cannot be downgraded around a blocker. High-risk approval binds to the evaluated revision after everything else is prepared.

Vigil starts each criterion at FAIL, probes behavior beyond the shipped tests, and reports the whole diff before marking what affects acceptance. State is checked before and after review.

Under Orca, read the existing worktree note on start or resume, update it at meaningful transitions and before completion, and verify it saved. Chat and project memory do not replace the note.

See [task classification](references/task-classification.md), [evidence](references/evidence-policy.md), [handoffs](references/handoff-protocol.md), and [the Orca example](references/orca-integration.md) when relevant. Repository-local commands, conventions, and domain rules remain authoritative.

## Versioning and validation

Skill changes are behavioral releases: record them in [CHANGELOG.md](CHANGELOG.md), update `VERSION`, merge reviewed changes to `main`, then tag the tested merge commit. Never move a published tag.

v0.4 rewrites the skills as invariants, not artifact formats: structured artifacts still use `schemaVersion: "0.2.0"`; checkpoints remain `blackfin-checkpoint-v1`. Finish active runs with their selected rules or explicitly replace the contract.

[Harness evidence](references/harness-evidence-2026-09.md) and the earlier [harness review](references/harness-review-2026-09.md) record the research and its limits. No release claims a measured speed or quality gain on Blackfin tasks.

```bash
python3 -m unittest discover -s tests -v
```

`skills/` contains installable instructions; `references/` contains policy; `schemas/` and `scripts/` are canonical sources mirrored into the relevant role packages. Tests check schema semantics, checkpoint behavior, package drift, and skill entrypoints (portable frontmatter, size, links, note obligation).
